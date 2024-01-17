from confluent_kafka import Producer

def delivery_report(err, msg):
    """Callback function called on message delivery confirmation."""
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        pass
        #print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def produce_message(bootstrap_servers, topic, message):
    """Produce a message to a Kafka topic."""
    producer_config = {
        'bootstrap.servers': bootstrap_servers,
    }

    producer = Producer(producer_config)

    try:
        # Produce message to topic
        producer.produce(topic, value=str(message), callback=delivery_report)

        # Wait for any outstanding messages to be delivered and delivery reports to be received
        producer.flush()

    except Exception as e:
        print('Exception while producing message: {}'.format(e))

