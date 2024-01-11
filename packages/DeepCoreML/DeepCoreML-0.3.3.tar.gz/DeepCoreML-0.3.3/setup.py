from distutils.core import setup
from setuptools import find_packages

DESCRIPTION = 'A collection of Machine Learning techniques for data management, engineering and augmentation.'
LONG_DESCRIPTION = '<p>DeepCoreML is a collection of Machine Learning techniques for data management, engineering, ' \
    'and augmentation. More specifically, DeepCoreML includes modules for:</p>'\
    '<ul>' \
    '<li>Dataset management</li>' \
    '<li>Text data preprocessing</li>' \
    '<li>Text representation, vectorization, embeddings</li>' \
    '<li>Dimensionality reduction</li>' \
    '<li>Generative modeling</li>' \
    '<li>Imbalanced datasets</li>' \
    '</ul>' \
    '<p><b>Licence:</b> Apache License, 2.0 (Apache-2.0)</p>' \
    '<p><b>Dependencies:</b> scikit-learn, imblearn, pytorch, numpy, pandas, transformers, nltk, matplotlib</p>'\
    '<p><b>GitHub repository:</b> '\
    '<a href="https://github.com/lakritidis/DeepCoreML">https://github.com/lakritidis/DeepCoreML</a></p>' \
    '<p><b>Publications:</b><ul>' \
    '<li>L. Akritidis, A. Fevgas, M. Alamaniotis, P. Bozanis, "Conditional Data Synthesis with Deep Generative Models '\
    'for Imbalanced Dataset Oversampling", In Proceedings of the 35th IEEE International Conference on Tools with '\
    'Artificial Intelligence (ICTAI), to appear, 2023.</li>' \
    '<li>L. Akritidis, P. Bozanis, "A Multi-Dimensional Survey on Learning from Imbalanced Data", Chapter in Machine '\
    'Learning Paradigms - Advances in Theory and Applications of Learning from Imbalanced Data, to appear, 2023.</li>' \
    '<li>L. Akritidis, P. Bozanis, "<a href="https://link.springer.com/article/10.1007/s42979-023-01913-y">' \
    'Low Dimensional Text Representations for Sentiment Analysis NLP Tasks</a>", Springer Nature (SN) Computer '\
    'Science, vol. 4, no. 5, 474, 2023.</li>' \
    '</ul></p>'

setup(
    name='DeepCoreML',
    version='0.3.3',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author="Leonidas Akritidis",
    author_email="lakritidis@ihu.gr",
    maintainer="Leonidas Akritidis",
    maintainer_email="lakritidis@ihu.gr",
    packages=find_packages(),
    package_data={'': ['generators/*']},
    url='https://github.com/lakritidis/DeepCoreML',
    install_requires=["numpy",
                      "pandas",
                      "nltk",
                      "matplotlib",
                      "seaborn",
                      "gensim",
                      "bs4",
                      "joblib",
                      "torch>=2.0.0",
                      "transformers>=4.29.0",
                      "scikit-learn>=1.0.0",
                      "imblearn>=0.0",
                      "rdt>=1.3.0,<2.0"],
    license="Apache",
    keywords=[
        "data engineering", "data management", "text vectorization", "text processing", "dimensionality reduction",
        "imbalanced data", "machine learning", "deep learning"]
)
