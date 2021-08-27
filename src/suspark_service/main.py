import os

import configargparse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from suspark.pipeline_repository import PiplineRepository
from suspark.suspark_context import SusparkContext
from suspark.suspark_modules_factory import ModulesFactory
from suspark_modules.suspark_test_modules import register_test_modules
from suspark_service.default_pipeline import create_default_pipeline
from suspark_service.suspark_service_app import create_suspark_service_app

os.environ["PYTHONHASHSEED"] = str(232)

from fastapi.staticfiles import StaticFiles

defaults = {"port": 9091}

p = configargparse.ArgParser()
p.add("-c", "--config-file", is_config_file=True, help="config file path")
p.add("--port", type=int)
p.add("--allow-remote", action="store_true")

p.set_defaults(**defaults)
options = p.parse_args()

modules_factory = ModulesFactory()
register_test_modules(modules_factory)

suspark_context = SusparkContext()
pipeline_repository = PiplineRepository(suspark_context=suspark_context, modules_factory=modules_factory)
create_default_pipeline(pipeline_repository)
app = create_suspark_service_app(modules_factory=modules_factory, pipeline_repository=pipeline_repository)

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


uvicorn.run(app, host=host, port=options.port)
