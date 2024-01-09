"""Optimal control MPC tools for Python."""
import sys

from setuptools import find_packages, setup

import versioneer

DOCLINES = __doc__.split("\n")

CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Science/Research
Intended Audience :: Information Technology
License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)
Programming Language :: Other
Topic :: Scientific/Engineering :: GIS
Topic :: Scientific/Engineering :: Mathematics
Topic :: Scientific/Engineering :: Physics
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""

# TODO: Remove when support for python_requires is standard.
if sys.version_info < (3, 8):
    sys.exit("Sorry, Python 3.8 or newer is required.")

setup(
    name='mesido',
    version=versioneer.get_version(),
    description=DOCLINES[0],
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
    url='https://pymoca.com/',
    author='Jack Vreeken',
    maintainer='Jack Vreeken',
    license='LGPLv3',
    keywords='mesibo optimization optimal control',
    platforms=['Windows', 'Linux', 'Mac OS-X', 'Unix'],
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[],
    python_requires='>=3.8',
    cmdclass=versioneer.get_cmdclass(),
)
