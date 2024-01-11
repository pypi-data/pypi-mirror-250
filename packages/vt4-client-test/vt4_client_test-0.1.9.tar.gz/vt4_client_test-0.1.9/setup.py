from setuptools import setup, find_packages

setup(
    name='vt4_client_test',
    version='0.1.9',
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    install_requires=[],
    author='Adam Drag',
    description='Python client for the CalcTree API',
    url='https://github.com/adam-drag/calctree-client',
)
