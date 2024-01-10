import pyobject,os
from setuptools import setup,Extension

try:os.chdir(os.path.split(__file__)[0])
except:pass

try:
    long_desc=open("README.rst").read()
except OSError:
    long_desc=pyobject.__doc__

setup(
    name='pyobject',
    version=pyobject.__version__,
    description=pyobject.__doc__.replace('\n',''),
    long_description=long_desc,
    author=pyobject.__author__,
    author_email=pyobject.__email__,
    url="https://github.com/qfcy/Python/tree/main/pyobject",
    packages=['pyobject'],
    ext_modules=[Extension(
        "pyobj_extension",["pyobject\\pyobj_extension.c"]
    )],
    keywords=["pyobject","python","object","util",
        "对象","bytecode","字节码","面向对象编程"
    ],
    classifiers=[
      'Programming Language :: Python',
      "Natural Language :: Chinese (Simplified)",
      "Topic :: Utilities",
      "Topic :: Software Development :: Libraries :: Python Modules"],
)
