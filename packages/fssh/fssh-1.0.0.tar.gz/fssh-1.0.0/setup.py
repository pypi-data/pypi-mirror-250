from setuptools import setup

with open('requirements.txt') as rf:
    reqs = rf.read().splitlines()

setup(
    name = 'fssh',
    version = '1.0.0',
    description = 'Fash SSH for UTCS students',
    url = 'https://github.com/migopp/fssh/',
    author = 'Michael Goppert',
    author_email = 'goppert@cs.utexas.edu',
    license = 'MIT',
    packages = ['fssh'],
    install_requires = reqs,
    entry_points = {
        'console_scripts': {
            'fssh = fssh.__main__:fssh',
            'fssh-setup = fssh.setup:setup'
        }
    }
)
