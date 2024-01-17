from createCoord import getCoordKebab, calculateNewCoord
from sendCoordToKafka import produce_message
from readBrokerKafka import consume_messages
from math import sqrt


if __name__ == "__main__":


    # Configuration
    bootstrap_servers = 'localhost:9092'  # Update with your Kafka broker(s)
    kafka_topic = 'my_topic'  # Update with your Kafka topic


    #Consumer configuration
    group_id = 'my_consumer_group'  # Mettez à jour avec votre ID de groupe de consommateurs

    #Get coords of the kebab of Pau, get init position at CyTech
    coordsKebab = getCoordKebab()
    currentCoord = [43.31905613543263, -0.36047011901155285]

    

    #While there is kebab to visit
    while coordsKebab:
        cle_a_supprimer, destination = coordsKebab.popitem()
        print("ARRIVEE KEBAB")
        print('destination',destination)
        #Continue to go to the kebab if you're not near
        while (sqrt(((currentCoord[0]-destination[0])**2 + (currentCoord[1]-destination[1])**2))) > 0.00002:
            currentCoordToSend= calculateNewCoord(currentCoord, destination, speed = 1 )
            # Produce the message to Kafka
            produce_message(bootstrap_servers, kafka_topic, currentCoordToSend)
        print("currentCoord",currentCoord)