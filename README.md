# SeisSpark

![Alt text](/images/pipeline_viewer.png?raw=true "Main Window")

# Getting started

1. Start Standalone container

```sh
cd docker
docker-compose build
docker-compose up
```

2. Open http://localhost:9091

# Distributed calculation

The system runs calculation using the Apache Spark framework.

# Seismic operations

The system run Seismic Unix operations wrapped py Python.
The Seismic Unix operations can be run in pipeline where the piping is build by sequence of Spark RDDs (Python pySpark).

# Web Interface

Web interface allows pipeline building and operations parameters changing.
