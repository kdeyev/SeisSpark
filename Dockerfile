FROM centos:7

LABEL Description="Seismic Unix on a proper Ubuntu 14.04 LTS base"

# Use /data as the persistant storage for seismic
VOLUME ["/data"]

# Download Seismic Unix, build it, and clean up tools and build artifacts
# Also try to strip down the image as much as possible by purging APT caches
RUN yum install -y curl make gcc 
RUN curl -o /root/cwp_su_all_44R19.tgz -SL "https://nextcloud.seismic-unix.org/s/LZpzc8jMzbWG9BZ/download?path=%2F&files=cwp_su_all_44R19.tgz" \
    && mkdir /root/cwp \
    && tar zxf /root/cwp_su_all_44R19.tgz -C /root/cwp \
    && rm /root/cwp_su_all_44R19.tgz \
    && /bin/bash -c \
       'echo exit 0 > /root/cwp/src/license.sh \
       && echo exit 0 > /root/cwp/src/mailhome.sh \
       && echo exit 0 > /root/cwp/src/chkroot.sh \
       && CWPROOT=/root/cwp PATH=$PATH:/root/cwp/bin make -C /root/cwp/src install' \
    && rm -rf /root/cwp/src 

# Add trampoline which will sett CWPROOT for each command being called
COPY trampoline.sh /root/cwp/trampoline.sh
RUN chmod 755 /root/cwp/trampoline.sh

# Symlink the trampoline script for every command in SU to /usr/local/bin
# Since /usr/local/bin is already in path, it simplifies the commands from the docker command line
#     docker run <image> segyread
# instead of
#     docker run <image> /root/cwp/bin/segyread
RUN cd /usr/local/bin/ \
    && for f in /root/cwp/bin/*; do \
         ln -s /root/cwp/trampoline.sh `basename $f`; \
       done

ENTRYPOINT ["/bin/sh"]