#!/bin/sh
#///////////////////////////////////////////////////////////////////////////////////////////////////
# Copyright (c) 2018 Alex Li (alex.l.li@outlook.com).
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
#
# File: build.sh
# Author: Alex Li(alex.l.li@outlook.com)
# Date: 2018/03/16 00:42:12
#///////////////////////////////////////////////////////////////////////////////////////////////////
PKGTOOL_HOME=$(cd $(dirname $0); echo $PWD)

BUILD_DIR=build
OUTPUT_DIR=$PKGTOOL_HOME/output

[ -d ${OUTPUT_DIR} ] || mkdir -p ${OUTPUT_DIR}

unset PYTHONHOME PYTHONPATH
#/usr/bin/python3 setup.py sdist --force-manifest --dist-dir ${OUTPUT_DIR}
/usr/bin/python3 setup.py sdist --dist-dir ${OUTPUT_DIR}

if [ -d "${BUILD_DIR}" ]; then
    rm -rf ${BUILD_DIR}
fi























# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
