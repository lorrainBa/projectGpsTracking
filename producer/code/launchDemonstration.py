from createCoord import getCoordsFromFile, calculateNewCoord
from sendCoordToKafka import produce_message
from math import sqrt
import sys
import json
import os


if __name__ == "__main__" :
    #Recuperer l'information si c'est executé en tant que producer 1 ou producer 2
    numProducer = os.getenv("IP_PRODUCER")
    print("numproducer----",numProducer)
        
    # Configuration pour kafka
    bootstrap_servers = 'kafka:9092'
    kafka_topic = 'coordinates'

    #Recuperer les coordonnes des lieux à visiter de pau et la position initial à CY-Tech
    
    if numProducer == "producer1":
        coordsToVisit = getCoordsFromFile("kebab")
        currentCoord = [43.31905613543263, -0.36047011901155285]

    elif numProducer == "producer2":
        coordsToVisit = getCoordsFromFile("garden")
        currentCoord = [43.31905613543263, -0.36047011901155285]

    currentCoordsToVisit = coordsToVisit

    #Tant qu'il y a des lieux à visiter le personnage va continuer à marcher
    while currentCoordsToVisit:
        print(len(currentCoordsToVisit))
        nomLieu, destination = currentCoordsToVisit.popitem()

        # Tant que le personnage n'est pas assez proche du lieux il continue d'avancer
        while (sqrt(((currentCoord[0]-destination[0])**2 + (currentCoord[1]-destination[1])**2))) > 0.00002:
            currentCoordToSend= calculateNewCoord(currentCoord, destination, speed = 1 )
            
            # Construire le message pour kafka en le metant sous forme de json
            messageToSend = {"numProducer":numProducer,"latitude":currentCoordToSend[0],"longitude":currentCoordToSend[1],"nomLieu":nomLieu}
            messageToSend = json.dumps(messageToSend)

            print(messageToSend)
            produce_message(bootstrap_servers, kafka_topic, messageToSend)
        print("ARRIVEE KEBAB")
        print("currentCoord",currentCoord)

        if len(currentCoordsToVisit) == 0:
            currentCoordsToVisit = coordsToVisit