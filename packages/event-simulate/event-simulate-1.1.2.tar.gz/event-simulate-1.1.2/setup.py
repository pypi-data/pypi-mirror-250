import event,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

desc=event.__doc__.replace('\n','')
try:
    long_desc=event.__doc__+open("README.rst").read()
except OSError:
    long_desc=desc

setup(
  name='event-simulate',
  version=event.__version__,
  description=desc,
  long_description=long_desc,
  author=event.__author__,
  author_email=event.__email__,
  url="https://github.com/qfcy/Python/tree/main/event",
  packages=['event'],
  keywords=["event","simulate","key","mouse","click","automation","键盘","鼠标","外挂"],
  classifiers=[
      "Programming Language :: Python :: 3",
      "Natural Language :: Chinese (Simplified)",
      "Environment :: Win32 (MS Windows)",
      "Topic :: Desktop Environment :: Window Managers :: Blackbox",
      "Topic :: Desktop Environment :: Window Managers",
      "Topic :: Desktop Environment :: Window Managers :: Applets",
      "Topic :: Education",
      "Topic :: Utilities"],
)
