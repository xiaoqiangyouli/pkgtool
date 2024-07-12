#!/usr/bin/env python
# -*- coding: utf-8 -*-
#///////////////////////////////////////////////////////////////////////////////////////////////////
# Copyright (c) 2017 Alex Li (alex.l.li@outlook.com).
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
   TODO: Module comments at here
   
   
"""

__copyright__ = "Copyright (c) 2017 Alex Li. All Rights Reserved."
__author__    = "Alex Li(alex.l.li@outlook.com)"
__date__      = "2017/05/13 14:31:20"



from distutils.core import setup

PACKAGES = [
    'pkgtool',
    ]

setup(name='pkgtool',
      author='Alex Li',
      author_email='alex.l.li@outlook.com',
      version='1.0.0.0',
      packages=PACKAGES,
      package_dir={'pkgtool': 'src/'},
     )


















# vim: set expandtab ts=4 sw=4 sts=4 tw=100:
