from setuptools import setup

setup(
    name='fauasg',
    version='0.1.0',
    description='A set of tools developed by the Animal Speech Group at FAU',
    url='https://github.com/alexanderbarnhill/fauasg',
    author='Alexander Barnhill',
    author_email='alexander.barnhill@fau.de',
    license='MIT',
    packages=['fauasg'],
    install_requires=['torch',
                      'numpy',
                      'matplotlib',
                      'scikit-learn',
                      'lightning',
                      'scikit-image',
                      'omegaconf',
                      'opencv-python',
                      'wandb',
                      ],

    classifiers=[
    ],
)
