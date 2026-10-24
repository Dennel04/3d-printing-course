# Fusion API helper: STANDARD Gridfinity bin foot (gridfinity-rebuilt-openscad BASE_PROFILE). See ../../knowledge/gridfinity-socket.md.
# Paste into a Fusion script (Fusion MCP) and call add_std_feet(). Dennel04 + Claude, 2026-10-24.
import adsk.core, adsk.fusion, math
MM = 0.1
# Standard Gridfinity bin foot (gridfinity-rebuilt-openscad BASE_PROFILE / gridfinity.xyz spec):
# from the bottom: 45 deg 0.8, vertical 1.8, 45 deg 2.15 = 4.75 mm; 35.6 -> 37.2 -> 41.5 mm per unit,
# corner radius 0.8 -> 1.6 -> 3.75, all corner arcs centred 17 mm from the cell centre.
# In the MG 400 rakis socket (0.7 / 1.8 / 2.15, 36.28 -> 37.68 -> 41.98) the profiles are parallel
# with 0.24 mm horizontal gap: a 1x1 bin wedges on the chamfers; a multi-cell bin rests on the inner ridges.
GF_TOP_HALF, GF_CORNER_C = 20.75, 17.0
GF_STEPS = (2.15, 1.8, 0.8)                 # top -> bottom
GF_HEIGHT = sum(GF_STEPS)                   # 4.75


def add_std_feet(comp, centres_mm, foot_top_z_mm, adjust_param="gf_fit_adjust"):
    """Join standard feet below the plane foot_top_z_mm (bin bottom + 4.75) to comp.bRepBodies[0].
    adjust_param: user parameter, extra inward offset per side (0 = standard)."""
    des = comp.parentDesign
    adj = des.userParameters.itemByName(adjust_param).value * 10
    target = comp.bRepBodies.item(0)
    P3 = adsk.core.Point3D.create
    halves = (GF_TOP_HALF - adj, GF_TOP_HALF - GF_STEPS[0] - adj, GF_TOP_HALF - GF_STEPS[0] - adj)
    z = foot_top_z_mm
    for i, (step, half) in enumerate(zip(GF_STEPS, halves)):
        pi = comp.constructionPlanes.createInput()
        pi.setByOffset(comp.xYConstructionPlane, adsk.core.ValueInput.createByReal(z * MM))
        sk = comp.sketches.add(comp.constructionPlanes.add(pi))
        sk.name = "gf_std_foot%d" % (i + 1)
        r = half - GF_CORNER_C
        for (x, y) in centres_mm:
            L = sk.sketchCurves.sketchLines.addCenterPointRectangle(P3(x * MM, y * MM, 0), P3((x + half) * MM, (y + half) * MM, 0))
            for k in range(4):
                a, b = L.item(k), L.item((k + 1) % 4)
                sk.sketchCurves.sketchArcs.addFillet(a, a.endSketchPoint.geometry, b, b.startSketchPoint.geometry, r * MM)
        profs = adsk.core.ObjectCollection.create()
        for p in sk.profiles:
            profs.add(p)
        ei = comp.features.extrudeFeatures.createInput(profs, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        ext = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(-step * MM))
        ei.setOneSideExtent(ext, adsk.fusion.ExtentDirections.PositiveExtentDirection,
                            adsk.core.ValueInput.createByString("0 deg" if i == 1 else "-45 deg"))
        ei.participantBodies = [target]
        f = comp.features.extrudeFeatures.add(ei)
        f.name = "gf_std_foot%d" % (i + 1)
        z -= step
    return z
