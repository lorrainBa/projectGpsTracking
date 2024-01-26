const { Client } = require('pg');
const kafka = require('kafka-node');

const dbConfig = {
  user: 'trackinguser',
  host: 'trackingpostgres',
  database: 'trackingdb',
  password: 'trackingpassword',
  port: 5432,
};

const pgclient = new Client(dbConfig);

pgclient.connect();

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
      console.log('coo', coordinates);
      // Ajoutez les données à la base de données sous forme JSON
      const insertQuery = 'INSERT INTO coords (ip, latitude, longitude, nomLieu) VALUES ($1, $2, $3, $4)';
      pgclient.query(insertQuery, [coordinates.ip, coordinates.latitudes, coordinates.longitude, coordinates.nomLieu]);

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
