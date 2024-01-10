import os
from .ternaryOperator import ternaryOperator

def clear():
    os.system(ternaryOperator(os.name == "nt", "cls", "clear"))