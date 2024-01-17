from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
    <head>
        <title>Map</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
        <style>
            body {
                margin: 0;
                height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            h1 {
                margin-top: 20px;
            }
            #map {
                flex: 1;
                width: 100%;
            }
        </style>
    </head>
    <body>
        <h1>Map</h1>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([51.505, -0.09], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);
        </script>
    </body>
    </html>
    """

