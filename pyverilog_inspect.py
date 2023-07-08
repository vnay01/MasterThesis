import pyverilog
import inspect
 
import os
import subprocess
from subprocess import call

input_string = inspect.getfile(pyverilog).strip('__init__.py')
print(input_string)

