#!/usr/bin/env python

PACKAGE_NAME="tornadoc"
PACKAGE_ROOT="tornadoc"
PACKAGE_URL="http://logn.info"
VERSION="0.1"
DESCRIPTION="Inline REST API documentation for Tornado handlers"
AUTHOR_NAME="Andrea Gronchi"
AUTHOR_EMAIL="neta@logn.info"
TEST_SUITE="tests"
INSTALL_REQUIRES = open("requirements.txt").readlines()
CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "License :: Other/Proprietary License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation :: CPython",
]

try:
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    pass

from setuptools import setup, find_packages
import sys, os

from setuptools.command.test import test as TestCommand
from distutils.core import Command



class CleanCommand(Command):
    description = "Clean leftovers of previous builds, tox and test runs"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        os.system("rm -fr "
                  ".eggs "
                  ".tox "
                  "build "
                  "dist "
                  ".coverage htmlcov "
                  "*.egg-info setuptools-*.egg setuptools-*.zip")
        os.system('find . -name __pycache__ '
                  '-o -name \\*.pyc '
                  '-o -name \\*.pyo '
                  '| xargs rm -fr ')


class TestCoverageCommand(Command):
    description = "Run the test suite, producing code coverage report"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system("coverage run --branch --source=%s setup.py test" % PACKAGE_ROOT)
        os.system("coverage html --directory=htmlcov")
        indexfile = os.path.join("htmlcov", "index.html")
        if os.path.isfile(indexfile):
            local_url = "file:///" + os.path.abspath(indexfile).replace("\\", "/")
            import webbrowser
            webbrowser.open(local_url)


class ToxCommand(TestCommand):
    description = "Run test suite under Tox, with all supported Python environments"
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


tests_require = []
other_commands = {
    "clean": CleanCommand,
    "coverage": TestCoverageCommand,
    "tox": ToxCommand,
}

if "coverage" in sys.argv:
    tests_require += [
        "coverage",
    ]

if "tox" in sys.argv:
    tests_require += [
        "tox",
        "setuptools",
        "virtualenv",
    ],


def namespace_packages():
    result = []
    toks = PACKAGE_ROOT.split(".")
    for i in range(1, len(toks)):
        result.append(".".join(toks[:i]))
    return result


setup(
    name            = PACKAGE_NAME,
    version         = VERSION,
    description     = DESCRIPTION,
    author          = AUTHOR_NAME,
    author_email    = AUTHOR_EMAIL,
    url             = PACKAGE_URL,
    zip_safe = False, # unnecessary; it avoids egg-as-zipfile install
    packages = find_packages(exclude=['tests']),
    namespace_packages = namespace_packages(),
    install_requires = INSTALL_REQUIRES,
    tests_require = tests_require,
    cmdclass = other_commands,
    classifiers = CLASSIFIERS,
    test_suite=TEST_SUITE,
)
