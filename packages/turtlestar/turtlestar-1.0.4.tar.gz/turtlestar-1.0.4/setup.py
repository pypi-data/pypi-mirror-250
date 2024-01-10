import turtlestar,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

desc="使用turtle模块画出动态星空的程序, 类似Windows内置的星空屏保。A program uses module turtle to draw dynamic stars, being similar to the built-in starry screen saver in Windows."
try:
    long_desc=open("README.rst").read()
except OSError:
    long_desc=desc

setup(
  name='turtlestar',
  version=turtlestar.__version__,
  description=desc,
  long_description=long_desc,
  author=turtlestar.__author__,
  author_email=turtlestar.__email__,
  url="https://github.com/qfcy/Python/blob/main/turtle/%E6%98%9F%E7%A9%BA.py",
  py_modules=['turtlestar'],
  keywords=["turtle","star","turtlestar","graphics"],
  classifiers=[
      'Programming Language :: Python',
      "Natural Language :: Chinese (Simplified)",
      "Topic :: Multimedia :: Graphics"],
)
