#!/bin/sh

# how to use:
#wget https://repo.continuum.io/archive/Anaconda2-4.4.0-Linux-x86_64.sh
#chmod +x Anaconda2-4.4.0-Linux-x86_64.sh
#./Anaconda2-4.4.0-Linux-x86_64.sh
#
#gsutil cp gs://kdeyev_europe_west1/remi-master.tar.gz .
#tar xvf remi-master.tar.gz 
#
#gsutil cp gs://kdeyev_europe_west1/master.sh .
#chmod +x master.sh
#./master.sh

sudo apt-get update
sudo apt-get install git -y
sudo apt-get install mc -y
sudo apt-get install python-pip -y

#sudo apt-get install python-dev -y
#sudo apt-get install libxml2-dev libxslt1-dev python-dev -y
#sudo pip install pyshark

sudo gsutil cp gs://kdeyev_europe_west1/pyspark_k /usr/lib/spark/bin/pyspark_k
sudo chmod +x /usr/lib/spark/bin/pyspark_k

export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

sudo apt-get update
sudo apt-get install gcsfuse -y
sudo mkdir /mnt/gcs-bucket
sudo chmod a+w /mnt/gcs-bucket
gcsfuse kdeyev_europe_west1 /mnt/gcs-bucket

git clone https://github.com/kdeyev/SeisSpark.git
sudo pip install git+https://github.com/dddomodossola/remi.git

####
sudo apt-get install default-jdk -y
sudo apt-get install maven -y
git clone https://github.com/cloudera/seismichadoop.git
cd seismichadoop
mvn package
cd ~

####

# pydoop
export JAVA_HOME=/usr
sudo apt-get install python-dev -y
sudo pip install pydoop
#git clone https://github.com/crs4/pydoop.git
cd ~

# python-hadoop
git clone https://github.com/matteobertozzi/Hadoop.git
cd Hadoop/python-hadoop/
sudo python setup.py install
cd ~

# cwp
sudo gsutil cp gs://kdeyev_europe_west1/cwp.tar.gz /usr/local/bin/
cd /usr/local/bin
sudo tar xvf cwp.tar.gz 
