- [SeisSpark](#seisspark)
  - [Spark](#spark)
  - [Seismic Unix (aka SU)](#seismic-unix-aka-su)
- [Architecture](#architecture)
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

# Architecture

SeisSpark deployment consist of two major components:
- SeisSpark service
- Apache Spark cluster


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
