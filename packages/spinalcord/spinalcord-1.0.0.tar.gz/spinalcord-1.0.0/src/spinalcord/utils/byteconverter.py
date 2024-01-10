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

import struct


class ByteConverter:

    @staticmethod
    def from_boolean(value):
        return struct.pack("?", value)

    @staticmethod
    def from_double(value):
        return struct.pack("<d", value)

    @staticmethod
    def from_int32(value):
        return struct.pack("<i", value)

    @staticmethod
    def from_uint16(value):
        return struct.pack("<H", value)

    @staticmethod
    def to_boolean(bytes_):
        return struct.unpack("?", bytes_)[0]

    @staticmethod
    def to_double(bytes_):
        return struct.unpack("<d", bytes_)[0]

    @staticmethod
    def to_int32(bytes_):
        return struct.unpack("<i", bytes_)[0]

    @staticmethod
    def to_uint16(bytes_):
        return struct.unpack("<H", bytes_)[0]
