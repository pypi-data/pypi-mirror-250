# Copyright 2017 David R. Bild
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License

import sys
from setuptools import Extension, setup

if sys.platform == 'win32':
    libraries = ['libcryptoMD', 'libsslMD']
    import platform
    bits, _ = platform.architecture()
    if bits == '32bit':
        include_dirs = ['win_depend/openssl-1.1.0f-vs2017/include']
        library_dirs = ['win_depend/openssl-1.1.0f-vs2017/lib']
    else:
        include_dirs = ['win_depend/openssl-1.1.0f-vs2017/include64']
        library_dirs = ['win_depend/openssl-1.1.0f-vs2017/lib64']
else:
    libraries = ['crypto', 'ssl']
    include_dirs = None
    library_dirs = None

setup(name='sslpsk-w', ext_modules=[
    Extension(name='sslpsk_w._sslpsk',
              sources=['sslpsk_w/_sslpsk.c'],
              include_dirs=include_dirs,
              libraries=libraries,
              library_dirs=library_dirs)])
