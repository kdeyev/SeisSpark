FROM su

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN mkdir /root/SeisSpark
ENV SEISSPARK_HOME=/root/SeisSpark
ADD src $SEISSPARK_HOME/src

ADD docker/requirements.txt .
RUN python -m pip install --upgrade pip && python -m pip install --quiet -r requirements.txt && rm -rf requirements.txt

WORKDIR $SEISSPARK_HOME
ENV PYTHONPATH=$SEISSPARK_HOME/src