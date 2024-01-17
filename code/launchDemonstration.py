from createCoord import generateCoord
from sendCoordToKafka import produce_message
from readBrokerKafka import consume_messages

if __name__ == "__main__":
    # Configuration
    bootstrap_servers = 'localhost:9092'  # Update with your Kafka broker(s)
    kafka_topic = 'my_topic'  # Update with your Kafka topic
    message_to_send = [1, 2, 3, 4, 5]

    #Consumer configuration
    group_id = 'my_consumer_group'  # Mettez à jour avec votre ID de groupe de consommateurs

    # Produce the message to Kafka
    produce_message(bootstrap_servers, kafka_topic, message_to_send)
