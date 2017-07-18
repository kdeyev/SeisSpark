1. seismichadoop
	- cd seismichadoop-master
	- mvn package
2. change suhdp
	#!/bin/bash
	hadoop jar /home/cloudera/SeisSpark/seismichadoop-master/target/seismic-0.1.0-job.jar $@
3. CWP
	export CWPROOT=/home/cloudera/cwp
	cd src/
	make install
4 segy load
	./bin/suhdp load -input ~/SeisSpark/7o_5m_final_vtap.segy -output sss.sgy
5. Anaconda 
	sh Anaconda2-4.2.0-Linux-x86_64.sh
	export PYSPARK_PYTHON=/home/cloudera/anaconda2/bin/python OR use run_k.sh

6. Haddop-python
	cd python-hadoop && ~/anaconda2/bin/python setup.py install

7. pydoop
	~/anaconda2/bin/pip install pydoop




https://github.com/matteobertozzi/Hadoop
pydoop

