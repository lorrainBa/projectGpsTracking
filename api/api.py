from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Définition de la base SQLAlchemy
Base = declarative_base()

# Définition du modèle Coords
class Coords(Base):
    __tablename__ = 'coords'

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, nullable= True)  # Ajout de la colonne ip
    latitude = Column(Float)
    longitude = Column(Float)
    nomlieu = Column(String)  # Ajout de la colonne nomlieu

# Initialisation de FastAPI
app = FastAPI()

# Configuration de la base de données
DATABASE_URL = "postgresql://trackinguser:trackingpassword@postgres/trackingdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Route principale de l'API
@app.get("/", response_class=HTMLResponse)
def read_root():
    db = SessionLocal()
    coordinates = db.query(Coords).all()  # Utilisation du modèle Coords
    db.close()

    if not coordinates:
        raise HTTPException(status_code=404, detail="No coordinates found")

    markers = ''.join(f"L.marker([{coord.latitude}, {coord.longitude}]).addTo(map);\n" for coord in coordinates)

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
            var map = L.map('map').setView([{coordinates[0].latitude}, {coordinates[0].longitude}], 13);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '© OpenStreetMap contributors'
            }}).addTo(map);
            {markers}
        </script>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)
