from distutils.core import setup
import sys
import io

NAME = 'domaininformation'
VERSION = '1.0.8'
AUTHOR = 'neu5ron'
AUTHOR_EMAIL = 'therealneu5ron AT gmail DOT com'
DESCRIPTION = "Combine information about a domain in JSON format"
URL = "https://github.com/neu5ron/domaininformation"
DOWNLOAD_URL = "https://github.com/neu5ron/domaininformation/tarball/master"

LONG_DESCRIPTION = '\n\n'.join([io.open('README.md', 'r',
                                        encoding='utf-8').read(),
                                io.open('CHANGES.md', 'r',
                                        encoding='utf-8').read()])


PACKAGES = ['domaininformation']


INSTALL_REQUIRES = []


if sys.version_info >= (3,):
    print 'Requires python 2.7'
    sys.exit(1)
else:
    INSTALL_REQUIRES.append("requests[security]")
    INSTALL_REQUIRES.append("dateutils")

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    download_url=DOWNLOAD_URL,
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES
)