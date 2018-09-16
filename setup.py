from setuptools import setup

setup(
    name='stochastic',
    version='0.1',
    description='Methods for lab on Stochastic Methods',
    license='MIT',
    author='Xavier Olive',
    packages=['stochastic', ],
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "cython",
        "cma",
        "vispy"
    ]
)
