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
import os

import configargparse
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from seisspark.pipeline_repository import PiplineRepository
from seisspark.seisspark_context import SeisSparkContext
from seisspark.seisspark_modules_factory import ModulesFactory
from seisspark_modules.seisspark_test_modules import register_test_modules
from seisspark_service.default_pipeline import create_default_pipeline
from seisspark_service.seisspark_service_app import create_seisspark_service_app

os.environ["PYTHONHASHSEED"] = str(232)


def use_route_names_as_operation_id(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


defaults = {"port": 9091, "allow_remote": True}

p = configargparse.ArgParser()
p.add("-c", "--config-file", is_config_file=True, help="config file path")
p.add("--port", type=int)
p.add("--allow-remote", action="store_true")

p.set_defaults(**defaults)
options = p.parse_args()

modules_factory = ModulesFactory()
register_test_modules(modules_factory)

seisspark_context = SeisSparkContext()
pipeline_repository = PiplineRepository(seisspark_context=seisspark_context, modules_factory=modules_factory)
create_default_pipeline(pipeline_repository)
app = create_seisspark_service_app(modules_factory=modules_factory, pipeline_repository=pipeline_repository)

app.mount("/", StaticFiles(directory="src/ui/build", html=True), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if options.allow_remote:
    host = "0.0.0.0"
else:
    host = "127.0.0.1"

use_route_names_as_operation_id(app)

uvicorn.run(app, host=host, port=options.port)
