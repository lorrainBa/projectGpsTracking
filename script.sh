#!/bin/bash

# Commande pour créer le topic "coordinates"
docker exec -t kafka kafka-topics.sh --create --bootstrap-server kafka:9092 --replication-factor 1 --partitions 1 --topic coordinates

echo "Le topic 'coordinates' a été créé avec succès."
