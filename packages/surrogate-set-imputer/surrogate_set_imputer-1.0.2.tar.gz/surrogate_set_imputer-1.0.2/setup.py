from setuptools import setup
from surrogate_set_imputer.surrogate_set_imputer import SurrogateSetImputer

setup(
    name='surrogate_set_imputer',
    version=SurrogateSetImputer.__version__,
    description='Surrogate Set Imputer is a method for imputing continuous feature values.',
    long_description='Surrogate Set Imputer is an inherently interpretable feature value imputation method. The preprint for the article that this library is based off can be found at: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4640047.',
    url='https://github.com/jamie-duell/surrogate_set_imputer',
    author='Jamie Duell',
    author_email='853435@swansea.ac.uk',
    packages=['surrogate_set_imputer'],
    install_requires=['numpy', 'scipy', 'scikit-learn', 'matplotlib'],
)