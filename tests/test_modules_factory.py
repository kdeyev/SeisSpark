# =============================================================================
# Copyright (c) 2021 SeisSpark (https://github.com/kdeyev/SeisSpark).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
import pytest

from seisspark.seisspark_modules_factory import ModulesFactory
from seisspark_modules.sufilter import SUfilter
from seisspark_modules.suimp2d import SUimp2d


def test_modules_factory() -> None:
    factory = ModulesFactory()
    factory.register_module_type("SUfilter", SUfilter)
    factory.register_module_type("SUimp2d", SUimp2d)

    with pytest.raises(KeyError):
        factory.register_module_type("SUfilter", SUfilter)

    with pytest.raises(Exception):
        factory.register_module_type("SU filter", SUfilter)

    assert factory.get_module_types() == ["SUfilter", "SUimp2d"]
