"""Parametric prototype kit for UT Narva 3D Printing Lab 3.
Five mechanical fit-test objects (NOT qualified pressure/UV safety hardware).
Dependencies: cadquery 2.8+, trimesh, numpy, lxml.
Run: python source/build_models.py
"""
from __future__ import annotations
from pathlib import Path
import math, zipfile, xml.etree.ElementTree as ET, json, csv
import cadquery as cq
import trimesh
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
for d in ('STL','STEP','3MF'):(ROOT/d).mkdir(exist_ok=True)

P = {
  # sourced product catalogue dimensions, millimetres
  'metcal_910b_barrel_od':18.26,
  'metcal_910b_barrel_id':15.72,
  'metcal_910b_flange_flat_span':22.6,
  'metcal_910b_flange_overall_span':34.0,
  'metcal_910b_flange_thickness':3.3,
  'metcal_910b_overall_length':90.9,
  'sarstedt_751337500_cup_top_diameter':37.0,
  'sarstedt_751337500_cup_height':40.0,
  'gridfinity_pitch':42.0, 'gf_nominal_1x1_width':41.5,
  # CAD candidate parameters requiring physical fitting
  'clip_radial_clearance':0.30, # per side
  'clip_mouth_gap':15.4,
  'cup_socket_open_diameter':37.9,
  'cup_socket_bottom_diameter':29.0,
  'nozzle_park_bore_diameter':6.8,
  'oring_nominal_id':11.0,'oring_nominal_cs':2.5,
  'oring_groove_root_diameter':11.50,'oring_groove_width':3.2,
  'oring_test_plug_body_diameter':14.66,
  'uv_led_starboard_ref_outer_dimension':19.9,
  'uv_aperture_diameter':22.5,
  'uv_shroud_side':66.0,'uv_shroud_height':29.0,
}

def wround(width,z,r=3.75, n=9):
    h=width/2
    pts=[]
    for cx,cy,a in ((h-r,h-r,0),(-h+r,h-r,90),(-h+r,-h+r,180),(h-r,-h+r,270)):
        # traverse CCW from rightmost at top-right to top, then up-left etc
        for angle in np.linspace(a,a+90,n,endpoint=False):
            # CCW: angle 0 point right, 90 point up
            pts.append(cq.Vector(cx+r*math.cos(math.radians(angle)), cy+r*math.sin(math.radians(angle)), z))
    pts.append(pts[0]);return cq.Wire.makePolygon(pts)

def gridfinity_foot():
    # z profile: w35.6->37.2 (0.8), vertical to 2.6, 45deg widening to 41.5 at 4.75
    # (outer corners radiused). No magnet / screw holes in this prototype.
    sections=[(0.0,35.6,2.50),(0.8,37.2,3.0),(2.6,37.2,3.0),(4.75,41.5,3.75)]
    return cq.Solid.makeLoft([wround(w,z,r) for z,w,r in sections], ruled=True)

def rounded_box_xy(side, depth, height, z, radius=3.75):
    return cq.Workplane('XY').box(side,depth,height,centered=(True,True,False)).translate((0,0,z)).edges('|Z').fillet(radius).val()

def cup_holder():
    foot=gridfinity_foot()
    body=rounded_box_xy(41.5,41.5,20.75,4.75,3.75) # top z25.5
    shape=foot.fuse(body)
    # Taper seats the cup only after real bottom diameter is verified; retains solid 4mm floor.
    cone=cq.Solid.makeCone(P['cup_socket_bottom_diameter']/2,
       P['cup_socket_open_diameter']/2,17.0,cq.Vector(0,0,8.5),cq.Vector(0,0,1))
    return shape.cut(cone)

def nozzle_park():
    foot=gridfinity_foot()
    body=rounded_box_xy(41.5,41.5,3.25,4.75,3.75) # top 8
    tube=cq.Solid.makeCylinder(12.5,21.0,cq.Vector(0,0,8.0))
    combined=foot.fuse(body).fuse(tube)
    # Dark blind pocket; needs a verified silicone closure before UV resin storage.
    blind=cq.Solid.makeCylinder(P['nozzle_park_bore_diameter']/2,20.5,cq.Vector(0,0,9.0))
    # top shallow wider relief for nozzle hub, but does not assume hub dimensions
    relief=cq.Solid.makeCylinder(5.5,2.5,cq.Vector(0,0,26.5))
    return combined.cut(blind).cut(relief)

def clip():
    # Horseshoe C-clip for 910-B barrel, flange rests at top. Part is a bench fit test,
    # not final MG400 multi-tool mount. PLA fatigue/spring behavior must be checked.
    r_in=(P['metcal_910b_barrel_od']/2)+P['clip_radial_clearance']
    r_out=13.0
    angle=math.degrees(math.acos(P['clip_mouth_gap']/(2*r_in)))
    start=180.0-angle; end=360.0+angle
    angles=np.linspace(start,end,140)
    pts=[(r_out*math.cos(math.radians(a)),12+r_out*math.sin(math.radians(a))) for a in angles]
    pts += [(r_in*math.cos(math.radians(a)),12+r_in*math.sin(math.radians(a))) for a in angles[::-1]]
    ring=cq.Workplane('XY').polyline(pts).close().extrude(20.0).translate((0,0,3.7)).val()
    foot=cq.Workplane('XY').box(50,21,4,centered=(True,True,False)).translate((0,-9,0)).val()
    bridge=cq.Workplane('XY').box(20,7.5,7,centered=(True,True,False)).translate((0,-1.0,3.4)).val()
    part=foot.fuse(bridge).fuse(ring)
    for x in (-17.0,17.0):
        part=part.cut(cq.Solid.makeCylinder(2.25,4.2,cq.Vector(x,-13.0,0)))
    return part

def uv_shroud():
    # PRINT INVERTED: 3mm roof on print bed at z=0, skirt walls grow upwards.
    # After installation, the roof is uppermost and opens to an OUTSIDE-mounted LED/heatsink.
    # Not UV-safe until heat/optical isolation verified; no mounting holes are claimed to match a heatsink.
    outer=rounded_box_xy(P['uv_shroud_side'],P['uv_shroud_side'],P['uv_shroud_height'],0,5.0)
    cavity=rounded_box_xy(60,60,26.2,3,2.5)
    shape=outer.cut(cavity)
    central=cq.Solid.makeCylinder(P['uv_aperture_diameter']/2,3.2,cq.Vector(0,0,0))
    shape=shape.cut(central)
    # short inside aperture baffle; doesn't enclose the heat sink
    ring=cq.Solid.makeCylinder(17.0,5.0,cq.Vector(0,0,3)).cut(
         cq.Solid.makeCylinder(P['uv_aperture_diameter']/2,5.1,cq.Vector(0,0,3)))
    return shape.fuse(ring)

def oring_coupon():
    handle=rounded_box_xy(32,25,3.5,0,2.5)
    plug=cq.Solid.makeCylinder(P['oring_test_plug_body_diameter']/2,18.0,cq.Vector(0,0,3.5))
    shape=handle.fuse(plug)
    z=11.5; w=P['oring_groove_width']; bottom=P['oring_groove_root_diameter']/2
    sleeve=cq.Solid.makeCylinder(9,w,cq.Vector(0,0,z)).cut(
           cq.Solid.makeCylinder(bottom,w+0.02,cq.Vector(0,0,z-0.01)))
    shape=shape.cut(sleeve)
    # Straight top pilot, no pressured seal in this coupon.
    return shape

PARTS = {
 '01_UV_Shroud_405nm_PROTOTYPE':uv_shroud(),
 '02_Metcal_910B_Syringe_C_Clip_FIT_TEST':clip(),
 '03_Gridfinity_1x1_Purge_Cup_Sarstedt_30ml':cup_holder(),
 '04_Gridfinity_1x1_Nozzle_Dark_Park_PROTOTYPE':nozzle_park(),
 '05_Oring_11x2p5_Groove_Fit_Coupon':oring_coupon(),
}

# Position on CORE One within 250x220, consistent 8+mm spacing, all z=0.
# Layout (all in XY relative to 0; target approx 156 x 126 mm):
PLACEMENTS = {
 '01_UV_Shroud_405nm_PROTOTYPE': (37,37),
 '02_Metcal_910B_Syringe_C_Clip_FIT_TEST': (115,38),
 '03_Gridfinity_1x1_Purge_Cup_Sarstedt_30ml': (26,105),
 '04_Gridfinity_1x1_Nozzle_Dark_Park_PROTOTYPE': (82,105),
 '05_Oring_11x2p5_Groove_Fit_Coupon': (137,105),
}

def to_trimesh(shape):
    vertices,faces=shape.tessellate(0.15)
    V=np.array([[v.x,v.y,v.z] for v in vertices]); F=np.array(faces,dtype=int)
    tm=trimesh.Trimesh(vertices=V,faces=F,process=True)
    # OCC could produce inverse orientation on certain tessellated faces; normalize by signed volume
    if tm.volume < 0: tm.invert()
    return tm

def make_3mf(meshes,targets,output):
    ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
    ET.register_namespace('',ns)
    model=ET.Element(f'{{{ns}}}model',{'unit':'millimeter','xml:lang':'en-US'})
    ET.SubElement(model,f'{{{ns}}}metadata',{'name':'Title'}).text='LAB3 five-part prototype fit-test plate v2'
    resources=ET.SubElement(model,f'{{{ns}}}resources')
    build=ET.SubElement(model,f'{{{ns}}}build')
    for idx,(name,mesh) in enumerate(meshes.items(),1):
        obj=ET.SubElement(resources,f'{{{ns}}}object',{'id':str(idx),'type':'model','name':name})
        elmesh=ET.SubElement(obj,f'{{{ns}}}mesh')
        vert_el=ET.SubElement(elmesh,f'{{{ns}}}vertices')
        tri_el=ET.SubElement(elmesh,f'{{{ns}}}triangles')
        for v in mesh.vertices: ET.SubElement(vert_el,f'{{{ns}}}vertex',{'x':f'{v[0]:.5f}','y':f'{v[1]:.5f}','z':f'{v[2]:.5f}'})
        for face in mesh.faces: ET.SubElement(tri_el,f'{{{ns}}}triangle',{'v1':str(face[0]),'v2':str(face[1]),'v3':str(face[2])})
        dx,dy=targets[name]
        ET.SubElement(build,f'{{{ns}}}item',{'objectid':str(idx),'transform':f'1 0 0 0 1 0 0 0 1 {dx:.4f} {dy:.4f} 0'})
    content=ET.tostring(model,encoding='utf-8',xml_declaration=True)
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        z.writestr('[Content_Types].xml','''<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>''')
        z.writestr('_rels/.rels','''<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>''')
        z.writestr('3D/3dmodel.model',content)

def main():
    meshes={}; summary={}
    for name,solid in PARTS.items():
        assert solid.isValid(), f'INVALID BREP: {name}'
        print(name, solid.Volume(), solid.BoundingBox().xlen, solid.BoundingBox().ylen, solid.BoundingBox().zlen,flush=True)
        cq.exporters.export(solid,str(ROOT/'STEP'/f'{name}.step'))
        cq.exporters.export(solid,str(ROOT/'STL'/f'{name}.stl'),tolerance=0.13,angularTolerance=0.2)
        mesh=trimesh.load_mesh(str(ROOT/'STL'/f'{name}.stl'),process=True)
        if mesh.volume<0:mesh.invert()
        assert mesh.is_watertight,f'NOT WATERTIGHT {name}'
        assert np.all(mesh.bounds[0]>=np.array([-45,-45,-0.02])), name
        assert mesh.bounds[0,2]>=-0.02
        meshes[name]=mesh
        summary[name]={'bbox_mm':np.round(mesh.extents,3).tolist(), 'volume_mm3':round(float(mesh.volume),1), 'watertight':mesh.is_watertight,'triangles':len(mesh.faces)}
    output=ROOT/'3MF'/'LAB3_FIT_TESTS_ONE_PLATE.3mf'
    make_3mf(meshes,PLACEMENTS,output)
    # Validate 3MF contains 5 named independent watertight objects and is within bed footprint.
    bounds=[]
    for name,mesh in meshes.items():
        p=np.array([*PLACEMENTS[name],0.0]);b=mesh.bounds+p;bounds.append(b)
        summary[name]['placement_center_xy_mm'] = list(PLACEMENTS[name])
    bb=np.array(bounds)
    bbox_total=np.vstack((bb[:,0].min(axis=0),bb[:,1].max(axis=0)))
    assert np.all(bbox_total[0,:2]>=0),bbox_total
    assert bbox_total[1,0] < 250 and bbox_total[1,1]<220,bbox_total
    # check XY bounding box overlap (fast conservative check)
    for i in range(len(bounds)):
        for j in range(i+1,len(bounds)):
            a,b=bounds[i],bounds[j]
            overlap=np.minimum(a[1,:2],b[1,:2])-np.maximum(a[0,:2],b[0,:2])
            assert np.any(overlap<0), f'Overlapping bounding boxes {i},{j}: {overlap}'
    ET.fromstring(zipfile.ZipFile(output).read('3D/3dmodel.model'))
    (ROOT/'validation.json').write_text(json.dumps({'parts':summary,'plate_bbox_mm':bbox_total.tolist(), '3mf':str(output.name)},indent=2),encoding='utf8')
    print('Saved:',output, 'total bounds:',bbox_total)

if __name__=='__main__':main()
