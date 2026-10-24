# Gridfinity calibration bin v3 (3d-print/lab2/gridfinity-calibration). Run as: header of s_gf_std.py + this file.
# 1x1, standard foot, 41.5 x 41.5 x 21, pocket 37 for the 4-corner suction-cup method, 1 x 35 mm cross 0.6 deep.

def run(_context):
    app = adsk.core.Application.get(); d = adsk.fusion.Design.cast(app.activeProduct); root = d.rootComponent
    up = d.userParameters; vi = adsk.core.ValueInput.createByString; P3 = adsk.core.Point3D.create
    P = {"gf_fit_adjust": ("0 mm", "Extra inward offset of the standard Gridfinity foot per side (0 = standard)"),
         "cal_height": ("21 mm", "Calibration bin height from the foot bottom, 3 Gridfinity units"),
         "cal_floor": ("7 mm", "Floor top above the foot bottom (BASE_HEIGHT of the generator)"),
         "cal_pocket": ("37 mm", "Inner pocket for the 4-corner suction cup method (cup ~22 mm effective -> ~15 mm travel)"),
         "cal_pocket_r": ("0.5 mm", "Inner pocket corner radius"),
         "cal_cross_w": ("1 mm", "Centre cross line width"),
         "cal_cross_depth": ("0.6 mm", "Centre cross depth (3 layers at 0.2)"),
         "cal_cross_len": ("35 mm", "Centre cross line length")}
    for n, (e, c) in P.items():
        if up.itemByName(n) is None: up.add(n, vi(e), "mm", c)
    v = lambda n: up.itemByName(n).value * 10   # mm
    cx, cy = -181.5, -63.0                      # cell B-2 (assignment: calibrate in B-2)
    z0 = 2.629 - 0.34                           # foot bottom when the chamfers touch (parallel profiles, 0.24 gap)
    o = root.occurrences.addNewComponent(adsk.core.Matrix3D.create()); C = o.component; C.name = "gridfinity_calibration_v3"
    def plane(z):
        pi = C.constructionPlanes.createInput(); pi.setByOffset(C.xYConstructionPlane, adsk.core.ValueInput.createByReal(z / 10))
        return C.constructionPlanes.add(pi)
    def rrect(sk, half, r):
        L = sk.sketchCurves.sketchLines.addCenterPointRectangle(P3(cx / 10, cy / 10, 0), P3((cx + half) / 10, (cy + half) / 10, 0))
        for k in range(4):
            a, b = L.item(k), L.item((k + 1) % 4)
            sk.sketchCurves.sketchArcs.addFillet(a, a.endSketchPoint.geometry, b, b.startSketchPoint.geometry, r / 10)
    def ext(sk, dist, op, start=None):
        ei = C.features.extrudeFeatures.createInput(sk.profiles.item(0), op)
        ei.setDistanceExtent(False, adsk.core.ValueInput.createByReal(dist / 10))
        if op != adsk.fusion.FeatureOperations.NewBodyFeatureOperation: ei.participantBodies = [C.bRepBodies.item(0)]
        return C.features.extrudeFeatures.add(ei)
    top = z0 + GF_HEIGHT
    sk = C.sketches.add(plane(top)); sk.name = "cal_body"; rrect(sk, 20.75 - v("gf_fit_adjust"), 3.75 - v("gf_fit_adjust"))
    ext(sk, v("cal_height") - GF_HEIGHT, adsk.fusion.FeatureOperations.NewBodyFeatureOperation).name = "cal_body"
    add_std_feet(C, [(cx, cy)], top)
    sk = C.sketches.add(plane(z0 + v("cal_height"))); sk.name = "cal_pocket"; rrect(sk, v("cal_pocket") / 2, v("cal_pocket_r"))
    ext(sk, -(v("cal_height") - v("cal_floor")), adsk.fusion.FeatureOperations.CutFeatureOperation).name = "cal_pocket"
    sk = C.sketches.add(plane(z0 + v("cal_floor"))); sk.name = "cal_cross"
    w, l = v("cal_cross_w") / 2, v("cal_cross_len") / 2   # mm
    sk.sketchCurves.sketchLines.addTwoPointRectangle(P3((cx - l) / 10, (cy - w) / 10, 0), P3((cx + l) / 10, (cy + w) / 10, 0))
    sk.sketchCurves.sketchLines.addTwoPointRectangle(P3((cx - w) / 10, (cy - l) / 10, 0), P3((cx + w) / 10, (cy + l) / 10, 0))
    profs = adsk.core.ObjectCollection.create()
    for p in sk.profiles: profs.add(p)
    ei = C.features.extrudeFeatures.createInput(profs, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ei.setDistanceExtent(False, adsk.core.ValueInput.createByReal(-v("cal_cross_depth") / 10)); ei.participantBodies = [C.bRepBodies.item(0)]
    C.features.extrudeFeatures.add(ei).name = "cal_cross"
    b = C.bRepBodies.item(0); b.name = "gridfinity_calibration_v3"
    bb = b.boundingBox
    print("bodies %d  %.2f x %.2f x %.2f mm  vol %.2f cm3  z %.3f..%.3f" % (C.bRepBodies.count, (bb.maxPoint.x-bb.minPoint.x)*10, (bb.maxPoint.y-bb.minPoint.y)*10, (bb.maxPoint.z-bb.minPoint.z)*10, b.volume, bb.minPoint.z*10, bb.maxPoint.z*10))
