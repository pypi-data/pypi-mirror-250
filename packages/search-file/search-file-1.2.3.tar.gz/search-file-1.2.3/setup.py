import search_file,sys,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

desc="""A python module that supplies tools to search files(or directories).一个用于搜索文件或文件夹的Python模块。"""

try:
    with open("README.rst") as f:
        long_desc=f.read()
except OSError:
    long_desc=None

setup(
  name='search-file',
  version=search_file.__version__,
  description=desc,
  long_description=long_desc,
  author=search_file.__author__,
  author_email=search_file.__email__,
  packages=['search_file'], #这里是代码所在的文件名称
  keywords=["path","search","file","directories","automation"],
  classifiers=[
      "Programming Language :: Python",
      "Topic :: System :: Filesystems",
      "Topic :: Software Development :: Libraries",
      "Natural Language :: Chinese (Simplified)"]
)
