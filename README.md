Producer changer "bootstrap_servers" avec l'ip du réseau, les PC doivent etre sur le meme reseau
Dans le consumer c'est kafka:9092 il faudra changer le kafka partout par l'ip de la personne qui execute le Consumer

docker-compose down --rmi all
sudo docker-compose up --build