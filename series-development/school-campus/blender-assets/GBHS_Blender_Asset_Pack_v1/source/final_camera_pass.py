import bpy,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
s=bpy.context.scene
for name,loc,target,ortho in [('01_Campus_Whole_Oblique',(-100,-540,580),(645,35,0),1280),('13_Sports_Aligned_Reverse',(700,260,145),(700,32,0),None)]:
    c=bpy.data.objects[name];c.location=loc;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler()
    if ortho:c.data.ortho_scale=ortho
s.camera=bpy.data.objects['07_Classroom_A_Back_To_Board']
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_perspective='CAMERA'
            area.spaces.active.clip_end=6000
            area.spaces.active.overlay.show_overlays=False
            area.spaces.active.shading.type='MATERIAL'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'models/GBHS_Campus_Classrooms_v1.blend'))
manifest=json.loads((ROOT/'asset_manifest.json').read_text())
manifest['objects']=len(s.objects)
manifest['cameras']=[{'name':c.name,'location':list(c.location),'lens':c.data.lens,'type':c.data.type} for c in s.objects if c.type=='CAMERA']
manifest['version']='1.1'
manifest['selected_render_names']=['01_Campus_Whole_Oblique.png','02_Campus_Plan.png','03_Main_Cluster_Sports_v1_1.png','04_Form_Three_Passage.png','05_Cafeteria_and_Sports_v1_1.png','06_Sixth_Form_and_Gate.png','07_Classroom_A_Back_To_Board.png','08_Classroom_A_Teacher_Reverse.png','09_Classroom_A_Doorway.png','10_Classroom_B_Lesson.png','13_Sports_Aligned_Reverse.png','14_Junior_Classroom_Veranda.png']
manifest['superseded_openart_previews']=['03_Main_Cluster_Sports.png','05_Cafeteria_and_Sports.png']
(ROOT/'asset_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
for name,suffix in [('01_Campus_Whole_Oblique',''),('13_Sports_Aligned_Reverse',''),('03_Main_Cluster_Sports','_v1_1'),('05_Cafeteria_and_Sports','_v1_1')]:
    s.camera=bpy.data.objects[name];s.render.filepath=str(ROOT/'renders'/f'{name}{suffix}.png');bpy.ops.render.render(write_still=True);print('FINAL_CAMERA',name,flush=True)
for m in bpy.data.materials:
    if m.use_nodes:
        p=m.node_tree.nodes.get('Principled BSDF')
        if p:
            for sock in ['Base Color','Normal']:
                for link in list(p.inputs[sock].links):m.node_tree.links.remove(link)
            p.inputs['Base Color'].default_value=m.diffuse_color
bpy.ops.object.select_all(action='DESELECT')
for obj in list(s.objects):
    if obj.type in ['CURVE','FONT']:
        obj.select_set(True);bpy.context.view_layer.objects.active=obj;bpy.ops.object.convert(target='MESH');obj.select_set(False)
kwargs=dict(filepath=str(ROOT/'models/GBHS_Campus_Classrooms_v1.glb'),export_format='GLB',use_active_scene=True,export_cameras=True,export_lights=True,export_animations=False,export_apply=True)
if 'use_renderable' in bpy.ops.export_scene.gltf.get_rna_type().properties:kwargs['use_renderable']=True
bpy.ops.export_scene.gltf(**kwargs)
print('FINAL_PACKAGE_GEOMETRY_READY',flush=True)
