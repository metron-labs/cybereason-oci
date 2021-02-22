#!/bin/bash
cd /tmp
wget https://objectstorage.us-ashburn-1.oraclecloud.com/p/oeaz8ub-TfAsIu9_X13Czg3pc1xF36HIey_VfCAu5mDwZiG3X21w6v9NZu1vWjhG/n/orasenatdpltsecitom01/b/Hammer/o/cybereason-sensor-20.1.289.0-1.x86_64_integration_integration-r.cybereason.net_443_ACTIVE_NORMAL_rpm.rpm
rpm -i cybereason-sensor-20.1.289.0-1.x86_64_integration_integration-r.cybereason.net_443_ACTIVE_NORMAL_rpm.rpm
sleep 5m
yum install nc -y
nc -l -p 3000 -q 5