# Utilisez une image de Python en tant que base
FROM python:3.8

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers nécessaires dans le conteneur
COPY . .

# Installez les dépendances, si nécessaire
RUN pip install -r requirements.txt



# Commande par défaut à exécuter lorsque le conteneur démarre
CMD ["python", "code/launchDemonstration.py"]