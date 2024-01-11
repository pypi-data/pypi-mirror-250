# Conditional GAN Implementation
import numpy as np
import torch
import torch.nn as nn
from torch.distributions import Categorical

from torch.utils.data import DataLoader

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import accuracy_score
from sklearn.metrics.pairwise import euclidean_distances

from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

from .DataTransformers import DataTransformer
from .gan_discriminators import PackedDiscriminator
from .gan_generators import Generator
from .BaseGenerators import BaseGAN


class clusterGAN(BaseGAN):
    """
    Safe-Borderline GAN

    Conditional GANs (cGANs) conditionally generate data from a specific class. They are trained
    by providing both the Generator and the Discriminator the input feature vectors concatenated
    with their respective one-hot-encoded class labels.

    A Packed Conditional GAN (Pac cGAN) is a cGAN that accepts input samples in packs. Pac cGAN
    uses a Packed Discriminator to prevent the model from mode collapsing.
    """

    def __init__(self, embedding_dim=128, discriminator=(128, 128), generator=(256, 256), pac=10, adaptive=False,
                 g_activation='tanh', epochs=300, batch_size=32, lr=2e-4, decay=1e-6, min_distance_factor=2,
                 random_state=0):
        """
        Initializes a Safe-Borderline Conditional GAN.

        Args:
            embedding_dim: Size of the random sample passed to the Generator.
            discriminator: a tuple with number of neurons in each fully connected layer of the Discriminator. It
                determines the dimensionality of the output of each layer.
            generator: a tuple with number of neurons in each fully connected layer of the Generator. It
                determines the dimensionality of the output of each residual block of the Generator.
            pac: Number of samples to group together when applying the discriminator.
            adaptive: boolean value to enable/disable adaptive training.
            g_activation: The activation function of the Generator's output layer.
            epochs: Number of training epochs.
            batch_size: Number of data instances per training batch.
            lr: Learning rate parameter for the Generator/Discriminator Adam optimizers.
            decay: Weight decay parameter for the Generator/Discriminator Adam optimizers.
            min_distance_factor:
            random_state: An integer for seeding the involved random number generators.
        """
        super().__init__(embedding_dim, discriminator, generator, pac, adaptive, g_activation, epochs, batch_size,
                         lr, decay, random_state)

        self._min_distance_factor = min_distance_factor
        self._n_clusters = 0
        self._cluster_class_distribution = []

    def cluster_prepare(self, x_train, y_train):
        """
        Refine the training set with sample filtering. It invokes `prepare` to return the preprocessed data.

        Args:
            x_train: The training data instances.
            y_train: The classes of the training data instances.

        Returns:
            A tensor with the preprocessed data.
        """

        self._n_classes = len(set(y_train))

        # ====== 1. Feature Transformation Step: First standardize, then project to a latent space of max variance.
        self._input_dim = x_train.shape[1]
        self._transformer = Pipeline([
                ('scaler', StandardScaler(with_mean=True, with_std=True)),
                ('pca', PCA(n_components=self._input_dim))
            ])

        self._transformer.fit(x_train)
        x_train_projected = self._transformer.transform(x_train)

        # ====== 2. Clustering step
        n_components = range(1, 30)
        covariance_type = ['spherical', 'tied', 'diag', 'full']
        score = []
        for cov in covariance_type:
            for n_comp in n_components:
                gmm = GaussianMixture(n_components=n_comp, covariance_type=cov, random_state=self._random_state)
                gmm.fit(x_train)
                score.append((cov, n_comp, gmm.bic(x_train)))

        best = min(score, key=lambda tup: tup[2])
        self._n_clusters = best[1]
        best_cov = best[0]
        print(best)

        gmm = GaussianMixture(n_components=self._n_clusters, covariance_type=best_cov, random_state=self._random_state)
        gmm.fit(x_train)
        cluster_labels = gmm.predict(x_train)

        '''
        # First, Apply a simple heuristic to get the max distance between two clusters.
        # Compute the distances and get the median, then divide the median by self._min_distance_factor
        e_dists = euclidean_distances(x_train, x_train)
        med = np.median(e_dists)
        eps = med / self._min_distance_factor

        clustering_method = AgglomerativeClustering(distance_threshold=eps, n_clusters=None, affinity='euclidean',
                                                    linkage='ward')
        clustering_method.fit(x_train_projected)
        cluster_labels = clustering_method.labels_

        # 3. One hot encode the cluster labels
        self._n_clusters = len(set(cluster_labels))
        cluster_encoder = OneHotEncoder()
        cluster_encoded_data = cluster_encoder.fit_transform(cluster_labels.reshape(-1, 1)).toarray()
        # print(cluster_encoded_data)

        clustering_method = AgglomerativeClustering(distance_threshold=eps, n_clusters=None, linkage='ward')
        clustering_method.fit(x_train_projected)
        self._n_clusters = len(set(clustering_method.labels_))
        cluster_labels = clustering_method.labels_

        while self._n_clusters < 50:
            eps /= 2

            clustering_method = AgglomerativeClustering(distance_threshold=eps, n_clusters=None, linkage='ward')
            clustering_method.fit(x_train_projected)
            self._n_clusters = len(set(cluster_labels))
            print("\tNew num_clusters:", self._n_clusters)
            cluster_labels = clustering_method.labels_
        '''

        # 3. One hot encode the cluster labels
        cluster_encoder = OneHotEncoder()
        cluster_encoded_data = cluster_encoder.fit_transform(cluster_labels.reshape(-1, 1)).toarray()
        # print(cluster_encoded_data)

        # 4. Get class distributions per cluster
        # If a cluster has 10 samples from class 0 and 20 samples from class 1, then create the list lcd=[10, 20]
        # self._cluster_class_distribution stores one such lcd list per cluster.
        for cluster in range(self._n_clusters):
            y_cluster_all = y_train[cluster_labels == cluster]

            lcd = [len(y_cluster_all[y_cluster_all == c]) for c in range(self._n_classes)]
            # print("Cluster:", cluster, " === Classes", y_cluster_all, " ==== ", lcd)
            self._cluster_class_distribution.append(lcd)
        # print("self._cluster_class_distribution", self._cluster_class_distribution)

        # 5. One hot encode the class labels
        class_encoder = OneHotEncoder()
        y_train = class_encoder.fit_transform(y_train.reshape(-1, 1)).toarray()

        # 6. Concatenate everything (x_train, ohe_clusters, ohe_classes)
        train_data = np.concatenate((x_train_projected, cluster_encoded_data, y_train), axis=1)
        training_data = torch.from_numpy(train_data).to(torch.float32)

        # print(training_data)
        # print("Shapes:\n\tClusters:", cluster_encoded_data.shape, "\n\tClasses:", y_train.shape,
        #      "\n\tFeatures:", x_train_projected.shape, "\n\tTraining set:", training_data.shape)

        # Determine how to draw samples from the GAN's Generator
        self._gen_samples_ratio = [int(sum(y_train[:, c])) for c in range(self._n_classes)]

        # Class specific training data
        self._samples_per_class = []
        for y in range(self._n_classes):
            x_class_data = np.array([x_train_projected[r, :] for r in range(y_train.shape[0]) if y_train[r, y] == 1])
            x_class_data = torch.from_numpy(x_class_data).to(torch.float32).to(self._device)

            self._samples_per_class.append(x_class_data)

        return training_data

    def train_batch(self, real_data):
        """
        Given a batch of input data, `train_batch` updates the Discriminator and Generator weights using the respective
        optimizers and back propagation.

        Args:
            real_data: data for cGAN training: a batch of concatenated sample vectors + one-hot-encoded class vectors.
        """

        # The loss function for GAN training - applied to both the Discriminator and Generator.
        loss_function = nn.BCELoss()

        # If the size of the batch does not allow an organization of the input vectors in packs of size self.pac_, then
        # abort silently and return without updating the model parameters.
        num_samples = real_data.shape[0]
        if num_samples % self.pac_ != 0:
            return 0, 0

        packed_samples = num_samples // self.pac_

        # DISCRIMINATOR TRAINING
        # Create fake samples from Generator
        self.D_optimizer_.zero_grad()

        # 1. Randomly take samples from a normal distribution
        # 2. Assign one-hot-encoded random classes
        # 3. Pass the fake data (samples + classes) to the Generator
        latent_x = torch.randn((num_samples, self.embedding_dim_))
        latent_classes = torch.from_numpy(np.random.randint(0, self._n_classes, num_samples)).to(torch.int64)
        latent_classes_ohe = nn.functional.one_hot(latent_classes, num_classes=self._n_classes)
        latent_clusters = torch.from_numpy(np.random.randint(0, self._n_clusters, num_samples)).to(torch.int64)
        latent_clusters_ohe = nn.functional.one_hot(latent_clusters, num_classes=self._n_clusters)
        latent_y = torch.cat((latent_clusters_ohe, latent_classes_ohe), dim=1)
        latent_data = torch.cat((latent_x, latent_y), dim=1)

        # 4. The Generator produces fake samples (their labels are 0)
        fake_x = self.G_(latent_data.to(self._device))
        fake_labels = torch.zeros((packed_samples, 1))

        # 5. The real samples (coming from the dataset) with their one-hot-encoded classes are assigned labels eq. to 1.
        real_x = real_data[:, 0:self._input_dim]
        real_y = real_data[:, self._input_dim:(self._input_dim + self._n_classes + self._n_clusters)]
        real_labels = torch.ones((packed_samples, 1))
        # print(real_x.shape, real_y.shape)

        # 6. Mix (concatenate) the fake samples (from Generator) with the real ones (from the dataset).
        all_x = torch.cat((real_x.to(self._device), fake_x))
        all_y = torch.cat((real_y, latent_y)).to(self._device)
        all_labels = torch.cat((real_labels, fake_labels)).to(self._device)
        all_data = torch.cat((all_x, all_y), dim=1)

        # 7. Reshape the data to feed it to Discriminator (num_samples, dimensionality) -> (-1, pac * dimensionality)
        # The samples are packed according to self.pac parameter.
        all_data = all_data.reshape((-1, self.pac_ * (self._input_dim + self._n_classes + self._n_clusters)))

        # 8. Pass the mixed data to the Discriminator and train the Discriminator (update its weights with backprop).
        # The loss function quantifies the Discriminator's ability to classify a real/fake sample as real/fake.
        d_predictions = self.D_(all_data)
        disc_loss = loss_function(d_predictions, all_labels)
        disc_loss.backward()
        self.D_optimizer_.step()

        # GENERATOR TRAINING
        self.G_optimizer_.zero_grad()

        latent_x = torch.randn((num_samples, self.embedding_dim_))
        latent_classes = torch.from_numpy(np.random.randint(0, self._n_classes, num_samples)).to(torch.int64)
        latent_classes_ohe = nn.functional.one_hot(latent_classes, num_classes=self._n_classes)
        latent_clusters = torch.from_numpy(np.random.randint(0, self._n_clusters, num_samples)).to(torch.int64)
        latent_clusters_ohe = nn.functional.one_hot(latent_clusters, num_classes=self._n_clusters)
        latent_y = torch.cat((latent_clusters_ohe, latent_classes_ohe), dim=1)
        latent_data = torch.cat((latent_x, latent_y), dim=1)

        fake_x = self.G_(latent_data.to(self._device))

        all_data = torch.cat((fake_x, latent_y.to(self._device)), dim=1)

        # Reshape the data to feed it to Discriminator ( (num_samples, dimensionality) -> ( -1, pac * dimensionality )
        all_data = all_data.reshape((-1, self.pac_ * (self._input_dim + self._n_classes + self._n_clusters)))

        d_predictions = self.D_(all_data)

        gen_loss = loss_function(d_predictions, real_labels.to(self._device))
        gen_loss.backward()
        self.G_optimizer_.step()

        return disc_loss, gen_loss

    def train(self, x_train, y_train):
        """
        Conventional training process of a Cluster GAN. The Generator and the Discriminator are trained
        simultaneously in the traditional adversarial fashion by optimizing `loss_function`.

        Args:
            x_train: The training data instances.
            y_train: The classes of the training data instances.
        """
        # Modify the size of the batch to align with self.pac_
        factor = self._batch_size // self.pac_
        batch_size = factor * self.pac_

        # select_prepare: implemented in BaseGenerators.py
        training_data = self.cluster_prepare(x_train, y_train)

        train_dataloader = DataLoader(training_data, batch_size=batch_size, shuffle=True)

        self.D_ = PackedDiscriminator(self.D_Arch_, input_dim=self._input_dim + self._n_classes + self._n_clusters,
                                      pac=self.pac_).to(self._device)
        self.G_ = (Generator(self.G_Arch_, input_dim=self.embedding_dim_ + self._n_classes + self._n_clusters,
                             output_dim=self._input_dim, activation=self.gen_activation_, normalize=self.batch_norm_).
                   to(self._device))

        self.D_optimizer_ = torch.optim.Adam(self.D_.parameters(),
                                             lr=self._lr, weight_decay=self._decay, betas=(0.5, 0.9))
        self.G_optimizer_ = torch.optim.Adam(self.G_.parameters(),
                                             lr=self._lr, weight_decay=self._decay, betas=(0.5, 0.9))

        disc_loss, gen_loss = 0, 0
        for epoch in range(self._epochs):
            for n, real_data in enumerate(train_dataloader):
                if real_data.shape[0] > 1:
                    disc_loss, gen_loss = self.train_batch(real_data)

                # if epoch % 10 == 0 and n >= x_train.shape[0] // batch_size:
                #    print(f"Epoch: {epoch} Loss D.: {disc_loss} Loss G.: {gen_loss}")

        return disc_loss, gen_loss

    def fit(self, x_train, y_train):
        """`fit` invokes the GAN training process. `fit` renders the CGAN class compatible with `imblearn`'s interface,
        allowing its usage in over-sampling/under-sampling pipelines.

        Args:
            x_train: The training data instances.
            y_train: The classes of the training data instances.
        """
        self.train(x_train, y_train)

    def fit_resample(self, x_train, y_train):
        """`fit_transform` invokes the GAN training process. `fit_transform` renders the CGAN class compatible with
        `imblearn`'s interface, allowing its usage in over-sampling/under-sampling pipelines.

        Args:
            x_train: The training data instances.
            y_train: The classes of the training data instances.
        """
        self.train(x_train, y_train)

        generated_data = [None for _ in range(self._n_classes)]

        majority_class = np.array(self._gen_samples_ratio).argmax()
        num_majority_samples = np.max(np.array(self._gen_samples_ratio))

        x_over_train = np.copy(x_train)
        y_over_train = np.copy(y_train)

        for cls in range(self._n_classes):
            if cls != majority_class:
                samples_to_generate = num_majority_samples - self._gen_samples_ratio[cls]

                # print("\tSampling Class y:", y, " Gen Samples ratio:", self._gen_samples_ratio[y])
                generated_data[cls] = self.sample(samples_to_generate, cls)

                min_classes = np.full(samples_to_generate, cls)

                x_over_train = np.vstack((x_over_train, generated_data[cls]))
                y_over_train = np.hstack((y_over_train, min_classes))

        return x_over_train, y_over_train

    def sample(self, num_samples, y=None):
        """ Create artificial samples using the GAN's Generator.

        Args:
            num_samples: The number of samples to generate.
            y: The class of the generated samples. If `None`, then samples with random classes are generated.

        Returns:
            Artificial data instances created by the Generator.
        """
        probabilities = np.zeros((self._n_classes, self._n_clusters))
        for clu in range(self._n_clusters):
            for cls in range(self._n_classes):
                probabilities[cls][clu] = self._cluster_class_distribution[clu][cls]/self._gen_samples_ratio[cls]
        # print(probabilities)

        if y is None:
            latent_clusters = torch.from_numpy(np.random.randint(0, self._n_clusters, num_samples)).to(torch.int64)
            latent_clusters_ohe = nn.functional.one_hot(latent_clusters, num_classes=self._n_clusters)

            latent_classes = torch.from_numpy(np.random.randint(0, self._n_classes, num_samples)).to(torch.int64)
            latent_classes_ohe = nn.functional.one_hot(latent_classes, num_classes=self._n_classes)
        else:
            # The part of the conditional vector that concerns the clusters
            mix = Categorical(torch.tensor(probabilities[y]))
            latent_clusters = mix.sample(sample_shape=torch.Size([num_samples]))
            # print("Sampling class", y, latent_clusters)
            latent_clusters_ohe = nn.functional.one_hot(
                latent_clusters, num_classes=self._n_clusters)

            # The part of the conditional vector that concerns the classes
            latent_classes_ohe = nn.functional.one_hot(
                torch.full(size=(num_samples,), fill_value=y), num_classes=self._n_classes)

        latent_y = torch.cat((latent_clusters_ohe, latent_classes_ohe), dim=1)
        latent_x = torch.randn((num_samples, self.embedding_dim_))

        # concatenate, copy to device, and pass to generator
        latent_data = torch.cat((latent_x, latent_y), dim=1).to(self._device)

        # Generate data from the model's Generator - The feature values of the generated samples fall into the range:
        # [-1,1]: if the activation function of the output layer of the Generator is nn.Tanh().
        # [0,1]: if the activation function of the output layer of the Generator is nn.Sigmoid().

        generated_samples = self.G_(latent_data).cpu().detach().numpy()
        # print("Generated Samples:\n", generated_samples)
        reconstructed_samples = self._transformer.inverse_transform(generated_samples)
        # print("Reconstructed samples\n", reconstructed_samples)
        return reconstructed_samples
