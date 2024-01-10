import pycodeobject,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

try:
    long_desc=open("README.rst").read()
except OSError:
    long_desc=pycodeobject.__doc__

setup(
  name='pycodeobject',
  version=pycodeobject.__version__,
  description=pycodeobject.__doc__,
  long_description=long_desc,
  author=pycodeobject.__author__,
  author_email=pycodeobject.__email__,
  url="https://github.com/qfcy/Python/blob/main/pyobject/code_.py",
  packages=['pycodeobject'],
  keywords=["python","bytecode","字节码","assemble","pyc","uncompile","反编译"],
  classifiers=["Topic :: Software Development :: Libraries :: Python Modules",
               "Programming Language :: Python :: 3",
               "Natural Language :: Chinese (Simplified)",
               "Topic :: Software Development :: Assemblers",
               "Topic :: Software Development :: Build Tools",
               "Topic :: Software Development :: Disassemblers",
               "Topic :: Software Development :: Bug Tracking",
               "Topic :: Education"]
)
