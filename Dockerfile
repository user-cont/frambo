# Just a base image for bots, not supposed to be run on its own.

FROM registry.fedoraproject.org/fedora:30

ENV LANG=en_US.UTF-8

RUN mkdir --mode=775 /var/log/bots

# Install requirements
COPY requirements.sh requirements.txt /tmp/frambo/
RUN cd /tmp/frambo/ && \
    bash requirements.sh && \
    dnf clean all && \
    pip3 install -r requirements.txt

# Install frambo
COPY ./ /tmp/frambo/
RUN cd /tmp/frambo && pip3 install .
