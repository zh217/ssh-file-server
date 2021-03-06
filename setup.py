from setuptools import setup, find_packages

setup(
    name='ssh-file-server',
    version='0.1.2',
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'paramiko'
    ],
    author='Ziyang Hu',
    author_email='hu.ziyang@cantab.net',
    description='Quickly accessing remote files as if they are local',
    url='https://github.com/zh217/ssh-file-server',

)
