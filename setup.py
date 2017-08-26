from setuptools import setup
import os
from acs_redis_multi_sessions import __version__

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

packages = ['acs_redis_multi_sessions']


setup(
    name='acs_redis_multi_sessions',
    version=__version__,
    description= "Multiple Redis backends for your sessions For Django",
    long_description=read("README.md"),
    keywords='django, sessions,',
    author='Zhang Yonglei',
    author_email='zhangyonglei@aragoncs.com',
    url='https://github.com/zhangyonglei/acs_redis_multi_sessions',
    license='BSD',
    packages=packages,
    zip_safe=False,
    install_requires=['redis>=2.4.10'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
)
