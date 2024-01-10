import timer,sys,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

doc=timer.__doc__.splitlines()
desc=''.join(doc[:3]) #取文档字符串的前3行

try:
    with open("README.rst") as f:
        long_desc=f.read()
except OSError:
    long_desc=None

setup(
    name='py-timer',
    version=timer.__version__,
    description=desc,
    long_description=long_desc,
    author=timer.__author__,
    author_email=timer.__email__,
    url="https://github.com/qfcy/Python/blob/main/timer.py",
    py_modules=['timer'],
    keywords=["timer","performance","analysis","计时器","性能"],
    classifiers=[
      'Programming Language :: Python',
      "Natural Language :: Chinese (Simplified)",
      "Topic :: Software Development :: Libraries :: Python Modules",
      "Topic :: Software Development :: Testing",
      "Topic :: Software Development :: Bug Tracking"],
)
