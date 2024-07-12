#///////////////////////////////////////////////////////////////////////////////////////////////////
# Copyright (c) 2024 Alex Li (alex.l.li@outlook.com).
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
import sys
import argparse

from pkgtool.package import PackageSetup


def mainloop():
    parser = argparse.ArgumentParser(description="Package Install Tool")
    parser.add_argument("command", choices=["install"])
    parser.add_argument("--target", help="Target install directory")
    parser.add_argument("--package", help="Package")
    parser.add_argument("--setup", help="Package", default="setup.py")
    parser.add_argument("--binary", help="Build binary package", action="store_true", default=False)

    args = parser.parse_args()

    setup = PackageSetup(targetDirectory=args.target, buildBinary=args.binary)
    setup.installPackage(args.package, setup_script=args.setup)