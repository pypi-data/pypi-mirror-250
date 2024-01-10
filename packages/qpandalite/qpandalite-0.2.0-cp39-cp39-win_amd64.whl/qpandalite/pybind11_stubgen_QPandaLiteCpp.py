import os, sys
from qpandalite import QPandaLitePy

from pybind11_stubgen import ModuleStubsGenerator

module = ModuleStubsGenerator('QPandaLitePy')
module.parse()
module.write_setup_py = False