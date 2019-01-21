#!/bin/bash

set -ex

# for debugging purposes: iputils (ping), redis (redis-cli)
# for bots: krb5-workstation, nss_wrapper
dnf install -y --nodocs gcc rpm-devel openssl-devel libxml2-devel redhat-rpm-config make git \
                        iputils redis krb5-workstation nss_wrapper \
                        python3-devel python3-pyOpenSSL

dnf clean all
