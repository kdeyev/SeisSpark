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
RUN yarn install --ignore-engines && yarn build

WORKDIR /root/SeisSpark
ENV PYTHONPATH=/root/SeisSpark/src
# ENV PATH=/root/SeisSpark/src

COPY bootstrap.sh /root/bootstrap.sh
RUN dos2unix /root/bootstrap.sh
RUN chmod 755 /root/bootstrap.sh

ENTRYPOINT ["/bin/sh"]
CMD [ "/root/bootstrap.sh" ]
