#!/usr/bin/python3

import subprocess
import os

def setup():
    path = os.path.abspath(__file__)
    script_path = f'{path[:len(path) - 2]}sh'
    subprocess.run(['chmod', '+x', script_path])
    subprocess.run(script_path)

if __name__ == '__main__':
    setup()
