from confluent_kafka import Producer


#Envoie le message à un topic kafka
def produce_message(bootstrap_servers, topic, message):
    """Produce a message to a Kafka topic."""
    producer_config = {
        'bootstrap.servers': bootstrap_servers,
    }

    producer = Producer(producer_config)

    try:
        producer.produce(topic, value=str(message))
        producer.flush()

    except Exception as e:
        print('Exception while producing message: {}'.format(e))

