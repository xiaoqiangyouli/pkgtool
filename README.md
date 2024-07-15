# pkgtool (Python Packaging Tool)

pkgtool offers functionality similar to the traditional python setup.py script. It supports install command and adds the benefit of installing dependencies alongside the main package. As the setup.py install is no longer recommended, this package offers an alternative to the deprecated setup.py install method.

Developed eight years ago, this package was created to address the need for packaging

1. binary only Python packages and
2. dependent libraries from local directories and archives

for deployment. Pretty much like the “virtual environments” functionalities provided by venv, but much simple. Each software package has its own independent site packages installed in their custom site package directory. 

## Install

Extract the downloaded package and run following command
```
sudo pip install .
```

## Usage

pkgtool provides two ways to install packages:

1. Run the pkgtool.runner in command line for convenient installation.
2. Write a setup script for more control over packaging.

### Command Line Runner

```
python -m pkgtool.runner install --target <TargetDirectory> --package <PackageDirectory|PackageArchive> [--setup <SetupScriptName>] [--binary]
```

| Options | Description |
|----|----|
|--target TargetDirectory | Package Install directory, default ~/.local/lib/python3.9/site-packages |
|--package PackageDirectory\|PackageArchive| PackageDirectory - Package directory containing a traditional setup.py script, pkgtool setup.py, or no setup.py <br/> PackageArchive - Package archive file (.tar.gz\|.tar.bz2\|.zip)|
|--setup <SetupScriptName> | setup script file name. In case that the package might use a different name, like package.py |
|--binary| Create bytecode-only package, source code (*.py) are removed after compilation  |

### Write a setup.py script
#### Example setup.py 

```
from pkgtool,package import PackageSetting, package

setting = PackageSetting(
    name='example',
    packages={
        'example': 'lib/python/example',
    },
    data=[
        ('relative/to/target_directory/directory1/', 'data/directory1'),
        ('/absolute/directory2/', [
            'file1',
            'directory3',
        ]),
    ],
    deps=[
        ("path/to/package/directory_no_setup_script", None),
        ("path/to/package/directory_pkgtool_setup_script", "package.py"),
        ("../third/python/download-from-web-python-master", "setup.py"),
        ("../third/python/download-from-web-python-master.tar.gz"),
        ("../third/python/download-from-web-python-master.tar.gz", "setup.py"),
    ]
)

package(
    name='Example',
    author='Your Name',
    author_email='yourname@example.com',
    version='1.0.0.0',
    url='http://www.example.com',
    setting=setting,
    binary=True,
)
```

#### PackageSetting
`PackageSetting` accept four parameters:
| Param | Description |
|-----|----------- |
name | Setting name
packages    | A dictionary mapping package names to their top-level directory. pkgtool will recursively traverse subdirectories within these packages to build the final package structure
data | Package data to be installed, list of two element tuples (DestDirectory, SourceDirectory\|[SourceFile\|SourceDirectory])
deps | Required Libraries, list of tuples (PackageDirectory\|PackageArchive, SetupScriptFileName) 

***Combine `PackageSetting`***

First define two `PackageSetting` instance

```
settingA = PackageSetting(
    name="A",
    packages={
        "A": "ilb/python/A"
    },
    data=[
        # package A data files
    ],
    deps=[
        # package A dependencies 
    ]
)

settingB = PackageSetting(
    name="B",
    packages={
        "B": "ilb/python/B"
    },
    data=[
        # package B data files
    ],
    deps=[
        # package B dependencies 
    ]
)
```
then combine
```
settingC = settingA + settingB
```
or 
```
settingA.update(settingB)
```

#### Function package()
The package() function allows you to specify package configuration, similar to how setup() works in setuptools. Here's a list of accepted parameters:

| Param | Description |
|-----|----------- |
name | Package name |
author | Author name, |
author_email | Author email |
version | Package version |
url | Package URL |
setting|`PackageSetting` instance |
binary | Create bytecode-only package, source code (*.py) are removed after compilation  |

NOTE: Only parameter `setting` and `binary` are effective.

#### Setup Script Install
To install, run the following command:
```
python setup.py install --target <TargetDirectory> [--binary]
```

| Options | Description |
|----|----|
|--target TargetDirectory | Package Install directory, default ~/.local/lib/python3.9/site-packages, where 3.9 is the installed python version |
|--binary| Create bytecode-only package, source code (*.py) are removed after compilation  |