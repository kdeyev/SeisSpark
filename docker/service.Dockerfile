FROM seisspark

WORKDIR $SEISSPARK_HOME
ADD docker/service_requirements.txt .
RUN python -m pip install --upgrade pip && python -m pip install --quiet -r service_requirements.txt && rm -rf service_requirements.txt

WORKDIR $SEISSPARK_HOME/src/ui
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install -y yarn
RUN yarn install --ignore-engines && yarn build && rm -rf node_modules

WORKDIR $SEISSPARK_HOME

COPY docker/start_standalone.sh /root/start_standalone.sh
RUN dos2unix  /root/start_standalone.sh
RUN chmod 755  /root/start_standalone.sh

COPY docker/start_service.sh /root/start_service.sh
RUN dos2unix  /root/start_service.sh
RUN chmod 755  /root/start_service.sh

ENTRYPOINT ["/bin/sh"]
CMD [ "/root/start_service.sh" ]
