#!/usr/bin/env python
# -*- coding: utf-8 -*-
#///////////////////////////////////////////////////////////////////////////////////////////////////
# Copyright (c) 2016 Alex Li (alex.l.li@outlook.com).
# 
# Licensed under the MIT License (the "License"); you may not use this file except in compliance 
# with the License. 
# 
# You may obtain a copy of the License at https://opensource.org/license/mit.
# 
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express 
# or implied. 
# 
# See the License for the specific language governing permissions and limitations under the License.
#///////////////////////////////////////////////////////////////////////////////////////////////////
"""
Third-party libraries to be packaged

Right now, it only support .zip and .tar.gz files

DEPENDENCIES=[
        ("third/hola-1.0.0.6/", "setup.py"),                    # directory
        ("third/leveldb-0.194.tar.gz", "setup.py"),             # compressed package
        ("third/python-bloomfilter-master.zip", None),          # compressed package
        ]
"""

__copyright__ = "Copyright (c) 2016 Alex Li. All Rights Reserved."
__author__    = "Alex Li(alex.l.li@outlook.com)"
__date__      = "2016/10/23 01:19:24"

import sys
import os
import os.path
import tarfile
import zipfile
import subprocess
import shutil
import copy

from distutils.util import byte_compile

def getMajorVersion():
    return sys.version_info[0]

def extractArchive(filepath, dest_dir):
    file_base = os.path.basename(filepath)
    if tarfile.is_tarfile(filepath) and filepath.endswith('.tar.bz2'):
        gtarobj = tarfile.open(filepath, "r:bz2")
        gtarobj.extractall(dest_dir)
        gtarobj.close()

        lib_build_dir = os.path.join(dest_dir, file_base.rstrip('.tar.bz2'))
    elif tarfile.is_tarfile(filepath) and filepath.endswith('.tar.gz'):
        gtarobj = tarfile.open(filepath, "r:gz")
        gtarobj.extractall(dest_dir)
        gtarobj.close()

        lib_build_dir = os.path.join(dest_dir, file_base.rstrip('.tar.gz'))
    elif zipfile.is_zipfile(filepath):
        zipobj = zipfile.ZipFile(filepath, "r")
        zipobj.extractall(dest_dir)
        zipobj.close()

        lib_build_dir = os.path.join(dest_dir, file_base.rstrip('.zip'))
    else:
        return None

    return lib_build_dir

def pyc3to2(pyfile):
    '''python3 put pyc in a __pycache__ directory and padding a version specific tag after file
    name, to enable run pyc only packages, we need to change new-style structure back to python2
    style structure
    '''

    import importlib.util

    pycfile = importlib.util.cache_from_source(pyfile)
    if not os.path.exists(pycfile):
        return None

    ddir = os.path.dirname(pyfile)
    if not os.path.exists(ddir):
        os.mkdirs(ddir)

    dfile = pyfile + "c"
    os.rename(pycfile, dfile)


class PackageSetting(object):
    def __init__(self, name=None, packages={}, data={}, deps=[]):
        """
            packages    package setup
            data        package data
            deps        third party libraries dependent on
        """
        self._name = name
        self._packages = packages
        self._package_data = data
        self._package_deps = deps

    @property
    def name(self):
        return self._name

    @property
    def packages(self):
        return self._packages

    @property
    def data(self):
        return self._package_data

    @property
    def deps(self):
        return self._package_deps

    def __add__(self, setting):
        if not setting:
            return self

        self.update(setting.packages, setting.data, setting.deps)
        return self

    def update(self, packages={}, data={}, deps=[]):
        if packages:
            self._packages.update(packages)

        if data:
            self._package_data.update(data)

        if deps:
            self._package_deps.extend(deps)

class PackageSetup(object):
    def __init__(self, name=None, packages={}, data={}, deps=[], targetDirectory=None, buildBinary=False) -> None:
        """
            packages    package declare
            data        package data
            deps        third party libraries dependent on
        """
        self._name = name
        self._packages = packages
        self._package_data = data
        self._package_deps = deps

        self.python = "python"
        if getMajorVersion() == 3:
            self.python += "3"
        
        self.proj_home = os.getcwd()
        self.buildBinaryPackage = buildBinary

        if not targetDirectory:
            targetDirectory = os.path.join(os.environ.get("HOME"), '.local/lib/python{}.{}/site-packages/'.format(sys.version_info.major, sys.version_info.minor))

        self.installDirectory = os.path.abspath(targetDirectory)

        if os.path.isdir(self.installDirectory):
            shutil.rmtree(self.installDirectory)

        os.makedirs(self.installDirectory)

        print("Project Home: {}".format(self.proj_home))
        print("Build Install Directory: {}".format(self.installDirectory))

        # temporary directory to put package source files
        self.buildDirectory = os.path.join(self.installDirectory, "temp")
        if os.path.isdir(self.buildDirectory):
            shutil.rmtree(self.buildDirectory)

        os.makedirs(self.buildDirectory)


    def byte_compile(self, files, base=None, prefix=None):
        byte_compile(files, prefix=prefix, base_dir=base, force=True, verbose=True)

        if self.buildBinaryPackage:
            for srcfile in files:
                if not srcfile.endswith(".py"):
                    continue

                if getMajorVersion() == 3:
                    pyc3to2(srcfile)

                os.remove(srcfile)

    def parseDependency(self):
        for library in self._package_deps:
            setup_script = "setup.py"
            options = None

            if len(library) == 1:
                lib_path = library[0]
            elif len(library) == 2:
                lib_path, setup_script = library
            elif len(library) == 3:
                lib_path, setup_script, options = library
            else:
                lib_path = None

            yield lib_path, setup_script, options

    def installPackage(self, package_path, package_name=None, setup_script=None, options=None):
        lib_build_dir = None
        delete_after_build = False

        os.chdir(self.proj_home)
        if os.path.isdir(package_path):
            if not package_name:
                package_name = os.path.basename(package_path)

            # use relative path, or else byte_compile will throw an exception
            if not setup_script:
                # copy library to install directory, compile inplace
                lib_build_dir = os.path.join(self.installDirectory, package_name)
            else:
                # copy library to build directory
                lib_build_dir = os.path.join(self.buildDirectory, package_name)

            shutil.copytree(package_path, lib_build_dir)
        elif os.path.isfile(package_path):
            # extract library to build directory
            lib_build_dir = extractArchive(package_path, self.buildDirectory)

        if not os.path.isdir(lib_build_dir):
            print("Build directory not found: {}".format(lib_build_dir, file=sys.stderr))
            return False

        print("Build package: {}".format(package_path))

        if not setup_script or not os.path.exists(os.path.join(lib_build_dir, setup_script)):
            os.chdir(self.proj_home)

            sourcefile_list = []
            for root, dirs, files in os.walk(lib_build_dir):
                for name in files:
                    if name.endswith(".py"):
                        filepath = os.path.join(root, name)
                        sourcefile_list.append(filepath)
                        print("Package file: {}".format(filepath))

            os.chdir(self.proj_home)
            self.byte_compile(sourcefile_list, prefix=lib_build_dir, base=os.path.join(self.installDirectory, os.path.basename(lib_build_dir)))
            os.chdir(self.proj_home)
        else:
            subdir = os.path.dirname(setup_script)
            setup_script_base = os.path.basename(setup_script)
            os.chdir(lib_build_dir + "/" + subdir)

            print("Package Directory: " + os.getcwd())

            subprocess.check_call('echo PYTHONPATH=$PYTHONPATH', shell=True)

            cmdlist = [self.python, setup_script_base, 'install_lib']
            if options:
                cmdlist.append(options)

            retcode = subprocess.check_call(cmdlist + ['-d', self.installDirectory])
            if 0 != retcode:
                print("Install package {} failed. quit!".format(package_path), file=sys.stderr)
                return

            os.chdir(self.proj_home)

            if delete_after_build:
                print("Remove build dir ...")
                shutil.rmtree(lib_build_dir)

            if self.buildBinaryPackage:
                print("Remove source file ...")
                for root, dirs, files in os.walk(self.installDirectory):
                    for name in files:
                        srcfile = os.path.join(root, name)

                        if not name.endswith(".py"):
                            continue

                        if getMajorVersion() == 3:
                            pyc3to2(srcfile)

                        os.remove(srcfile)

    def install(self):
        for package, package_path in self._packages.items():
            self.installPackage(package_path=package_path, package_name=package)

    def installDependency(self):
        for package_path, setup_script, options in self.parseDependency():
            self.installPackage(package_path, setup_script=setup_script, options=options)

    def installPackageData(self):
        from distutils.util import convert_path

        os.chdir(self.proj_home)

        for f in self._package_data:
            # it's a tuple with path to install to and a list of files
            dir = convert_path(f[0])
            if not os.path.isabs(dir):
                dir = os.path.join(self.installDirectory, dir)

            os.makedirs(dir)

            if isinstance(f[1], list):
                for data in f[1]:
                    data = convert_path(data)
                    if os.path.isdir(data):
                        shutil.copy_tree(data, dir)
                    else:
                        shutil.copy_file(data, dir)
            elif isinstance(f[1], str) and os.path.isdir(f[1]):
                shutil.copy_tree(f[1], dir)

    def run(self):
        self.install()
        self.installPackageData()
        self.installDependency()

        shutil.rmtree(self.buildDirectory)


def package(**kwargs):
    print("Python version: {}.{}".format(sys.version_info[0], sys.version_info[1]))
    print("PYTHON={}".format(os.environ.get("PYTHONH")))
    print("PYTHONHOME={}".format(os.environ.get("PYTHONHOME")))
    print("PYTHONPATH={}".format(os.environ.get("PYTHONPATH")))
    print("HOME={}".format(os.environ.get("HOME")))
    print("PATH={}".format(os.environ.get("PATH")))
    print("PWD={}".format(os.environ.get("PWD")))

    import argparse

    parser = argparse.ArgumentParser(description="Package Install Tool")
    parser.add_argument("command", choices=["install"])
    parser.add_argument("--target", help="Target install directory")
    parser.add_argument("--binary", help="Build binary package", action="store_true", default=False)

    args = parser.parse_args()

    setting = copy.deepcopy(kwargs.get("setting", None))
    if not setting:
        print("Package setting is required", file=sys.stderr)
        return 
    
    if not args.binary:
        buildBinary = kwargs.get("binary", False)
    else:
        buildBinary = args.binary

    setup = PackageSetup(name=setting.name, 
                         packages=setting.packages, 
                         data=setting.data, 
                         deps=setting.deps, 
                         targetDirectory=args.target, 
                         buildBinary=buildBinary)
    setup.run()

    










# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
