FROM su

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /root
ENV SEISSPARK_HOME=/root/SeisSpark
RUN apt-get update && apt-get install -y git
RUN pip install pipenv
RUN git clone https://github.com/kdeyev/SeisSpark.git
WORKDIR $SEISSPARK_HOME
ENV PIPENV_VENV_IN_PROJECT=1
RUN pipenv install --dev

WORKDIR $SEISSPARK_HOME/src/ui
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install -y yarn
RUN yarn install --ignore-engines && yarn build

WORKDIR $SEISSPARK_HOME
ENV PYTHONPATH=$SEISSPARK_HOME/src

COPY start_dev.sh /root/start_dev.sh
RUN dos2unix  /root/start_dev.sh
RUN chmod 755  /root/start_dev.sh

ENTRYPOINT ["/bin/sh"]
CMD [ "/root/start_dev.sh" ]

