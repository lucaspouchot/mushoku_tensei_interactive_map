"""Vectorize a hand-traced World Map mask (PNG) into a GeoJSON Map Layer.

Usage: python tools/vectorize_mask.py MASK.png FEATURES.json OUT.geojson
                                      [--blur 1.5] [--tolerance 0.6]

MASK.png      traced over books/assets/MushokuTensei-Vol4_FRONTMATTER_4.jpg at
              the same size (2000x1425): opaque pixels are inside a feature,
              transparent pixels are outside. Edges may be aliased.
FEATURES.json the identity of each feature: a list of
              {"anchor": [x, y], "properties": {"id": ..., ...}} where the
              anchor is a Map Coordinate lying inside the feature.
OUT.geojson   one Polygon per feature, in Map Coordinates.

Map Coordinates live in the World Map plane: 0..6000 x 0..4275, x to the
right, y downward (pixels of the 2000x1425 illustration times 3).

The mask is upsampled to the Map Coordinate grid, blurred, and contoured at
sub-pixel precision, so aliased strokes come out smooth instead of stair-
stepped. Each polygon takes the properties of the anchor it contains, so ids
survive any re-trace. Polygons without an anchor get an "unnamed-NNN" id and
anchors without a polygon are reported; both need a fix in FEATURES.json.

Needs scikit-image and shapely (see tools/requirements.txt).
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from shapely.geometry import Point, Polygon, mapping
from skimage import filters, measure

SOURCE_SIZE = (2000, 1425)
SCALE = 3
OPAQUE = 128
MIN_AREA = 30  # in squared Map Coordinate units; drops specks left by stray pixels
DECIMALS = 2


def load_mask(path):
    image = Image.open(path).convert("RGBA")
    if image.size != SOURCE_SIZE:
        sys.exit(f"{path}: expected {SOURCE_SIZE[0]}x{SOURCE_SIZE[1]}, got {image.size[0]}x{image.size[1]}")
    return np.asarray(image)[..., 3] > OPAQUE


def contour_rings(mask, blur):
    width, height = SOURCE_SIZE[0] * SCALE, SOURCE_SIZE[1] * SCALE
    upsampled = Image.fromarray((mask * 255).astype(np.uint8)).resize((width, height), Image.BILINEAR)
    field = filters.gaussian(np.asarray(upsampled, dtype=float) / 255, sigma=blur)
    # Pad so features touching the edge still yield closed rings.
    for contour in measure.find_contours(np.pad(field, 1), 0.5):
        # (row, col) of the padded grid -> (x, y) at pixel centres of the Map Coordinate grid
        ring = Polygon(contour[:, ::-1] - 1 + 0.5)
        if ring.area >= MIN_AREA:
            yield ring


def assemble(rings, tolerance):
    """Nest rings by containment: even depth is a shell, odd depth a hole of its parent."""
    rings = sorted(rings, key=lambda ring: ring.area, reverse=True)
    parents = []
    for index, ring in enumerate(rings):
        point = ring.representative_point()
        containing = [j for j in range(index) if rings[j].contains(point)]
        parents.append(containing[-1] if containing else None)
    depth = []
    for parent in parents:
        depth.append(0 if parent is None else depth[parent] + 1)
    shells = {}
    for index, ring in enumerate(rings):
        if depth[index] % 2 == 0:
            shells[index] = (ring, [])
        else:
            shells[parents[index]][1].append(ring)
    for shell, holes in shells.values():
        polygon = Polygon(shell.exterior.coords, [hole.exterior.coords for hole in holes])
        yield polygon.simplify(tolerance, preserve_topology=True)


def rounded(geometry):
    def walk(value):
        if isinstance(value, (list, tuple)) and value and isinstance(value[0], (int, float)):
            return [round(value[0], DECIMALS), round(value[1], DECIMALS)]
        return [walk(item) for item in value]
    geometry = mapping(geometry)
    return {"type": geometry["type"], "coordinates": walk(geometry["coordinates"])}


def identify(polygons, features):
    anchors = [(Point(feature["anchor"]), feature["properties"]) for feature in features]
    used = set()
    unnamed = 0
    for polygon in sorted(polygons, key=lambda p: (p.bounds[1], p.bounds[0])):
        matches = [i for i, (anchor, _) in enumerate(anchors) if polygon.contains(anchor)]
        if len(matches) > 1:
            ids = ", ".join(anchors[i][1]["id"] for i in matches)
            print(f"warning: one polygon holds several anchors ({ids}); keeping the first", file=sys.stderr)
        if matches:
            used.add(matches[0])
            properties = anchors[matches[0]][1]
        else:
            unnamed += 1
            x, y = polygon.representative_point().coords[0]
            properties = {"id": f"unnamed-{unnamed:03d}"}
            print(f"warning: polygon near ({x:.0f}, {y:.0f}) has no anchor; named {properties['id']}", file=sys.stderr)
        yield properties, polygon
    for i, (anchor, properties) in enumerate(anchors):
        if i not in used:
            print(f"warning: anchor {properties['id']} at ({anchor.x:.0f}, {anchor.y:.0f}) matches no polygon", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("mask", type=Path)
    parser.add_argument("features", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--blur", type=float, default=1.5, help="Gaussian sigma in Map Coordinate units")
    parser.add_argument("--tolerance", type=float, default=0.6, help="simplification tolerance in Map Coordinate units")
    args = parser.parse_args()

    features = json.loads(args.features.read_text(encoding="utf-8"))
    polygons = list(assemble(contour_rings(load_mask(args.mask), args.blur), args.tolerance))
    collection = {
        "type": "FeatureCollection",
        "coordinate_frame": "World Map plane: 0..6000 x 0..4275, x right, y down (illustration pixels x 3); not longitude/latitude",
        "features": [
            {"type": "Feature", "id": properties["id"], "properties": properties, "geometry": rounded(polygon)}
            for properties, polygon in identify(polygons, features)
        ],
    }
    args.out.write_text(json.dumps(collection, ensure_ascii=False), encoding="utf-8")
    vertices = sum(len(p.exterior.coords) + sum(len(h.coords) for h in p.interiors) for p in polygons)
    print(f"{args.out}: {len(polygons)} polygons, {vertices} vertices")


if __name__ == "__main__":
    main()
