const { Client } = require('pg');
const Kafka = require('node-rdkafka');

const dbConfig = {
  user: 'trackinguser',
  host: 'postgres',
  database: 'trackingdb',
  password: 'trackingpassword',
  port: 5432,
};

const client = new Client(dbConfig);

async function consumeMessages(bootstrapServers, groupId, topic) {
  const consumer = new Kafka.KafkaConsumer(
    {
      'group.id': groupId,
      'metadata.broker.list': bootstrapServers,
      'auto.offset.reset': 'earliest',
    },
    {}
  );

  consumer.connect();

  consumer
    .on('ready', function () {
      console.log('Consumer is ready.');

      consumer.subscribe([topic]);
      consumer.consume();
    })
    .on('data', async function (message) {
      try {
        // Traitez les coordonnées reçues
        const coordinates = JSON.parse(message.value.toString());
        console.log(coordinates);
        // Connectez-vous à la base de données
        await client.connect();

        // Ajoutez les données à la base de données sous forme JSON
        const insertQuery = 'INSERT INTO coords (ip, latitude, longitude, nomLieu) VALUES ($1, $2, $3, $4);';
        await client.query(insertQuery, [JSON.stringify(coordinates)]);

        console.log('Received and stored message:', message.value.toString());
      } catch (error) {
        console.error('Error processing message:', error);
      }
    })
    .on('error', function (err) {
      console.error('Error:', err);
    });

  process.on('SIGINT', function () {
    consumer.disconnect();
    client.end();
  });
}

// Utilisation
const bootstrapServers = '172.21.0.2:9092'; // Utilisez le nom du service Kafka dans le réseau Docker
const groupId = 'gps_consumer_group';
const topic = 'coordinates';

consumeMessages(bootstrapServers, groupId, topic);
