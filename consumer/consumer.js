const { Client } = require('pg');
const kafka = require('kafka-node');

const dbConfig = {
  user: 'trackinguser',
  host: 'postgres',
  database: 'trackingdb',
  password: 'trackingpassword',
  port: 5432,
};

const client = new Client(dbConfig);

async function consumeMessages(bootstrapServers, topic) {
  const client = new kafka.KafkaClient({ kafkaHost: bootstrapServers });
  const consumer = new kafka.Consumer(
    client,
    [{ topic: topic, partition: 0 }],
    {
      autoCommit: true,
      autoCommitIntervalMs: 5000,
      fromOffset: 'earliest'
    }
  );

  consumer.on('message', async function (message) {
    try {
      // Traitez les coordonnées reçues
      const coordinates = JSON.parse(message.value);
      console.log(coordinates);
      // Connectez-vous à la base de données
      await client.connect();

      // Ajoutez les données à la base de données sous forme JSON
      const insertQuery = 'INSERT INTO coords (ip, latitude, longitude, nomLieu) VALUES ($1, $2, $3, $4);';
      await client.query(insertQuery, [JSON.stringify(coordinates)]);

      console.log('Received and stored message:', message.value);
    } catch (error) {
      console.error('Error processing message:', error);
    }
  });

  consumer.on('error', function (err) {
    console.error('Error:', err);
  });

  process.on('SIGINT', function () {
    consumer.close(true, function () {
      client.end();
      process.exit();
    });
  });
}

// Utilisation
const bootstrapServers = 'kafka:9092';
const topic = 'coordinates';

consumeMessages(bootstrapServers, topic);
