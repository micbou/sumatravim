import codecs
import os
import re
from setuptools import setup, find_packages


def read(*parts):
    """
    Build an absolute path from *parts* and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), 'rb', 'utf-8') as f:
        return f.read()


def find_version(*file_paths):
    """
    Build a path from *file_paths* and search for a ``__version__``
    string inside.
    """
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


setup(
    name='sumatravim',
    version=find_version('sumatravim', '__init__.py'),
    description='SumatraPDF wrapper for Vim and LaTeX.',
    long_description=read('README.rst'),
    url='http://github.com/micbou/sumatravim/',
    license='MIT',
    author='micbou',
    author_email='contact@micbou.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sumatravim = sumatravim.__main__:Main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Multimedia :: Graphics :: Viewers',
        'Topic :: Text Editors',
        'Topic :: Text Processing :: Markup :: LaTeX',
    ],
)
