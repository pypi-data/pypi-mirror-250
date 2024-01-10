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

from .base import BaseField
from ..utils.bytebuffer import ByteBuffer
from ..utils.byteconverter import ByteConverter
from ..exceptions import FieldNotSetException


class Int32Field(BaseField):

    def __init__(self, column_name):
        super().__init__(column_name)
        self._value = None

    def get_byte_length(self):
        return super().get_byte_length() + 4 if self.is_set() else super().get_byte_length()

    def clear(self):
        if self.is_set():
            self.toggle_is_set()

    def from_bytes(self, buffer):
        if ByteConverter.to_boolean(buffer.read(1)):
            self.set(ByteConverter.to_int32(buffer.read(4)))

    def get(self):
        if not self.is_set():
            raise FieldNotSetException
        return self._value

    def set(self, value):
        self._value = value
        if not self.is_set():
            self.toggle_is_set()

    def to_bytes(self):
        buffer = ByteBuffer()
        buffer.append(ByteConverter.from_boolean(self.is_set()))
        try:
            buffer.append(ByteConverter.from_int32(self.get()))
        except FieldNotSetException:
            pass
        return buffer.get()
