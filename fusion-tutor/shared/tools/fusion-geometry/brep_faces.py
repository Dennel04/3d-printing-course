# Fusion script (run through Fusion MCP, read-only): list the exact faces of a body inside a box.
# Prints every face as Plane / Cylinder / Cone / Torus with its real parameters (radius, half-angle,
# normal), in mm and relative to CENTRE. Use it to "see" fillets and chamfers exactly instead of
# guessing them from a screenshot or sampling points. Written 2026-10-24 for the Gridfinity socket
# (see ../../knowledge/gridfinity-socket.md).
#
# Edit the four settings below, then run with readOnly: true.
import adsk.core, adsk.fusion, math

OCCURRENCE_PATH = ["MG 400 rakis:1", "rakis_E_long:1"]   # occurrence names from the root down
BODY = "grid_pos_0"
CENTRE = (-139.5, 21.0)        # mm, e.g. a cell centre
BOX = 21.5                     # mm, half-size of the search box around CENTRE (XY)


def run(_context):
    app = adsk.core.Application.get()
    root = adsk.fusion.Design.cast(app.activeProduct).rootComponent
    occs, occ = root.occurrences, None
    for n in OCCURRENCE_PATH:
        occ = occs.itemByName(n)
        occs = occ.childOccurrences
    body = [b for b in occ.bRepBodies if b.name == BODY][0]
    cx, cy = CENTRE
    rows = []
    for f in body.faces:
        bb = f.boundingBox
        x0, x1, y0, y1 = bb.minPoint.x * 10, bb.maxPoint.x * 10, bb.minPoint.y * 10, bb.maxPoint.y * 10
        if x1 < cx - BOX or x0 > cx + BOX or y1 < cy - BOX or y0 > cy + BOX:
            continue
        g = f.geometry
        t = type(g).__name__
        if t == "Plane":
            d = "normal (%.3f, %.3f, %.3f)" % (g.normal.x, g.normal.y, g.normal.z)
        elif t == "Cylinder":
            d = "R %.3f, axis at (%.3f, %.3f)" % (g.radius * 10, g.origin.x * 10 - cx, g.origin.y * 10 - cy)
        elif t == "Cone":
            d = "R %.3f at z %.3f, half-angle %.2f deg, axis at (%.3f, %.3f)" % (
                g.radius * 10, g.origin.z * 10, math.degrees(g.halfAngle), g.origin.x * 10 - cx, g.origin.y * 10 - cy)
        elif t == "Torus":
            d = "major %.3f minor %.3f" % (g.majorRadius * 10, g.minorRadius * 10)
        else:
            d = ""
        rows.append((bb.maxPoint.z, "%-8s z %8.3f..%8.3f  x %8.3f..%8.3f  y %8.3f..%8.3f  %s" % (
            t, bb.minPoint.z * 10, bb.maxPoint.z * 10, x0 - cx, x1 - cx, y0 - cy, y1 - cy, d)))
    for _, r in sorted(rows, reverse=True):
        print(r)
