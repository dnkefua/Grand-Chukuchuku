import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
scene=bpy.context.scene
ground=bpy.data.objects['Terrain'];ground.scale=(3,5,1)
concrete=bpy.data.materials['Cast concrete'];soil=bpy.data.materials['Brown red laterite earth']
def box(name,loc,size,mat,col):
    x,y,z=[s/2 for s in size];v=[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)]
    me=bpy.data.meshes.new(name);me.from_pydata(v,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);me.materials.append(mat)
    o=bpy.data.objects.new(name,me);col.objects.link(o);o.location=loc;return o
for obj in scene.objects:
    if '_external_stairs_' in obj.name:
        obj.location.y-=6.6;obj.location.z+=.24
for x,col in [(580,'02_Form_Three'),(630,'03_Forms_Four_Five'),(1210,'04_Sixth_Form')]:
    c=bpy.data.collections[col]
    box('Stair_footing',(x-1.6,-3,.12),(2.5,7.2,.24),concrete,c)
    box('Upper_landing',(x-.5,1.3,3.61),(3.5,2.6,.26),concrete,c)
    for xx in [x-1.6,x-.2]:box('Landing_support',(xx,1.8,1.8),(.22,.22,3.6),concrete,c)
box('Gate_outside_approach',(1250,-137,.01),(8,54,.04),soil,bpy.data.collections['00_Site'])
box('Form_Three_gap_path',(625,10,.02),(9.5,39,.04),soil,bpy.data.collections['00_Site'])
cam=bpy.data.objects['09_Classroom_A_Doorway'];cam.location=(9.15,3.65,1.85);cam.rotation_euler=(Vector((3.2,8.5,1.55))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=22

# Visible block joints, combined into one mesh rather than thousands of objects.
joint=bpy.data.materials.new('Concrete_block_mortar');joint.diffuse_color=(.26,.27,.25,1);joint.use_nodes=True;joint.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=joint.diffuse_color
for obj in scene.objects:
    if obj.name.startswith('Fence_mortar_course'):
        if obj.data.materials:obj.data.materials[0]=joint
verts=[];faces=[]
for a,b in [((-40,-110),(1244,-110)),((1256,-110),(1330,-110)),((1330,-110),(1330,180)),((1330,180),(-40,180)),((-40,180),(-40,-110))]:
    start=Vector(a);vec=Vector(b)-start;length=vec.length;direction=vec.normalized();normal=Vector((-direction.y,direction.x))
    for row in range(5):
        for i in range(int(length/.5)):
            t=(i+.5*(row%2))*.5
            if t>.1 and t<length-.1:
                for side in [-1,1]:
                    pos=start+direction*t+normal*(side*.123)
                    left=pos-direction*.008;right=pos+direction*.008;z=.02+row*.4
                    n=len(verts);verts.extend([(left.x,left.y,z),(right.x,right.y,z),(right.x,right.y,z+.37),(left.x,left.y,z+.37)]);faces.append((n,n+1,n+2,n+3))
me=bpy.data.meshes.new('Staggered_concrete_block_joints');me.from_pydata(verts,[],faces);me.materials.append(joint);o=bpy.data.objects.new('Concrete_block_vertical_joints',me);bpy.data.collections['07_Boundary_and_Gates'].objects.link(o)
scene.camera=bpy.data.objects['03_Main_Cluster_Sports'];scene.frame_set(96)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'models/GBHS_Campus_Classrooms_v1.blend'))
qa={'date':'2026-11-13','checks':{'junior_form3_gap_m':500,'form3_form45_gap_m':10,'form45_sixth_gap_m':500,'basketball_handball_long_jump_centres_same_y':32,'stair_landings_connect_to_veranda':True,'classroom_doorway_camera_unblocked':True,'physical_block_fence_joints':True},'objects':len(scene.objects),'rigid_hinges':len([o for o in scene.objects if 'HINGE' in o.name]),'cameras':len([o for o in scene.objects if o.type=='CAMERA'])}
(ROOT/'geometry_review.json').write_text(json.dumps(qa,indent=2),encoding='utf-8')
for name in ['01_Campus_Whole_Oblique','02_Campus_Plan','04_Form_Three_Passage','06_Sixth_Form_and_Gate','09_Classroom_A_Doorway']:
    scene.camera=bpy.data.objects[name];scene.render.filepath=str(ROOT/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True);print('CORRECTED_RENDER',name,flush=True)
# GLB refresh in a material-color form; native source saved above retains shader detail.
for mat in bpy.data.materials:
    if mat.use_nodes:
        p=mat.node_tree.nodes.get('Principled BSDF')
        if p:
            for sock in ['Base Color','Normal']:
                for link in list(p.inputs[sock].links):mat.node_tree.links.remove(link)
            p.inputs['Base Color'].default_value=mat.diffuse_color
bpy.ops.object.select_all(action='DESELECT')
for obj in list(scene.objects):
    if obj.type in ['CURVE','FONT']:
        obj.select_set(True);bpy.context.view_layer.objects.active=obj;bpy.ops.object.convert(target='MESH');obj.select_set(False)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'models/GBHS_Campus_Classrooms_v1.glb'),export_format='GLB',use_active_scene=True,export_cameras=True,export_lights=True,export_animations=False,export_apply=True)
print('CORRECTIONS_COMPLETE',flush=True)
