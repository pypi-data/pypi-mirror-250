#!/usr/bin/python3

import subprocess

def setup():
    subprocess.run(['chmod', '+x', 'src/fssh/setup.sh'])
    subprocess.run('./src/fssh/setup.sh')

if __name__ == '__main__':
    setup()
