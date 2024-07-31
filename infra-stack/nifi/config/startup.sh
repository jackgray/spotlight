#!/bin/bash

# Replace placeholders in nifi.properties
sed -i "s|{NIFI_HTTP_PORT}|${NIFI_HTTP_PORT}|g" /opt/nifi/nifi-current/conf/nifi.properties
sed -i "s|{NIFI_HTTPS_PORT}|${NIFI_HTTPS_PORT}|g" /opt/nifi/nifi-current/conf/nifi.properties
sed -i "s|{NIFI_KEYSTORE}|${NIFI_KEYSTORE}|g" /opt/nifi/nifi-current/conf/nifi.properties
sed -i "s|{NIFI_KEYSTORE_PASSWORD}|${NIFI_KEYSTORE_PASSWORD}|g" /opt/nifi/nifi-current/conf/nifi.properties
sed -i "s|{NIFI_TRUSTSTORE}|${NIFI_TRUSTSTORE}|g" /opt/nifi/nifi-current/conf/nifi.properties
sed -i "s|{NIFI_TRUSTSTORE_PASSWORD}|${NIFI_TRUSTSTORE_PASSWORD}|g" /opt/nifi/nifi-current/conf/nifi.properties

# Start NiFi
exec /opt/nifi/nifi-current/bin/nifi.sh start
