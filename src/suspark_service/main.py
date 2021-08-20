# =============================================================================
# <copyright>
# Copyright (c) 2021 Bluware Inc. All rights reserved.
#
# All rights are reserved. Reproduction or transmission in whole or in part, in
# any form or by any means, electronic, mechanical or otherwise, is prohibited
# without the prior written permission of the copyright owner.
# </copyright>
# =============================================================================


import configargparse
import uvicorn
from fastapi import FastAPI

import suspark_service.routers.modules as modules
import suspark_service.routers.pipelines as pipelines
from suspark.pipeline_repository import PiplineRepository
from suspark.suspark_context import SusparkContext
from suspark.suspark_modules_factory import ModulesFactory, register_module_types

defaults = {"port": 9091}

p = configargparse.ArgParser()
p.add("-c", "--config-file", is_config_file=True, help="config file path")
p.add("--port", type=int)
p.add("--allow-remote", action="store_true")

p.set_defaults(**defaults)
options = p.parse_args()


app = FastAPI()
modules_factory = ModulesFactory()
suspark_context = SusparkContext()
pipeline_repository = PiplineRepository(suspark_context=suspark_context, modules_factory=modules_factory)
register_module_types(modules_factory)

if options.allow_remote:
    host = "0.0.0.0"
else:
    host = "127.0.0.1"


# @app.on_event("startup")
# async def startup() -> None:
#     await db_handler.connect()

app.include_router(pipelines.init_router(pipeline_repository=pipeline_repository))
app.include_router(modules.init_router(modules_factory=modules_factory))

uvicorn.run(app, host=host, port=options.port)
