version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      KAFKA_BOOTSTRAP_SERVERS: $KAFKA_BOOTSTRAP_SERVERS
      KAFKA_TOPIC: 'swaps_raw'
