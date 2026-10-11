set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# Clean every books/*.md (epub conversion) into books/volume_<N>/, one file per chapter
clean:
    python tools/clean_md.py

# Install the Python packages the map tools need
tools-deps:
    python -m pip install -r tools/requirements.txt

# Vectorize the traced land mask (exported from worldmap_base.pdn) into the World Map's land GeoJSON
map-land:
    python tools/vectorize_mask.py assets/worldmap_base.png assets/worldmap_base.features.json assets/worldmap_base.geojson
