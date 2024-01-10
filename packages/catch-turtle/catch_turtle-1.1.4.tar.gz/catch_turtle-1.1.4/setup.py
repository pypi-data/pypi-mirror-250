import catch_turtle,os,warnings
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

try:import turtle
except ImportError:
    warnings.warn("缺少turtle模块。Module turtle required")

try:
    long_desc=open("README.rst").read()
except OSError:
    long_desc=catch_turtle.__doc__

setup(
  name='catch_turtle',
  version=catch_turtle.__version__,
  description="使用turtle模块制作的一款娱乐游戏。An entertainment game using module turtle.作者:qfcy",
  long_description=long_desc,
  author=catch_turtle.__author__,
  author_email=catch_turtle.__email__,
  url='https://github.com/qfcy/Python/tree/main/catch_turtle',
  packages=['catch_turtle'],
  keywords=["python","turtle","game","catch"],
  classifiers=["Topic :: Games/Entertainment",
               "Programming Language :: Python :: 3",
               "Natural Language :: Chinese (Simplified)",
               "Topic :: Education"]
)
