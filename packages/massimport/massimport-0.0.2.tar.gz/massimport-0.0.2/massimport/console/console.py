from time import *
import os

def wait(x):
    sleep(x)

def add(x):
    os.system(f"echo {x} >> importconfig.txt")
