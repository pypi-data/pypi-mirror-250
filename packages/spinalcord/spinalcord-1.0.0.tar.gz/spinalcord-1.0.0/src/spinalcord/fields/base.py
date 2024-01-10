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


class BaseField(ABC):

    def __init__(self, column_name):
        self._column_name = column_name
        self._is_set = False

    def get_byte_length(self):
        return 1

    def get_column_name(self):
        return self._column_name

    def is_set(self):
        return self._is_set

    def toggle_is_set(self):
        self._is_set = not self._is_set

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def from_bytes(self, buffer):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def set(self, value):
        pass

    @abstractmethod
    def to_bytes(self):
        pass
