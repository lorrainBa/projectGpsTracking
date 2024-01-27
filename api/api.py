from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Coordinates  # Assurez-vous d'importer votre modèle de données correctement
import time 

app = FastAPI()

DATABASE_URL = "postgresql://trackinguser:trackingpassword@postgres/trackingdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.on_event("startup")
def startup_db_client():
    time.sleep(5)  # Attente pour s'assurer que la base de données est prête
    pass  # Vous pouvez exécuter d'autres opérations d'initialisation ici si nécessaire

@app.on_event("shutdown")
def shutdown_db_client():
    SessionLocal.close()

@app.get("/", response_class=HTMLResponse)
def read_root():
    db = SessionLocal()
    coordinates = db.query(Coordinates).all()  # Récupérer toutes les coordonnées
    db.close()

    if not coordinates:
        raise HTTPException(status_code=404, detail="No coordinates found")

    # Créer une liste de marqueurs pour Leaflet
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

