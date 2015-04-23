from setuptools import setup, find_packages

setup(
    name='python-bandsintown',
    version='.'.join(map(str, __import__("devserver").__version__)),
    description='Simple Python client for the Bandsintown API',
    author='Chris Forrette',
    author_email='chris@chrisforrette.com',
    url='https://github.com/jolbyandfriends/python-bandsintown'
    package=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
    license='MIT'
)
