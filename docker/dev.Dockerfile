FROM seisspark

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8



WORKDIR /root
RUN apt-get update && apt-get install -y git
RUN pip install pipenv
RUN git clone --branch refactroring  https://github.com/kdeyev/SeisSpark.git
WORKDIR /root/SeisSpark
ENV PIPENV_VENV_IN_PROJECT=1
RUN pipenv install --dev

WORKDIR /root/SeisSpark/src/ui
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install -y yarn
RUN yarn install --ignore-engines && yarn build

WORKDIR /root/SeisSpark
ENV PYTHONPATH=/root/SeisSpark/src
# ENV PATH=/root/SeisSpark/src

COPY start_dev.sh /root/start_dev.sh
RUN dos2unix  /root/start_dev.sh
RUN chmod 755  /root/start_dev.sh

ENTRYPOINT ["/bin/sh"]
CMD [ "/root/start_dev.sh" ]
