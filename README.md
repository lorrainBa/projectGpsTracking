# Application de tracking GPS avec Kafka

Cette application utilise Docker, Kafka, PostgreSQL, et FastAPI pour créer un système de suivi GPS en temps réel. L'application comprend deux producteurs Kafka, un consommateur Kafka en javascript, une base de données PostgreSQL, et une API FastAPI pour visualiser les données de suivi sur une carte.

## Pour lancer l'application :

docker-compose up --build

## Pour l'arrêter : 

docker-compose down

La carte est accessible à l'adresse http://localhost:8000/. Elle permet de suivre deux parcours différents : un marqueur fait le tour des kebabs de Pau en partant de CY-Tech, un autre fait le tour des parcs.

[trackinggps.webm](https://github.com/lorrainBa/projectGpsTracking/assets/100688035/52b4b7c0-1389-4336-96dc-6091dc932350)


