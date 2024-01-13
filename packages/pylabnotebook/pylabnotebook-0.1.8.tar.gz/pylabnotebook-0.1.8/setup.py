import subprocess
import re
from setuptools import setup, find_packages
from setuptools.command.install import install
from pylabnotebook import __version__
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

GIT_VERSION = '2.40.1'
class PostInstallCommand(install):

    def get_git_version(self):
        try:
            git_version_output = subprocess.check_output(['git', '--version'], text=True)
            match = re.search(r'(\d+\.\d+\.\d+)', git_version_output)
            if match:
                return match.group(1)
            else:
                return None
        except subprocess.CalledProcessError:
            red = '\033[0;31m'
            raise SystemExit(f"{red}Git is not installed. Please install Git version >= 2.40.1 on your system.")
        
    def compare_git_version(self, target_version):
        git_version = self.get_git_version()
        if git_version:
            return tuple(map(int, git_version.split('.'))) >= tuple(map(int, target_version.split('.')))
        else:
            return None

    def run(self):
        if self.compare_git_version(GIT_VERSION):
            install.run(self)
        else:
            red = '\033[0;31m'
            raise SystemExit(f"{red}Git version required is >= 2.40.1. Please install a valid git version.")

setup(
    name='pylabnotebook',
    version=__version__,
    description="This package provides functions to write an automated labnotebook using git.",
    long_description=long_description,
    long_description_content_type='text/markdown',

    author="Matteo Miotto",
    author_email="miotsdata@gmail.com",
    
    packages=find_packages(),
    package_data={'labnotebook': ['templates/*']},
    entry_points={
        'console_scripts': [
            'labnotebook = pylabnotebook.main:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    python_requires='>=3.7',
    install_requires=[
        "argparse",
    ],
)
