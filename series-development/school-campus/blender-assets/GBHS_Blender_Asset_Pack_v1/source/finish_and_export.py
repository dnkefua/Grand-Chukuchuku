import bpy, math, json, sys, bmesh
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
scene=bpy.context.scene

# Render-friendly material corrections: landscape noise in metres, subtle canopy variation.
for name in ['Tropical campus grass','Worn football turf','Brown red laterite earth']:
    m=bpy.data.materials.get(name)
    if m and m.use_nodes:
        nt=m.node_tree;tex=next((n for n in nt.nodes if n.type=='TEX_NOISE'),None)
        if tex:
            geo=nt.nodes.new('ShaderNodeNewGeometry');nt.links.new(geo.outputs['Position'],tex.inputs['Vector']);tex.inputs['Scale'].default_value=.10 if 'grass' in name or 'turf' in name else 1.5
for name in ['Mango foliage','Sunlit tropical foliage']:
    m=bpy.data.materials.get(name)
    if m:
        ramp=next((n for n in m.node_tree.nodes if n.type=='VALTORGB'),None)
        if ramp:
            c=m.diffuse_color
            ramp.color_ramp.elements[0].color=(c[0]*.8,c[1]*.8,c[2]*.8,1)
            ramp.color_ramp.elements[1].color=(c[0]*1.12,c[1]*1.12,c[2]*1.12,1)
for me in bpy.data.meshes:
    if me.name.startswith('Icosphere'):
        for p in me.polygons:p.material_index=0

def box(name,loc,size,mat,col):
    x,y,z=[s/2 for s in size];v=[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)]
    me=bpy.data.meshes.new(name);me.from_pydata(v,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);me.materials.append(mat)
    o=bpy.data.objects.new(name,me);col.objects.link(o);o.location=loc;mod=o.modifiers.new('Furniture_edges','BEVEL');mod.width=.018;mod.segments=2;return o
wood=bpy.data.materials['Worn solid hardwood']
for off,cname in [(0,'10_Classroom_A_First_Day'),(10,'11_Classroom_B_Lessons')]:
    col=bpy.data.collections[cname]
    box('Teacher_chair_seat',(off+.48,5,.71),(.44,.48,.08),wood,col)
    for xx in [off+.31,off+.65]:
        for yy in [4.83,5.17]:box('Teacher_chair_leg',(xx,yy,.47),(.06,.06,.46),wood,col)
    box('Teacher_chair_back',(off+.28,5,1.04),(.065,.48,.6),wood,col)
    # Sunlit practical room: stronger local ceiling bounce, without deleting a roof.
    bpy.data.lights[cname+'_daylight_fill'].energy=320

# Camera framing keeps the three sporting facilities visible in the campus detail.
cam=bpy.data.objects['03_Main_Cluster_Sports'];cam.location=(710,-230,230);cam.rotation_euler=(Vector((710,32,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=38
def newcamera(name,loc,target,lens):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);bpy.data.collections['12_Cameras'].objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.lens=lens;d.clip_start=.05;d.clip_end=6000;return o
newcamera('13_Sports_Aligned_Reverse',(690,145,70),(690,27,0),35)
newcamera('14_Junior_Classroom_Veranda',(28,-16,3.2),(15,5,1.8),27)
scene.frame_set(96)
scene.camera=bpy.data.objects['03_Main_Cluster_Sports']
scene.render.resolution_x=1600;scene.render.resolution_y=900
for c in bpy.data.collections:
    if c.name.startswith(('01_','02_','03_','04_','05_','06_')):
        c.asset_mark();c.asset_data.description='GBHS Kumba editable environment component; proposed reconstruction from creator layout.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'models/GBHS_Campus_Classrooms_v1.blend'))

# Extract complete furnished classroom sets with their actual walls and roofs.
# Geometry crossing the module edges is cut deterministically; no image editing.
def standalone_classroom(off,cname,dest):
    sub=bpy.data.scenes.new(dest)
    sub.world=scene.world
    sub.render.engine='BLENDER_EEVEE'
    sub.unit_settings.system='METRIC'
    group=bpy.data.collections.new(dest+'_Complete_Set');sub.collection.children.link(group)
    sources=list(bpy.data.collections[cname].objects)
    sources+=list(bpy.data.collections['01_Forms_One_Two'].objects)
    sources+=[o for o in bpy.data.collections['13_Lighting'].objects if cname in o.name or o.type=='LIGHT' and o.data.type=='SUN']
    sources+=[bpy.data.objects['07_Classroom_A_Back_To_Board' if off==0 else '10_Classroom_B_Lesson']]
    newobjs={}
    for obj in sources:
        if obj.type in ['MESH','CURVE','FONT']:
            points=[obj.matrix_world@Vector(v) for v in obj.bound_box]
            if max(p.x for p in points)<off-.21 or min(p.x for p in points)>off+10.21:continue
            if max(p.y for p in points)<-.9 or min(p.y for p in points)>15:continue
        elif obj.type=='EMPTY':
            wx=obj.matrix_world.translation.x
            if not off-.21<=wx<=off+10.21:continue
        cp=obj.copy();
        if obj.data:cp.data=obj.data.copy()
        cp.animation_data_clear();group.objects.link(cp);cp.parent=None;cp.matrix_world=obj.matrix_world.copy();newobjs[obj]=cp
        if cp.type=='MESH':
            # Clip only long cross-boundary meshes such as floor, roof and veranda beams.
            points=[cp.matrix_world@Vector(v) for v in cp.bound_box]
            if min(p.x for p in points)<off-.21 or max(p.x for p in points)>off+10.21:
                bm=bmesh.new();bm.from_mesh(cp.data);mx=cp.matrix_world.copy()
                bmesh.ops.transform(bm,matrix=mx,verts=bm.verts)
                for plane,normal in [(off-.21,(-1,0,0)),(off+10.21,(1,0,0))]:
                    geom=list(bm.verts)+list(bm.edges)+list(bm.faces)
                    bmesh.ops.bisect_plane(bm,geom=geom,dist=.0001,plane_co=(plane,0,0),plane_no=normal,clear_outer=True,clear_inner=False)
                bmesh.ops.transform(bm,matrix=mx.inverted(),verts=bm.verts);bm.to_mesh(cp.data);bm.free()
    for old,cp in newobjs.items():
        if old.parent in newobjs:
            mx=cp.matrix_world.copy();cp.parent=newobjs[old.parent];cp.matrix_world=mx
    sub.camera=next(o for o in group.objects if o.type=='CAMERA')
    sub.render.resolution_x=1600;sub.render.resolution_y=900;sub.render.resolution_percentage=100
    group.asset_mark();group.asset_data.description='Complete furnished classroom, walls, windows, rigid door/shutter hinges and camera. From the same campus geometry.'
    bpy.data.libraries.write(str(ROOT/'models'/f'{dest}.blend'),{sub},fake_user=True,compress=True)
    print('CLASSROOM_EXPORTED',dest,len(group.objects),flush=True)
    return sub
standalone_classroom(0,'10_Classroom_A_First_Day','GBHS_Classroom_A_First_Day')
standalone_classroom(10,'11_Classroom_B_Lessons','GBHS_Classroom_B_Lessons')

if '--renders' in sys.argv:
    names=['01_Campus_Whole_Oblique','02_Campus_Plan','03_Main_Cluster_Sports','04_Form_Three_Passage','05_Cafeteria_and_Sports','06_Sixth_Form_and_Gate','07_Classroom_A_Back_To_Board','08_Classroom_A_Teacher_Reverse','09_Classroom_A_Doorway','10_Classroom_B_Lesson','13_Sports_Aligned_Reverse','14_Junior_Classroom_Veranda']
    for name in names:
        scene.camera=bpy.data.objects[name];scene.render.filepath=str(ROOT/'renders'/f'{name}.png')
        bpy.ops.render.render(write_still=True,scene=scene.name);print('FINAL_RENDER',name,flush=True)

# glTF is the portable geometry backup. Shader-node texture variation stays in .blend.
if '--glb' in sys.argv:
    bpy.context.window.scene=scene
    for mat in bpy.data.materials:
        if mat.use_nodes:
            p=mat.node_tree.nodes.get('Principled BSDF')
            if p:
                for link in list(p.inputs['Base Color'].links):mat.node_tree.links.remove(link)
                for link in list(p.inputs['Normal'].links):mat.node_tree.links.remove(link)
                p.inputs['Base Color'].default_value=mat.diffuse_color
    bpy.ops.object.select_all(action='DESELECT')
    for obj in list(scene.objects):
        if obj.type in ['CURVE','FONT']:
            obj.select_set(True);bpy.context.view_layer.objects.active=obj
            bpy.ops.object.convert(target='MESH');obj.select_set(False)
    bpy.ops.export_scene.gltf(filepath=str(ROOT/'models/GBHS_Campus_Classrooms_v1.glb'),export_format='GLB',use_active_scene=True,export_cameras=True,export_lights=True,export_animations=False,export_apply=True)
    print('GLB_EXPORTED',flush=True)
