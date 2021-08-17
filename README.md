# SeisSpark
![Alt text](/images/main_window.jpg?raw=true "Main Window")


# Distributed calculation
The system runs calculation suing the Apache Spark framework.

# Seismic operations
The system run Seismic Unix operations wrapped py Python.
The Seismic Unix operations can be run in pipeline where the piping is build by sequence of Spark RDDs (Python pySpark).

# Web Interface
Web interface allows pipeline building and operations parameters changing. The web interface is build using remi project (Python HTTP server).
Seismic data visualisation is build using Plotly.js project (JavaScript).
