from setuptools import find_packages, setup

setup(
    name='T-Ragx',
    packages=find_packages(),
    version='0.0.1',
    description='Translation using retrieval augmented generation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ray Liu',
    license='MIT',
)
