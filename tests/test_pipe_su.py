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
from su_data.su_pipe import su_process_pipe


def test_run_su_processes() -> None:
    output_buffers = su_process_pipe(["suplane"], [])

    output_buffers = su_process_pipe(["sufilter", "f1=10,f2=20,f3=30,f4-40"], output_buffers)

    for buffer in output_buffers:
        print(buffer)
