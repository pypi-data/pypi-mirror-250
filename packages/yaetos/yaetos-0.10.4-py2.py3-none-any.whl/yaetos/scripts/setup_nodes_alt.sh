#!/bin/bash
# Script to configure all nodes on EMR cluster. (Setup as part of a boostrap operation in AWS)
# OBSOLETE, was required by spark 2.4


# Installs below are specific to python version, which is specific to EMR version. TODO: make it independant. Will be fixed when using to emr-6.x since python3 will be default and it will support pip3.
sudo pip-3.6 install boto3==1.9.57
sudo pip-3.6 install networkx==2.4
sudo pip-3.6 install numpy==1.18.5  # need to force this version instead of latest (1.19.2) to be compatible with koalas 1.3.0 (requiring <1.19)
sudo pip-3.6 install pandas==1.0.0  # downgraded from 1.0.4 to be compatible with koalas. 0.25.1
sudo pip-3.6 install sqlalchemy==1.3.15  # don't use 1.3.17 since not compatible with sqlalchemy-redshift (0.7.7). See if it is still a pb at https://github.com/sqlalchemy-redshift/sqlalchemy-redshift/issues/195
# TODO: reuse "requirement.txt" libs but just the part that need to run on the cluster side
