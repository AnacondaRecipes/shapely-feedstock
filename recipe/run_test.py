import sys

from shapely.geometry import Point, shape

# This test is intended as a regression test for a bug happening
# in a downstream package, fiona. On a couple of platforms
# shapely was built for geos 3.9.1 while for others for 3.8.6 and
# the count of the vertices did not match.
#
# The function vertex_count is taken directly from the failing test
# in fiona that spotted the issue.
#
# Ref:
# https://github.com/Toblerity/Fiona/blob/1.10.1/tests/test_features.py#L67-L69


def vertex_count(obj: object) -> int:
    """Count the vertices of a GeoJSON-like geometry object.

    Parameters
    ----------
    obj: object
        A GeoJSON-like mapping or an object that provides
        __geo_interface__.

    Returns
    -------
    int

    """
    shp = shape(obj)
    if hasattr(shp, "geoms"):
        return sum(vertex_count(part) for part in shp.geoms)
    elif hasattr(shp, "exterior"):
        return vertex_count(shp.exterior) + sum(
            vertex_count(ring) for ring in shp.interiors
        )
    else:
        return len(shp.coords)


obj = Point(0, 0).buffer(10.0).difference(Point(0, 0).buffer(1.0))
count = 130

vc_count = vertex_count(obj)
if not count == vc_count:
    print(f"FAIL {count} != {vc_count}")
    sys.exit(1)
else:
    print("SUCCESS! Vertex counter succeeded.")
