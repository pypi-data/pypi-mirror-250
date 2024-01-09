#
# Copyright (C) 2022 Vaticle
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from typedb.common.exception import TypeDBDriverException


T = TypeVar("T")


class NativeWrapper(ABC, Generic[T]):

    def __init__(self, native_object: T):
        self._native_object = native_object

    @property
    @abstractmethod
    def _native_object_not_owned_exception(self) -> TypeDBDriverException:
        pass

    @property
    def native_object(self) -> Any:
        if not self._native_object.thisown:
            raise self._native_object_not_owned_exception
        return self._native_object
