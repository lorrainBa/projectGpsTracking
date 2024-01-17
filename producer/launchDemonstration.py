from createCoord import getCoordKebab, calculateNewCoord
from sendCoordToKafka import produce_message
from math import sqrt
import sys
import json



if __name__ == "__main__" :
    #Get the input to see if it's producer 1 or producer 2
    if len(sys.argv) > 1:
        numProducer = sys.argv[1]
    else:
        numProducer = "producer1"
        
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
        nomKebab, destination = coordsKebab.popitem()
        
        print('destination',destination)
        #Continue to go to the kebab if you're not near
        while (sqrt(((currentCoord[0]-destination[0])**2 + (currentCoord[1]-destination[1])**2))) > 0.00002:
            currentCoordToSend= calculateNewCoord(currentCoord, destination, speed = 1 )
            
            # Produce the message to Kafka and put it in a string
            messageToSend = {"ip":numProducer,"latitude":currentCoordToSend[0],"longitude":currentCoordToSend[1],"nomKebab":nomKebab}
            messageToSend = json.dumps(messageToSend)

            print(messageToSend)
            produce_message(bootstrap_servers, kafka_topic, messageToSend)
        print("ARRIVEE KEBAB")
        print("currentCoord",currentCoord)