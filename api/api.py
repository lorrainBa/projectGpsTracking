import asyncio
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from starlette.responses import StreamingResponse

# Définition de la base SQLAlchemy
Base = declarative_base()

# Définition du modèle Coords
class Coords(Base):
    __tablename__ = 'coords'

    id = Column(Integer, primary_key=True, index=True)
    numproducer = Column(String, nullable= True) 
    latitude = Column(Float)
    longitude = Column(Float)
    nomlieu = Column(String)

# Initialisation de FastAPI
app = FastAPI()

# Configuration de la base de données
DATABASE_URL = "postgresql://trackinguser:trackingpassword@postgres/trackingdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.get("/coords_stream/{producer}")
async def coords_stream(producer: str):
    db = SessionLocal()
    coordinates = db.query(Coords).filter(Coords.numproducer == producer).all()
    db.close()

    if not coordinates:
        raise HTTPException(status_code=404, detail=f"No coordinates found for producer {producer}")

    async def event_stream():
        for coord in coordinates:
            yield f"data: {json.dumps({'latitude': coord.latitude, 'longitude': coord.longitude})}\n\n"
            await asyncio.sleep(0.01)  # On attend un centième de seconde entre chaque set

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <html>
    <head>
        <title>Map</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
        <style>
            body { margin: 0; height: 100vh; display: flex; flex-direction: column; align-items: center; }
            h1 { margin-top: 20px; }
            #map { flex: 1; width: 100%; }
        </style>
    </head>
    <body>
        <h1>Map</h1>
        <div id="map"></div>
        <script>
            // Initialisation de la map avec au centre CY-Tech
            var map = L.map('map').setView([43.31905613543263, -0.36047011901155285], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);

            // Ajout des markers à CY-Tech
            var marker1 = L.marker([43.31905613543263, -0.36047011901155285]).addTo(map);
            var marker2 = L.marker([43.31905613543263, -0.36047011901155285]).addTo(map);

            // Màj de la position des markers
            function updateMarkerPosition(marker, latitude, longitude) {
                marker.setLatLng([latitude, longitude]);
            }

            // Chaque marker va fetch les coordonnées de son producteur
            function fetchCoordsStream(producer, marker) {
                const eventSource = new EventSource('/coords_stream/' + producer);

                eventSource.onmessage = function(event) {
                    const coord = JSON.parse(event.data);
                    updateMarkerPosition(marker, coord.latitude, coord.longitude);
                };
            }

            fetchCoordsStream('producer1', marker1);
            fetchCoordsStream('producer2', marker2);
        </script>
    </body>
    </html>
    """.strip()

    return HTMLResponse(content=html_content)