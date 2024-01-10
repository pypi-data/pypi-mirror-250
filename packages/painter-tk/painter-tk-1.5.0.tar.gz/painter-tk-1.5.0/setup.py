import painter,sys,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

desc=painter.__doc__.replace('\n',' ')
try:
    long_desc=open("README.rst").read()
except OSError:long_desc=''

setup(
  name='painter-tk',
  version=painter._ver,
  description=desc,
  long_description=long_desc,
  author=painter.__author__,
  author_email=painter.__email__,
  url='https://github.com/qfcy/Python/tree/main/painter',
  py_modules=['painter'],
  keywords=["simple","text","editor","notepad","tkinter"],
  classifiers=[
      'Programming Language :: Python',
      "Natural Language :: Chinese (Simplified)",
      "Topic :: Multimedia :: Graphics",
      "Topic :: Desktop Environment",
      "Topic :: Software Development :: User Interfaces"
      ],
)
