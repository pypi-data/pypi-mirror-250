import music_score,sys,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

desc="""A program that using re module to analyze music score (simplified score).
使用re模块解析曲谱(简谱)的程序。"""

try:
    long_desc=open("README.rst").read()
except OSError:
    long_desc=None

setup(
  name='music-score',
  version=music_score.__version__,
  description=desc,
  long_description=long_desc,
  author=music_score.__author__,
  author_email=music_score.__email__,
  url="https://github.com/qfcy/Python/blob/main/music.py",
  py_modules=['music_score'], #这里是代码所在的文件名称
  keywords=["music","music score","song","winsound","声音"],
  classifiers=[
      'Programming Language :: Python',
      "Topic :: Multimedia :: Sound/Audio",
      "Natural Language :: Chinese (Simplified)"],
  install_requires=["console-tool","py-timer"]
)
