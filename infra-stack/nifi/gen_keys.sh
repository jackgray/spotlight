# Generate a keystore
keytool -genkey -alias nifi -keyalg RSA -keystore config/keystore.jks -keysize 2048 -validity 365 -storepass changeit -keypass changeit

# Generate a truststore
keytool -import -file config/server.crt -alias nifi -keystore truststore.jks -storepass changeit
