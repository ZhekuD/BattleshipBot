from setuptools import setup, find_packages

setup(
    name='ProjectToPyPI',
    version='0.0.1',
    packages=find_packages(),
    url='None',
    license='MIT',
    author='zhekud',
    author_email='zhekud@gmail.com',
    description='weather bot',
    install_requires=[
        'python-telegram-bot>=11.1.0',
    ]
)