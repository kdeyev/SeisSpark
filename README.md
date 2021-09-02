- [SeisSpark](#seisspark)
  - [Spark](#spark)
  - [Seismic Unix (aka SU)](#seismic-unix-aka-su)
  - [SeisSpark pipeline](#seisspark-pipeline)
    - [SeisSpark module](#seisspark-module)
    - [SeisSpark data model](#seisspark-data-model)
    - [SeisSpark's RDD](#seissparks-rdd)
- [Architecture](#architecture)
  - [SeisSpark service](#seisspark-service)
- [API docs](#api-docs)
- [Implementation details](#implementation-details)
- [Getting started](#getting-started)
- [Web UI](#web-ui)

# SeisSpark

This project is targeting to experiment for Apache Spark utilization for seismic data processing needs.
The longer-term target is running heavy seismic data imaging pipelines on big-scaled resources and providing the result in "real-time".

## Spark

```
"Apache Spark is a unified analytics engine for large-scale data processing."
```

The main idea of the SeisSpark project is the representation of the seismic data processing graph as DAG of [RDD](https://spark.apache.org/docs/3.0.0/rdd-programming-guide.html) operations in Apache Spark.
The seismic data can is represented as key-value RDD, where the key is the gather id and value is the gather data.

## Seismic Unix (aka SU)

The [wiki page](https://wiki.seismic-unix.org/doku.php) says:
```
"Seismic Un*x is an open source seismic processing package."
```
SeisSpark is actively using [SU commands](https://wiki.seismic-unix.org/tutorials:first_steps) for running the actual data transformation. Also, SeisSpark uses the [SU data format](https://wiki.seismic-unix.org/sudoc:su_data_format) internally.

Additional information regarding the SU can be found in the [SU documentation](https://web.mit.edu/cwpsu_v44r1/sumanual_600dpi_letter.pdf
) or in the [SU GitHub repo](https://github.com/JohnWStockwellJr/SeisUnix).

The SU programs are invoked as subprocesses and all the data transferring is done via stdin and stdout. Practically it means that Spark Worker nodes need to have the SU package installed.

## SeisSpark pipeline

SeisSpark pipeline is a chain of SU programs wrapped by Python and executed in Spark. The translation of the SeisSpark pipeline into Spark RDD is done by the SeisSpark service. Currently, only sequential chains are supported, but there are plans to extend SeisSpark for DAG support.

### SeisSpark module
SeisSpark module is the node in SeisSpark pipeline. Each SeisSpark module is translated to at least one Spark transformation. Most of the SeisSpark modules are using SU programs for data transformation, but several of the modules are implemented directly with pyspark for performance needs.
Each module describes its own parameters schema (JSON Schema was used), and parameters can be modified which is supposed to modify the module results.

### SeisSpark data model

SeisSpark uses Spark's RDDs for the representation of the data state at each step of the pipeline. To say it simpler each SeisSpark module receives an RDD and produces another one, each RDD is a list of key-value pairs.

### SeisSpark's RDD

SeisSpark's RDD value is a list of seismic traces. SeisSpark's RDD key is a gather id (or ensemble id). In most cases, the key is a trace header value, common in the list of traces.

# Architecture

SeisSpark deployment consist of two major components:
- SeisSpark service
- Apache Spark cluster

## SeisSpark service

SeisSpark service is HTTP (mostly RESTful) service, which allows the building and management o SeisSpark pipelines.

# API docs

[FastAPI client documentation](src/seisspark_client/README.md)

# Implementation details

TODO


# Getting started

1. Start Standalone container

```sh
cd docker
docker-compose build
docker-compose up
```

2. Open http://localhost:9091

![Alt text](/images/pipeline_viewer.png?raw=true "Main Window")

# Web UI

TODO
