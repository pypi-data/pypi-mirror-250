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

from abc import ABC
from abc import abstractmethod

from ..utils.bytebuffer import ByteBuffer


class Model(ABC):

    def clear(self):
        # Clear fields
        for field in self.get_fields():
            field.clear()

    def from_bytes(self, bytes_):
        buffer = ByteBuffer(bytes_)
        # Set fields
        for field in self.get_fields():
            field.from_bytes(buffer)

    def get_byte_length(self):
        bytes_n = 0
        # Sum fields
        for field in self.get_fields():
            bytes_n += field.get_byte_length()
        return bytes_n

    def to_bytes(self):
        buffer = ByteBuffer()
        # Append fields
        for field in self.get_fields():
            buffer.append(field.to_bytes())
        return buffer.get()

    @abstractmethod
    def get_fields(self):
        pass
