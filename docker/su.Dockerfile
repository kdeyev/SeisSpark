FROM bitnami/spark
# FROM datamechanics/spark:3.1-latest

LABEL Description="Seismic Unix on a proper Ubuntu 14.04 LTS base"

# Use /data as the persistant storage for seismic
VOLUME ["/data"]

USER root

# Download Seismic Unix, build it, and clean up tools and build artifacts
# Also try to strip down the image as much as possible by purging APT caches
RUN apt-get update && apt-get install -y \
    dos2unix \
    build-essential \
    libx11-dev \
    libxt6 libxt-dev \
    && curl -o /root/cwp_su_all_44R19.tgz -SL "https://nextcloud.seismic-unix.org/s/LZpzc8jMzbWG9BZ/download?path=%2F&files=cwp_su_all_44R19.tgz" \
    && mkdir /usr/local/cwp \
    && tar zxf /root/cwp_su_all_44R19.tgz -C /usr/local/cwp \
    && rm /root/cwp_su_all_44R19.tgz \
    && /bin/bash -c \
       'echo exit 0 > /usr/local/cwp/src/license.sh \
       && echo exit 0 > /usr/local/cwp/src/mailhome.sh \
       && echo exit 0 > /usr/local/cwp/src/chkroot.sh \
       && CWPROOT=/usr/local/cwp PATH=$PATH:/usr/local/cwp/bin make -C /usr/local/cwp/src install xtinstall' \
    && rm -rf /usr/local/cwp/src \
    && rm -rf /var/lib/apt/lists \
    && apt-get autoremove -y \
    && apt-get autoclean -y

# Add trampoline which will sett CWPROOT for each command being called
COPY trampoline.sh /usr/local/cwp/trampoline.sh
RUN dos2unix /usr/local/cwp/trampoline.sh
RUN chmod 755 /usr/local/cwp/trampoline.sh

ENV CWPROOT=/usr/local/cwp

# Symlink the trampoline script for every command in SU to /usr/local/bin
# Since /usr/local/bin is already in path, it simplifies the commands from the docker command line
#     docker run <image> segyread
# instead of
#     docker run <image> /usr/local/cwp/bin/segyread
RUN cd /usr/local/bin/ \
    && for f in /usr/local/cwp/bin/*; do \
         cp $f `basename $f`; \
         chmod 777 `basename $f`; \
         chmod +x `basename $f`; \
       done
