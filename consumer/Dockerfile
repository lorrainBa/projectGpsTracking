FROM node:14

WORKDIR /app

COPY package.json package-lock.json /app/

RUN npm install

COPY . /app/

# Exposer le port si nécessaire
# EXPOSE 3000

# Commande pour démarrer l'application
CMD ["node", "consumer.js"]
