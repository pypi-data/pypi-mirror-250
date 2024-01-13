from setuptools import setup, find_packages

setup(
    name='cromdf',
    version='0.1.4',
    author='Hiromuabe',
    author_email='s2122072@stu.musashino-u.ac.jp',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    url='https://github.com/Hiromuabe/cromdf',
    license='MIT',
    description='An utility for fusing data across different modalities like text and image',
    long_description=open('README.md').read(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'torch',
        'torchvision',
        'torchaudio'
    ],
)
