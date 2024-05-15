#!/bin/sh
apt-get update
apt-get install -y libgeos-dev
pip3 install -r ${SRC_PKG}/requirements.txt -t ${SRC_PKG} && cp -r ${SRC_PKG} ${DEPLOY_PKG}
