sudo apt-get update

sudo apt-get install git

sudo apt-get install mc

sudo apt-get install python-pip
sudo apt-get install python-dev


echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
sudo apt-get update
sudo apt-get install gcsfuse


sudo mkdir /mnt/gcs-bucket
sudo chmod a+w /mnt/gcs-bucket
gcsfuse black-network-149916.appspot.com /mnt/gcs-bucket

git clone https://github.com/kdeyev/SeisSpark.git



~/anaconda2/bin/pip install git+https://github.com/kdeyev/remi.git
~/anaconda2/bin/pip install py4j


export PYSPARK_PYTHON=~/anaconda2/bin/python
pyspark my_script.py 