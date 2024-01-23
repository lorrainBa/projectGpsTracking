from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time 

Base = declarative_base()

DATABASE_URL = "postgresql://trackinguser:trackingpassword@postgres/trackingdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création de la base de données coordonnées avec des colonnes id, latitude et longitude
class Coordinates(Base):
    __tablename__ = "coordinates"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

app = FastAPI()

# Configuration de la base de données
@app.on_event("startup")
def startup_db_client():
    time.sleep(5)
    Base.metadata.create_all(bind=engine)

# Fermeture de la connexion à la base de données
@app.on_event("shutdown")
def shutdown_db_client():
    SessionLocal.close()

@app.get("/", response_class=HTMLResponse)
def read_root():
    # Récupérer les coordonnées depuis la base de données
    db = SessionLocal()
    coordinates = db.query(Coordinates).first()
    db.close()

    # Générer la page HTML avec les coordonnées
    html_content = f"""
    <html>
    <head>
        <title>Map</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
        <style>
            body {{
                margin: 0;
                height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            h1 {{
                margin-top: 20px;
            }}
            #map {{
                flex: 1;
                width: 100%;
            }}
        </style>
    </head>
    <body>
        <h1>Map</h1>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([{coordinates.latitude}, {coordinates.longitude}], 13);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '© OpenStreetMap contributors'
            }}).addTo(map);
            L.marker([{coordinates.latitude}, {coordinates.longitude}]).addTo(map);
        </script>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)
