import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks=[]
for name in ['GBHS_Classroom_A_First_Day','GBHS_Classroom_B_Lessons']:
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'models'/f'{name}.blend'))
    s=bpy.context.scene
    desks=[o for o in s.objects if '_writing_top' in o.name]
    hinges=[o for o in s.objects if 'HINGE' in o.name]
    assert len(desks)==15,(name,len(desks))
    assert s.camera and s.camera.type=='CAMERA',name
    assert len(hinges)>=5,(name,len(hinges))
    assert any('Chalkboard' in o.name for o in s.objects),name
    checks.append({'file':name+'.blend','opened_successfully':True,'paired_desks':len(desks),'seat_capacity':len(desks)*2,'hinge_controls':len(hinges),'objects':len(s.objects),'camera':s.camera.name})
    if name.endswith('First_Day'):
        s.render.resolution_x=800;s.render.resolution_y=450;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
        s.render.filepath=str(ROOT/'previews/Standalone_Classroom_A_Verification.png');bpy.ops.render.render(write_still=True)
(ROOT/'classroom_file_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print('CLASSROOM_FILES_VERIFIED',checks,flush=True)
