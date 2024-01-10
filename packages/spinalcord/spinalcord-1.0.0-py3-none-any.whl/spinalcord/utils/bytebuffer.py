# Copyright 2023 Lepta Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class ByteBuffer:

    def __init__(self, bytes_=b''):
        self._bytes = bytearray(bytes_)
        self._cursor_i = 0

    def append(self, bytes_):
        self._bytes.extend(bytes_)

    def get(self):
        return self._bytes

    def read(self, n):
        bytes_ = self._bytes[self._cursor_i:self._cursor_i + n]
        self._cursor_i += n
        return bytes_
