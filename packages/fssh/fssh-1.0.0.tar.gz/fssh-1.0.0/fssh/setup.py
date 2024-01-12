#!/usr/bin/python3

import subprocess

def setup():
    subprocess.run(['chmod', '+x', 'fssh/setup.sh'])
    subprocess.run('./fssh/setup.sh')

if __name__ == '__main__':
    setup()
