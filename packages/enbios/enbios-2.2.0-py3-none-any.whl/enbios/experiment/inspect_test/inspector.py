import inspect
import sys
from importlib import import_module

from enbios.experiment.inspect_test.theABC import EnbiosAdapter

sys.path.insert(0,"/home/ra/projects/enbios/enbios/experiment/inspect_test")
adapter_module = import_module("baseA")

for cl in inspect.getmembers(adapter_module, inspect.isclass):
    # check if cl is subclass of EnbiosAdapter
    if cl[1].__bases__[0].__name__ == EnbiosAdapter.__name__:
        print("ok")
    # instance an object with some config-dict
    obj = cl[1]()
