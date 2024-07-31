from kafka import KafkaProducer
import os
import some_protobuf_library as pb

class KafkaHandler:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'))
    
    def convert_to_protobuf(self, data):
        return pb.convert(data)  # Implement your conversion logic here

    def send(self, data, topic):
        protobuf_data = self.convert_to_protobuf(data)
        self.producer.send(topic, protobuf_data)
        self.producer.flush()

kafka_handler = KafkaHandler()
