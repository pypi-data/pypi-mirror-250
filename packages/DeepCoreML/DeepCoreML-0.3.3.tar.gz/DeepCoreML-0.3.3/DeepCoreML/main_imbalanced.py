import os
import numpy as np
import sys
from imblearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# DeepCore ML imports
import DataTools
from Datasets import BaseDataset
from DataSamplers import DataSamplers
from Classifiers import Classifiers
from ResultHandler import ResultHandler

from generators.sb_gan import sbGAN
from generators.cluster_gan import clusterGAN
from generators.c_gan import cGAN
from generators.ct_gan import ctGAN
from generators.cbr import CentroidSampler, CBR

num_threads = 1
os.environ['OMP_NUM_THREADS'] = str(num_threads)

seed = 0
DataTools.set_random_states(seed)
np_random_state, torch_random_state, cuda_random_state = DataTools.get_random_states()

dataset_path = 'C:/Users/Leo/PycharmProjects/datasets/soft_defect/'
# dataset_path = 'C:/Users/Leo/PycharmProjects/datasets/imbalanced/'

imbalanced_datasets = {
    'CreditCard': {'path': dataset_path + 'creditcarddefault.csv', 'features_cols': range(1, 24), 'class_col': 24},
}

datasets = {
    'Synthetic': None,
    'AR1': {'path': dataset_path + 'ar1.csv', 'features_cols': range(0, 29), 'class_col': 29},
    # 'AR3': {'path': dataset_path + 'ar3.csv', 'features_cols': range(0, 29), 'class_col': 29},
    'AR4': {'path': dataset_path + 'ar4.csv', 'features_cols': range(0, 29), 'class_col': 29},
    'CM1': {'path': dataset_path + 'cm1.csv', 'features_cols': range(0, 21), 'class_col': 21},
    'JM1': {'path': dataset_path + 'jm1.csv', 'features_cols': range(0, 21), 'class_col': 21},
    'KC1': {'path': dataset_path + 'kc1.csv', 'features_cols': range(0, 21), 'class_col': 21},
    'KC2': {'path': dataset_path + 'kc2.csv', 'features_cols': range(0, 21), 'class_col': 21},
    'KC3': {'path': dataset_path + 'kc3.csv', 'features_cols': range(0, 39), 'class_col': 39},
    # 'MC1': {'path': dataset_path + 'mc1.csv', 'features_cols': range(0, 38), 'class_col': 38},
    'MC2': {'path': dataset_path + 'mc2.csv', 'features_cols': range(0, 39), 'class_col': 39},
    'MW1': {'path': dataset_path + 'mw1.csv', 'features_cols': range(0, 37), 'class_col': 37},
    'PC1': {'path': dataset_path + 'pc1.csv', 'features_cols': range(0, 21), 'class_col': 21},
    # 'PC2': {'path': dataset_path + 'pc2.csv', 'features_cols': range(0, 36), 'class_col': 36},
    'PC3': {'path': dataset_path + 'pc3.csv', 'features_cols': range(0, 37), 'class_col': 37},
    'PC4': {'path': dataset_path + 'pc4.csv', 'features_cols': range(0, 37), 'class_col': 37},

    'ANT-1.3': {'path': dataset_path + 'ant-1.3.csv', 'features_cols': range(0, 20), 'class_col': 20},
    # 'ANT-1.4': {'path': dataset_path + 'ant-1.4.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'ANT-1.5': {'path': dataset_path + 'ant-1.5.csv', 'features_cols': range(0, 20), 'class_col': 20},
    # 'ANT-1.6': {'path': dataset_path + 'ant-1.6.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'ANT-1.7': {'path': dataset_path + 'ant-1.7.csv', 'features_cols': range(0, 20), 'class_col': 20},
    # 'CAMEL-1.0': {'path': dataset_path + 'camel-1.0.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'CAMEL-1.2': {'path': dataset_path + 'camel-1.2.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'CAMEL-1.4': {'path': dataset_path + 'camel-1.4.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'CAMEL-1.6': {'path': dataset_path + 'camel-1.6.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'IVY-1.1': {'path': dataset_path + 'ivy-1.1.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'IVY-1.4': {'path': dataset_path + 'ivy-1.4.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'IVY-2.0': {'path': dataset_path + 'ivy-2.0.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'JEDIT-3.2': {'path': dataset_path + 'jedit-3.2.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'JEDIT-4.0': {'path': dataset_path + 'jedit-4.0.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'JEDIT-4.1': {'path': dataset_path + 'jedit-4.1.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'JEDIT-4.2': {'path': dataset_path + 'jedit-4.2.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'JEDIT-4.3': {'path': dataset_path + 'jedit-4.3.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'LOG4J-1.0': {'path': dataset_path + 'log4j-1.0.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'LOG4J-1.1': {'path': dataset_path + 'log4j-1.1.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'LOG4J-1.2': {'path': dataset_path + 'log4j-1.2.csv', 'features_cols': range(0, 20), 'class_col': 20},
    # 'LUCENE-2.0': {'path': dataset_path + 'lucene-2.0.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'LUCENE-2.2': {'path': dataset_path + 'lucene-2.2.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'LUCENE-2.4': {'path': dataset_path + 'lucene-2.4.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'POI-1.5': {'path': dataset_path + 'poi-1.5.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'POI-2.0': {'path': dataset_path + 'poi-2.0.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'POI-2.5': {'path': dataset_path + 'poi-2.5.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'POI-3.0': {'path': dataset_path + 'poi-3.0.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'SYNAPSE-1.0': {'path': dataset_path + 'synapse-1.0.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'SYNAPSE-1.1': {'path': dataset_path + 'synapse-1.1.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'SYNAPSE-1.2': {'path': dataset_path + 'synapse-1.2.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'VELOCITY-1.4': {'path': dataset_path + 'velocity-1.4.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'VELOCITY-1.5': {'path': dataset_path + 'velocity-1.5.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'VELOCITY-1.6': {'path': dataset_path + 'velocity-1.6.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'XERCES-1.2': {'path': dataset_path + 'xerces-1.2.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'XERCES-1.3': {'path': dataset_path + 'xerces-1.3.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'XERCES-1.4': {'path': dataset_path + 'xerces-1.4.csv', 'features_cols': range(0, 20), 'class_col': 20}
}

key = 'PC1'
dataset = datasets[key]

dataset_1 = BaseDataset(random_state=seed)
dataset_1.load_from_csv(path=dataset['path'], feature_cols=dataset['features_cols'], class_col=dataset['class_col'])
dataset_1.display_params()

x = dataset_1.x_
y = dataset_1.y_

classifiers = Classifiers(random_state=seed)
results_list = []

np.set_printoptions(linewidth=400, threshold=sys.maxsize)

# Create and train generators
# Use a Random Forest classifier to test the generated data quality. High accuracy reveals high quality data.
# clf = classifiers.models_[3]

# standardizer = StandardScaler()
# x_std = standardizer.fit_transform(x)
# gan = sbGAN(discriminator=(128, 128), generator=(128, 256, 128), method='knn', k=5, r=200, random_state=seed)
# gan = clusterGAN(discriminator=(128, 128), generator=(128, 256, 128), pac=1, random_state=seed)
# gan = cGAN(discriminator=(128, 128), generator=(128, 256, 128), pac=1, random_state=seed)
# gan = ctGAN(discriminator=(256, 256), generator=(128, 256, 128), pac=1)

#balanced_data = gan.fit_resample(x, y)
#print(balanced_data[0].shape)
# print(balanced_data[0])


for clf in classifiers.models_:
    DataTools.reset_random_states(np_random_state, torch_random_state, cuda_random_state)
    samplers = DataSamplers(sampling_strategy='auto', random_state=seed)

    order = 0
    print("")
    for s in samplers.over_samplers_:
        order += 1
        print("Testing", clf.name_, "with", s.name_)

        pipe_line = make_pipeline(s.sampler_, StandardScaler(), clf.model_)

        dataset_1.cv_pipeline(pipe_line, num_folds=5, num_threads=num_threads, results_list=results_list,
                              classifier_str=clf.name_, sampler_str=s.name_, order=order)

        DataTools.reset_random_states(np_random_state, torch_random_state, cuda_random_state)

print(results_list)

presenter = ResultHandler(results_list)
print(presenter.to_df(columns=['Classifier', 'Sampler', 'Accuracy_Mean', 'Balanced_Accuracy_Mean', 'F1_Mean']))
presenter.record_results(key)

'''
cs = CentroidSampler(random_state=seed)
x_bal, y_bal = cs.fit_resample(
    np.array([
        [10,1, 7], [20, 2, 3], [30, 3, 5], [10, 10, 5], [12, 13, 5], [7, 8, 9], [8,7,6], [5,3,9], [10,10,10]
    ]),
    [1, 1, 0, 0, 0, 2, 2, 2, 2])

print(x_bal.shape,y_bal.shape)
print(x_bal)
print(y_bal)
'''

'''
cbo = CBR(verbose=True, k_neighbors=1, random_state=seed)
X_reb, Y_reb = cbo.fit_resample(x, y)
print(X_reb.shape)
print(Y_reb.shape)
'''
