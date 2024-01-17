from confluent_kafka import Consumer, KafkaException

def consume_messages(bootstrap_servers, group_id, topic):
    consumer_config = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_config)

    try:
        consumer.subscribe([topic])

        while True:
            try:
                msg = consumer.poll(timeout=1000)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break
                print('Received message: {}'.format(msg.value().decode('utf-8')))
                
                # Vous pouvez ajouter ici la logique pour traiter les coordonnées reçues

            except KeyboardInterrupt:
                break

    except Exception as e:
        print('Exception while consuming messages: {}'.format(e))

    finally:
        consumer.close()


