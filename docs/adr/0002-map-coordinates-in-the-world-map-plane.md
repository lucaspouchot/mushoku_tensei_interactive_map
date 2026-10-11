# Map Coordinates in the World Map plane, not longitude/latitude

The World Map is a vector map redrawn from the volume 4 illustration. Every Location and Route will store Map Coordinates, so the frame is costly to change once data exists.

We store Map Coordinates as points in the World Map's own plane: 0..6000 × 0..4275, x to the right, y downward, where one unit is a pixel of the 2000×1425 illustration divided by 3. Distances are Euclidean in that plane. GeoJSON files use these coordinates and say so in a `coordinate_frame` member. OpenLayers renders them with a custom projection in pixel units, negating y on load.

## Considered Options

- **Longitude/latitude spread over a world map** (the first conversion tried). Rejected: the novels say nothing about the world's shape or size, so degrees would be invented. That conversion also had unequal scales per axis (one degree of latitude covered 1.43× more map than one degree of longitude), which stretches the display and distorts every distance. Under Web Mercator, the default of most map tools, the north and south would stretch further still, and spherical distance functions would shrink east-west distances near the "poles" by up to three times.
- **Longitude/latitude with equal scales on both axes**, always shown in plate carrée and measured in the plane. Kept as the fallback if editing in online GIS tools ever matters. Rejected for now: the degrees mean nothing, and they invite spherical maths that would be wrong.
- **Fractions of the image file (0–1 per axis).** Rejected: the units are not square, and the frame depends on the file's crop rather than on the artwork.

## Consequences

- Online GeoJSON viewers (geojson.tools, geojson.io) assume WGS84 and show these files wrongly. QGIS, OpenLayers and the project's own preview do not.
- A position read on the volume 4 illustration converts into a Map Coordinate by multiplying by 3.
- Travel durations need a scale factor from map distance to time, calibrated against the text later.
