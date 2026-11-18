"""GBHS Kumba: editable production-location reconstruction, Blender 5.x.
Author-supplied relationships take precedence over the older proposed map.
All unsurveyed measurements and classroom details are editable proposals.
No remote services, generation APIs or paid operations are used here.
"""
import bpy, math, random, json, sys
from pathlib import Path
from mathutils import Vector, Matrix

ROOT = Path(__file__).resolve().parents[1]
random.seed(73)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.name='GBHS_Campus_and_First_Days_Classrooms'
scene.unit_settings.system='METRIC'
scene.unit_settings.scale_length=1.0
scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=1600
scene.render.resolution_y=900
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
scene.render.fps=24
scene.frame_start=1
scene.frame_end=96
scene.render.image_settings.color_mode='RGB'
scene.view_settings.view_transform='AgX'
scene.render.image_settings.color_depth='8'
if hasattr(scene,'eevee'):
    for key,val in [('taa_render_samples',32),('taa_samples',16)]:
        if hasattr(scene.eevee,key): setattr(scene.eevee,key,val)

COL={}
def collection(name):
    c=bpy.data.collections.new(name);scene.collection.children.link(c);COL[name]=c;return c
for n in ['00_Site','01_Forms_One_Two','02_Form_Three','03_Forms_Four_Five','04_Sixth_Form','05_Admin_Labs_Canteen','06_Sport_and_Food_Nutrition','07_Boundary_and_Gates','08_North_East_Neighbours','09_Tropical_Landscape','10_Classroom_A_First_Day','11_Classroom_B_Lessons','12_Cameras','13_Lighting','14_Blocking_Markers']:
    collection(n)
active=COL['00_Site']
def use(n):
    global active
    active=COL[n]

def mat(name,color,rough=.7,noise=0,scale=6,metal=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    nt=m.node_tree;p=nt.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    if noise:
        tex=nt.nodes.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=scale;tex.inputs['Detail'].default_value=3
        coord=nt.nodes.new('ShaderNodeTexCoord');nt.links.new(coord.outputs['Generated'],tex.inputs['Vector'])
        ramp=nt.nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].position=.18;ramp.color_ramp.elements[0].color=(*(v*(1-noise) for v in color),1)
        ramp.color_ramp.elements[1].position=.8;ramp.color_ramp.elements[1].color=(*(min(1,v*(1+noise*.4)) for v in color),1)
        nt.links.new(tex.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs['Color'],p.inputs['Base Color'])
        bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.035
        nt.links.new(tex.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],p.inputs['Normal'])
    return m
M={
 'plaster':mat('Warm cream lime plaster',(.68,.55,.36),noise=.24),
 'dado':mat('Ochre lower-wall protective paint',(.33,.19,.09),noise=.25),
 'concrete':mat('Cast concrete',(.42,.40,.34),noise=.3),
 'roof':mat('Weathered galvanized corrugated roof',(.37,.41,.40),.55,.3,12,.35),
 'rust':mat('Oxidized roof sheets',(.30,.12,.055),.8,.4),
 'wood':mat('Worn solid hardwood',(.24,.095,.025),.7,.55,5),
 'deskwood':mat('Honey brown desk timber',(.40,.20,.065),.6,.38,9),
 'metal':mat('Dark blue grey painted steel',(.065,.095,.105),.45,0,6,.25),
 'soil':mat('Brown red laterite earth',(.40,.20,.075),.95,.45,90),
 'grass':mat('Tropical campus grass',(.20,.28,.072),.95,.5,35),
 'pitch':mat('Worn football turf',(.24,.32,.10),.95,.35,28),
 'court':mat('Faded oxide sports concrete',(.42,.19,.10),.9,.3,14),
 'sand':mat('Long jump sand',(.64,.48,.25),.95,.3,20),
 'white':mat('Warm chalk white',(.85,.83,.72),.85),
 'board':mat('Used dark-green chalkboard',(.035,.075,.055),.92,.45,14),
 'paper':mat('Exercise paper ivory',(.82,.78,.65),.82),
 'blue':mat('School notebook blue',(.07,.18,.32),.7),
 'red':mat('School notebook burgundy',(.29,.045,.035),.7),
 'leaf':mat('Mango foliage',(.09,.22,.044),.92,.55,3),
 'leaf2':mat('Sunlit tropical foliage',(.19,.32,.065),.92,.4,3),
 'bark':mat('Tree bark',(.15,.085,.035),.95,.6),
 'orange':mat('Basketball rim',(.62,.20,.035),.5,0,6,.3),
 'water':mat('Water pail blue',(.06,.18,.24),.45),
}
cache={}
def box(name,loc,size,material,bevel=0,parent=None):
    key=tuple(round(v,4) for v in size)+(material.name,)
    mesh=cache.get(key)
    if mesh is None:
        x,y,z=[v/2 for v in size]
        verts=[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)]
        mesh=bpy.data.meshes.new(name+'_mesh');mesh.from_pydata(verts,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);mesh.materials.append(material);cache[key]=mesh
    ob=bpy.data.objects.new(name,mesh);active.objects.link(ob);ob.location=loc
    if bevel:
        mod=ob.modifiers.new('Soft manufactured edges','BEVEL');mod.width=bevel;mod.segments=2
    if parent: ob.parent=parent
    return ob

def empty(name,loc):
    ob=bpy.data.objects.new(name,None);active.objects.link(ob);ob.location=loc;ob.empty_display_type='ARROWS';ob.empty_display_size=.3;return ob

def cyl(name,a,b,r,material,verts=12):
    a,b=Vector(a),Vector(b);d=b-a
    key=('cyl',round(r,4),round(d.length,4),verts,material.name)
    mesh=cache.get(key)
    if mesh is None:
        v=[(r*math.cos(t*2*math.pi/verts),r*math.sin(t*2*math.pi/verts),z) for z in [-d.length/2,d.length/2] for t in range(verts)]
        f=[tuple(reversed(range(verts))),tuple(range(verts,2*verts))]+[(i,(i+1)%verts,(i+1)%verts+verts,i+verts) for i in range(verts)]
        mesh=bpy.data.meshes.new(name+'_mesh');mesh.from_pydata(v,[],f);mesh.materials.append(material);cache[key]=mesh
    ob=bpy.data.objects.new(name,mesh);active.objects.link(ob);ob.location=(a+b)/2;ob.rotation_euler=d.to_track_quat('Z','Y').to_euler();return ob

def line(name,points,r,material,closed=False):
    c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=1;c.bevel_depth=r;c.bevel_resolution=1
    sp=c.splines.new('POLY');sp.points.add(len(points)-1)
    for p,v in zip(sp.points,points):p.co=(*v,1)
    sp.use_cyclic_u=closed;c.materials.append(material);ob=bpy.data.objects.new(name,c);active.objects.link(ob);return ob

def rectline(name,cx,cy,w,h,z=.08,r=.06):
    return line(name,[(cx-w/2,cy-h/2,z),(cx+w/2,cy-h/2,z),(cx+w/2,cy+h/2,z),(cx-w/2,cy+h/2,z)],r,M['white'],True)

def ring(name,cx,cy,radius,z=.08,material=None,width=.06):
    return line(name,[(cx+radius*math.cos(i*2*math.pi/64),cy+radius*math.sin(i*2*math.pi/64),z) for i in range(64)],width,material or M['white'],True)

def text(name,body,loc,size,normal=(0,-1,0),material=None):
    c=bpy.data.curves.new(name,'FONT');c.body=body;c.align_x='CENTER';c.align_y='CENTER';c.size=size;c.extrude=.0007;c.materials.append(material or M['white'])
    ob=bpy.data.objects.new(name,c);active.objects.link(ob);ob.location=loc
    n=Vector(normal);up=Vector((0,0,1));right=up.cross(n).normalized()
    ob.rotation_euler=Matrix((right,up,n)).transposed().to_euler();return ob

def roof(name,cx,cy,w,d,z,rise=2):
    # Continuous pitched mesh with physical corrugations; ridge runs along X.
    n=max(12,int(w/.22));verts=[];faces=[]
    for i in range(n+1):
        x=cx-w/2+w*i/n;wave=.04*math.cos(i*math.pi)
        verts.extend([(x,cy-d/2,z+wave),(x,cy,z+rise+wave),(x,cy+d/2,z+wave)])
    for i in range(n):
        for j in range(2):faces.append((i*3+j,(i+1)*3+j,(i+1)*3+j+1,i*3+j+1))
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(M['roof']);me.materials.append(M['rust'])
    for p in me.polygons:p.material_index=1 if (p.index//2)%37<3 else 0
    ob=bpy.data.objects.new(name,me);active.objects.link(ob)
    cyl(name+'_ridge',(cx-w/2,cy,z+rise+.08),(cx+w/2,cy,z+rise+.08),.085,M['roof'])
    for x in [cx-w/2+.15,cx+w/2-.15]:
        me2=bpy.data.meshes.new(name+'_gable');me2.from_pydata([(x,cy-d/2+.4,z),(x,cy,z+rise),(x,cy+d/2-.4,z)],[],[(0,1,2)]);me2.materials.append(M['plaster']);o=bpy.data.objects.new(name+'_gable',me2);active.objects.link(o)
    return ob

def wall_with_openings(name,x0,x1,y,zbase,height,openings,thick=.25):
    # Opening bounds are in world X and height above local floor; build wall piers/lintels.
    xs=sorted(set([x0,x1]+[v for op in openings for v in op[:2]]))
    for a,b in zip(xs,xs[1:]):
        mid=(a+b)/2
        op=next((o for o in openings if o[0]<=mid<=o[1]),None)
        spans=[(0,height)] if op is None else [(0,op[2]),(op[3],height)]
        for lo,hi in spans:
            if hi-lo<.01:continue
            # Ochre dado is geometry, not a texture that shifts between angles.
            cuts=sorted(set([lo,hi]+([1.0] if lo<1<hi else [])))
            for p,q in zip(cuts,cuts[1:]):box(name+'_masonry',((a+b)/2,y,zbase+(p+q)/2),(b-a,thick,q-p),M['dado'] if q<=1.001 else M['plaster'])

def window(name,cx,y,z,wide=2.0,high=1.55,animate=False):
    for xx in [cx-wide/2-.05,cx+wide/2+.05]:box(name+'_jamb',(xx,y,z),( .09,.2,high+.18),M['wood'])
    for zz in [z-high/2-.05,z+high/2+.05]:box(name+'_sill',(cx,y,zz),(wide+.2,.28,.11),M['wood'])
    box(name+'_center',(cx,y,z),(.065,.12,high),M['metal'])
    for t in [-.6,0,.6]:box(name+'_security_bar',(cx+t,y,z),(.035,.05,high),M['metal'])
    for side in [-1,1]:
        pivot=empty(name+('_Left_HINGE' if side==-1 else '_Right_HINGE'),(cx+side*wide/2,y-.16,z-high/2))
        pivot['control']='Rotate local Z; rigid shutter. Never scale or morph.'
        leaf=box(name+'_shutter',(-side*wide/4,0,high/2),(wide/2-.035,.065,high-.035),M['wood'],.01,parent=pivot)
        for k in range(6):box(name+'_louvre',(-side*wide/4,-.04,.13+k*(high-.15)/6),(wide/2-.1,.045,.055),M['dado'],parent=pivot)
        pivot.rotation_euler.z=side*math.radians(155)
        if animate:
            for frame,deg in [(1,155),(25,155),(72,25),(96,25)]:pivot.rotation_euler.z=side*math.radians(deg);pivot.keyframe_insert('rotation_euler',frame=frame)
    return

def door(name,x,y,z,width=1.2,angle=-82,animated=False):
    for xx in [x-.06,x+width+.06]:box(name+'_jamb',(xx,y,z+1.2),(.11,.27,2.5),M['wood'])
    box(name+'_lintel',(x+width/2,y,z+2.46),(width+.24,.27,.13),M['wood'])
    hinge=empty(name+'_HINGE',(x,y-.14,z));hinge['control']='Rotate local Z about the hinge; rigid geometry.'
    box(name+'_leaf',(width/2,0,1.2),(width-.04,.075,2.38),M['wood'],.02,hinge)
    for zz in [.35,1.98]:box(name+'_brace',(width/2,-.055,zz),(width-.12,.055,.12),M['dado'],parent=hinge)
    box(name+'_handle',(width-.18,-.11,1.02),(.10,.10,.035),M['metal'],parent=hinge)
    hinge.rotation_euler.z=math.radians(angle)
    if animated:
        for f,ang in [(1,0),(12,0),(64,angle),(96,angle)]:hinge.rotation_euler.z=math.radians(ang);hinge.keyframe_insert('rotation_euler',frame=f)
    return hinge

def stairs(name,x,y,height):
    n=22;run=6.6
    for i in range(n):box(name+'_step',(x,y+run*i/n,(i+1)*height/n/2),(2.2,run/n+.02,(i+1)*height/n),M['concrete'])
    for dx in [-1.0,1.0]:
        cyl(name+'_handrail',(x+dx,y-.2,.95),(x+dx,y+run,height+.95),.045,M['metal'])
        for i in [0,5,11,17,21]:cyl(name+'_post',(x+dx,y+i*run/n,(i+1)*height/n),(x+dx,y+i*run/n,(i+1)*height/n+.95),.035,M['metal'])

def block(name,x0,x1,y0,y1,floors,room_width=10,interior=False):
    width=x1-x0;depth=y1-y0;h=3.5
    box(name+'_foundation',((x0+x1)/2,(y0+y1)/2,.12),(width+.6,depth+.5,.24),M['concrete'])
    rooms=round(width/room_width);rw=width/rooms
    for floor in range(floors):
        z=.24+floor*h
        if floor:box(name+'_upper_slab',((x0+x1)/2,(y0+y1)/2,z-.13),(width+.25,depth+.2,.26),M['concrete'])
        for j in range(rooms):
            a=x0+j*rw;b=a+rw
            for side,yy in [('front',y0+3),('rear',y1)]:
                ops=[(a+1.4,a+3.4,1.1,2.65),(a+4.5,a+6.5,1.1,2.65)]
                if side=='front':ops.append((b-1.65,b-.45,0,2.4))
                else:ops.append((b-3,b-1,1.1,2.65))
                wall_with_openings(name+f'_{floor}_{j}_{side}',a,b,yy,z,h-.2,ops)
                for k,op in enumerate(ops):
                    if op[2]==0:
                        door(name+f'_F{floor}_R{j}_DOOR',op[0],yy,z,animated=(interior and j==0))
                    else:window(name+f'_F{floor}_R{j}_{side}_W{k}',(op[0]+op[1])/2,yy,z+(op[2]+op[3])/2,op[1]-op[0],op[3]-op[2])
            # Real partitions: furnished rooms fit inside the same campus shell.
            box(name+'_partition',(a,y0+(depth+3)/2,z+(h-.2)/2),(.24,depth-3,h-.2),M['plaster'])
            box(name+'_ceiling',((a+b)/2,y0+(depth+3)/2,z+h-.22),(rw,depth-3,.12),M['plaster'])
            for xx in [a,a+rw/2]:box(name+'_veranda_column',(xx,y0+.2,z+(h-.1)/2),(.28,.30,h-.1),M['plaster'])
        box(name+'_end_wall',(x1,y0+(depth+3)/2,z+(h-.2)/2),(.24,depth-3,h-.2),M['plaster'])
        box(name+'_veranda_beam',((x0+x1)/2,y0+.2,z+h-.25),(width,.35,.32),M['plaster'])
        if floor:
            for zh in [.12,.9]:box(name+'_balcony_rail',((x0+x1)/2,y0+.25,z+zh),(width,.065,.065),M['metal'])
            for i in range(int(width/.65)+1):box(name+'_baluster',(x0+i*.65,y0+.25,z+.51),(.032,.04,.85),M['metal'])
    roof(name+'_ROOF',(x0+x1)/2,(y0+y1)/2,width+1.2,depth+1.7,.24+floors*h,2.0)
    text(name+'_sign',name.replace('_',' ').upper(),((x0+x1)/2,y0-.025,2.95),.50,material=M['metal'])
    if floors==2:stairs(name+'_external_stairs',x0-1.6,y0+.3,3.5)
    return

use('00_Site')
box('Terrain', (645,30,-.38),(1700,700,.7),M['grass'])
box('Earth_under_campus',(645,35,-.05),(1370,290,.10),M['grass'])
box('Academic_red_earth_walk',(645,-8,.005),(1290,7,.025),M['soil'])
# Road from gate nearest Sixth Form to cafeteria, kept clear of the sports strip.
box('Gate_road_to_cafeteria_long',(1030,-48,.015),(450,7,.04),M['soil'])
box('Gate_road_entry',(1250,-77,.02),(8,66,.04),M['soil'])
box('Cafeteria_road_arrival',(814,-22,.02),(7,52,.04),M['soil'])
box('Admin_court',(688,60,.015),(48,24,.04),M['soil'])
box('Junior_walk',(40,-12,.02),(82,12,.04),M['soil'])

use('01_Forms_One_Two');block('Forms_One_and_Two',0,80,0,14,1,interior=True)
use('02_Form_Three');block('Form_Three',580,620,0,16,2)
use('03_Forms_Four_Five');block('Forms_Four_and_Five',630,710,0,16,2)
use('04_Sixth_Form');block('Lower_and_Upper_Sixth',1210,1290,0,16,2)
use('05_Admin_Labs_Canteen');block('Main_Office',665,710,75,95,1,room_width=11.25)
block('Physics_Biology_Chemistry_Labs',722,782,0,24,1)
# Open-sided cafeteria with serving counters and reusable benches.
for x in [794,804,814,824,834]:
    for y in [0,24]:box('Cafeteria_pillar',(x,y,1.9),(.32,.32,3.8),M['plaster'])
box('Cafeteria_slab',(814,12,.1),(41,25,.2),M['concrete']);roof('Cafeteria_roof',814,12,42,27,3.9,2.2)
for x in [800,810,820,830]:
    box('Food_vendor_counter',(x,21,.9),(6,1.3,1.8),M['dado'])
    box('Food_counter_top',(x,21,1.82),(6.1,1.45,.12),M['deskwood'])
    for y in [5,12]:
        box('Canteen_table',(x,y,.77),(5,1.0,.09),M['deskwood'])
        for dx in [-1.7,1.7]:box('Table_support',(x+dx,y,.37),(.12,.7,.74),M['metal'])
        for dy in [-.9,.9]:
            box('Canteen_bench',(x,y+dy,.43),(5,.35,.09),M['wood'])
            for dx in [-1.7,1.7]:box('Bench_leg',(x+dx,y+dy,.2),(.12,.22,.4),M['metal'])
text('Cafeteria_sign','CAFETERIA',(814,-.25,3.25),.62,material=M['metal'])

use('06_Sport_and_Food_Nutrition')
block('Food_and_Nutrition',532,558,72,88,1,room_width=13)
cx,cy=470,32
box('Football_field',(cx,cy,.025),(113,76,.04),M['pitch']);rectline('Football_touchlines',cx,cy,105,68)
line('Football_halfway',[(cx,cy-34,.09),(cx,cy+34,.09)],.07,M['white']);ring('Football_centre_circle',cx,cy,9.15)
for side in [-1,1]:
    gx=cx+side*52.5
    rectline('Penalty_area',gx-side*8.25,cy,16.5,40.32)
    rectline('Goal_area',gx-side*2.75,cy,5.5,18.32)
    for yy in [-3.66,3.66]:cyl('Goalpost',(gx,cy+yy,.1),(gx,cy+yy,2.44),.065,M['white'])
    cyl('Goal_crossbar',(gx,cy-3.66,2.44),(gx,cy+3.66,2.44),.065,M['white'])
    for yy in [-3.66,3.66]:line('Goal_support',[(gx,cy+yy,2.44),(gx+side*1.5,cy+yy,.1),(gx,cy+yy,.1)],.04,M['metal'])
    for j in range(12):line('Goal_net',[(gx,cy-3.66+j*.665,2.4),(gx+side*1.5,cy-3.66+j*.665,.1)],.009,M['white'])

def court(name,cx,cy,w,d):
    box(name+'_surface',(cx,cy,.04),(w+4,d+4,.08),M['court']);rectline(name+'_lines',cx,cy,w,d,z=.09,r=.045)
    line(name+'_midline',[(cx,cy-d/2,.1),(cx,cy+d/2,.1)],.045,M['white']);ring(name+'_centre',cx,cy,1.8,z=.1,width=.045)
court('Basketball',595,32,28,15)
for side in [-1,1]:
    x=595+side*15
    cyl('Hoop_post',(x,32,.1),(x,32,3.7),.1,M['metal'])
    box('Backboard',(x-side*.9,32,3.45),(.10,1.8,1.05),M['white'])
    ring('Basketball_rim',x-side*1.35,32,.23,z=3.05,material=M['orange'],width=.025)
    rectline('Basketball_key',595+side*11,32,6,4.9,z=.1,r=.04)
court('Handball',651,32,40,20)
for side in [-1,1]:
    x=651+side*20
    for y in [30.5,33.5]:cyl('Handball_post',(x,y,.1),(x,y,2.1),.055,M['white'])
    cyl('Handball_bar',(x,30.5,2.1),(x,33.5,2.1),.055,M['white'])
box('Long_jump_runway',(767,32,.06),(48,1.4,.09),M['court'])
box('Long_jump_takeoff_board',(789.5,32,.12),(.25,1.4,.04),M['white'])
box('Long_jump_sandpit',(796,32,.035),(9,3,.06),M['sand']);rectline('Sandpit_border',796,32,9,3,z=.07,r=.08)

use('07_Boundary_and_Gates')
def fence_segment(a,b):
    a,b=Vector(a),Vector(b);length=(b-a).length;steps=math.ceil(length/5);step=(b-a)/steps
    for i in range(steps):
        p=a+step*(i+.5);s=(step.length-.22,.22,2.2)
        o=box('Concrete_block_fence_panel',(p.x,p.y,1.1),s,M['concrete']);o.rotation_euler.z=math.atan2(step.y,step.x)
        # Mortar courses on both sides, deterministic physical grooves.
        for zz in [.4,.8,1.2,1.6,2.0]:
            o=box('Fence_mortar_course',(p.x,p.y,zz),(s[0],.235,.018),M['dado']);o.rotation_euler.z=math.atan2(step.y,step.x)
    for i in range(steps+1):
        p=a+step*i;box('Fence_pier',(p.x,p.y,1.18),(.38,.38,2.36),M['concrete'])
for a,b in [((-40,-110,0),(1244,-110,0)),((1256,-110,0),(1330,-110,0)),((1330,-110,0),(1330,180,0)),((1330,180,0),(-40,180,0)),((-40,180,0),(-40,-110,0))]:fence_segment(a,b)
for x in [1244,1256]:box('Main_gate_pier',(x,-110,2.7),(.8,.8,5.4),M['plaster'])
box('GBHS_gate_arch',(1250,-110,5.15),(12.8,.65,1.05),M['plaster'])
text('Gate_school_name','GBHS KUMBA',(1250,-110.35,5.15),.65,material=M['metal'])
for side in [-1,1]:
    pivot=empty('GATE_LEFT_HINGE' if side==-1 else 'GATE_RIGHT_HINGE',(1250+side*6,-110,0))
    pivot['control']='Rotate Z to open the steel gate. World-space fixed hinge.'
    box('Gate_lower_panel',(-side*3,0,.5),(5.8,.09,1),M['metal'],parent=pivot)
    for i in range(16):box('Gate_bar',(-side*(.2+i*.36),0,1.65),(.035,.05,2.3),M['metal'],parent=pivot)
    box('Gate_top_rail',(-side*3,0,2.8),(5.8,.08,.08),M['metal'],parent=pivot)
    pivot.rotation_euler.z=side*math.radians(70)

# Efficient instanced trees keep the environment reusable on a modest laptop.
use('09_Tropical_Landscape')
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1)
proto=bpy.context.object;leafmesh=proto.data;leafmesh.materials.append(M['leaf']);leafmesh.materials.append(M['leaf2'])
for p in leafmesh.polygons:p.material_index=1 if p.index%5==0 else 0;p.use_smooth=True
bpy.data.objects.remove(proto,do_unlink=True)
def tree(x,y,size=7):
    cyl('Mango_trunk',(x,y,0),(x,y,size*.67),size*.047,M['bark'],10)
    for dx,dy,dz,s in [(-.2,0,.74,.35),(.22,.1,.77,.36),(0,-.19,.95,.39)]:
        o=bpy.data.objects.new('Mango_canopy',leafmesh);active.objects.link(o);o.location=(x+dx*size,y+dy*size,dz*size);o.scale=(s*size,s*size,s*size*.86)
for x,y in [(100,80),(165,40),(240,75),(320,30),(385,85),(550,-40),(580,110),(740,110),(855,80),(900,60),(975,80),(1095,80),(1170,-35),(1300,75),(100,-55),(250,-60),(350,-70),(715,-65),(60,110),(70,-45)]:tree(x,y,random.uniform(7,13))
for i in range(140):
    if i<95:x=random.uniform(-120,1400);y=random.uniform(-245,-130)
    else:x=random.uniform(-170,-60);y=random.uniform(-100,240)
    tree(x,y,random.uniform(7,17))
use('08_North_East_Neighbours')
housemats=[mat('Neighbour_plaster_'+str(i),c,noise=.25) for i,c in enumerate([(.55,.36,.18),(.52,.47,.34),(.37,.39,.30),(.44,.23,.13)])]
def house(x,y,i):
    w=random.uniform(9,17);d=random.uniform(7,13);h=random.choice([3.5,4.0,6.3])
    box('Neighbour_house',(x,y,h/2),(w,d,h),housemats[i%4]);roof('Neighbour_roof',x,y,w+1,d+1,h,2)
    for dx in [-w*.28,w*.25]:box('Neighbour_window',(x+dx,y-d/2-.02,1.8),(1.5,.08,1.3),M['wood'])
for i in range(50):house(-5+i*27,random.uniform(210,250),i)
for i in range(10):house(random.uniform(1360,1400),-85+i*29,i)

def desk(name,x,y):
    # Two-pupil desk: seats face west toward the chalkboard.
    box(name+'_writing_top',(x,y,.81),(.56,1.72,.075),M['deskwood'],.015)
    box(name+'_book_shelf',(x,y,.58),(.46,1.54,.055),M['wood'],.008)
    for dx in [-.19,.19]:
        for dy in [-.68,.68]:box(name+'_desk_leg',(x+dx,y+dy,.4),(.065,.065,.8),M['metal'])
    box(name+'_bench',(x+.57,y,.46),(.32,1.72,.075),M['wood'],.012)
    for dy in [-.66,.66]:box(name+'_bench_leg',(x+.57,y+dy,.21),(.08,.08,.42),M['metal'])
    return

def classroom(offset,col,variant):
    use(col)
    z=.24
    # Blackboard is on the west partition; daylight openings stay north/south.
    box('Board_frame',(offset+.19,8.5,2.03),(.12,5.6,1.8),M['wood'],.015)
    box('Chalkboard',(offset+.265,8.5,2.03),(.025,5.38,1.59),M['board'])
    box('Chalk_tray',(offset+.34,8.5,1.18),(.25,5.5,.07),M['wood'])
    if variant=='first_day':
        text('First_day_blackboard','WELCOME TO\nGBHS KUMBA\n\nFORM ONE',(offset+.287,8.5,2.15),.30,(1,0,0))
    else:
        text('Lesson_blackboard','MATHEMATICS\n\n24 + 18 = 42\n36 / 6 = 6\n\nShow your working.',(offset+.287,8.5,2.10),.25,(1,0,0))
    for i in range(5):
        for j in range(3):
            xx=offset+2.5+i*1.35;yy=4.8+j*3.05
            desk(f'{variant}_R{i+1}_PAIR{j+1}',xx,yy)
            if (i+j)%3!=0:
                ob=box('Exercise_book',(xx-.025,yy+.36,.86),(.39,.28,.025),M['blue'] if (i+j)%2 else M['red'],.005)
                ob.rotation_euler.z=random.uniform(-.16,.16)
                box('Book_pages',(xx-.025,yy+.36,.874),(.36,.25,.01),M['paper'])
                cyl('Pencil',(xx-.16,yy+.10,.875),(xx+.10,yy+.15,.875),.009,M['dado'],6)
            marker=empty(f'{variant}_Seat_R{i+1}_C{j+1}',(xx+.57,yy,.24));marker.hide_render=True
            marker['purpose']='Optional paired pupil blocking position, no character or identity implied.'
    # Lift furnished units onto the slab: desk heights are measured from floor.
    for ob in list(active.objects):
        if ob.name.startswith(('first_day_R','lesson_R','Exercise_book','Book_pages','Pencil')) and not ob.parent:ob.location.z+=.24
    box('Teacher_desk_top',(offset+1.25,5.0,1.04),(1.05,1.8,.09),M['deskwood'],.02)
    for dx in [-.4,.4]:
        for dy in [-.7,.7]:box('Teacher_desk_leg',(offset+1.25+dx,5+dy,.63),(.09,.09,.78),M['wood'])
    box('Class_register',(offset+1.3,5.2,1.11),(.47,.34,.04),M['red'],.005)
    text('Register_cover','CLASS REGISTER',(offset+1.3,5.2,1.135),.045,normal=(0,-1,0),material=M['white']).hide_render=True
    # A clock, pinned paper and bag hooks add practical staging details.
    box('Noticeboard',(offset+9.8,5.3,2.1),(.08,1.8,1.3),M['wood'])
    for yy in [4.8,5.35,5.8]:box('Pinned_class_sheet',(offset+9.75,yy,2.15),(.012,.37,.53),M['paper'])
    for yy in [6.6,7.0,7.4]:cyl('Bag_hook',(offset+9.75,yy,1.45),(offset+9.55,yy,1.45),.02,M['metal'])
    # Ceiling lights are fixed fixtures, not modern screens or computer equipment.
    for xx in [offset+3,offset+7]:box('Fluorescent_fixture',(xx,8.5,3.46),(1.2,.14,.08),M['white'])
    # Soft fill mimics bounced daylight through the real openings.
    ld=bpy.data.lights.new(col+'_daylight_fill','AREA');ld.energy=180;ld.shape='RECTANGLE';ld.size=6;ld.size_y=4
    lo=bpy.data.objects.new(col+'_daylight_fill',ld);COL['13_Lighting'].objects.link(lo);lo.location=(offset+5,8.5,3.2)
    return
classroom(0,'10_Classroom_A_First_Day','first_day')
classroom(10,'11_Classroom_B_Lessons','lesson')

use('13_Lighting')
world=bpy.data.worlds.new('Humid Cameroon daylight');scene.world=world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.48,.65,.83,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.6
ld=bpy.data.lights.new('Late_morning_sun','SUN');ld.energy=3.1;ld.angle=math.radians(15)
sun=bpy.data.objects.new('Late_morning_sun',ld);active.objects.link(sun);sun.rotation_euler=(math.radians(24),math.radians(-28),math.radians(-32))

cameras=[]
use('12_Cameras')
def camera(name,loc,target,lens=35,ortho=None):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);active.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y').to_euler();d.lens=lens;d.clip_start=.05;d.clip_end=6000
    if ortho:d.type='ORTHO';d.ortho_scale=ortho
    cameras.append(o);return o
camera('01_Campus_Whole_Oblique',(645,-850,670),(645,25,0),ortho=1470)
camera('02_Campus_Plan',(645,35,1600),(645,35,0),ortho=1470)
camera('03_Main_Cluster_Sports',(699,-185,155),(699,35,0),lens=35)
camera('04_Form_Three_Passage',(625,-16,1.9),(625,25,2.3),lens=22)
camera('05_Cafeteria_and_Sports',(845,65,16),(720,27,2),lens=32)
camera('06_Sixth_Form_and_Gate',(1217,-132,10),(1250,-85,3),lens=30)
camera('07_Classroom_A_Back_To_Board',(9.15,8.3,1.85),(.35,8.4,1.75),lens=20)
camera('08_Classroom_A_Teacher_Reverse',(.80,8.4,1.85),(9.4,8.4,1.5),lens=20)
camera('09_Classroom_A_Doorway',(8.85,1.35,1.85),(5.6,8.1,1.5),lens=22)
camera('10_Classroom_B_Lesson',(19.15,8.3,1.85),(10.35,8.4,1.75),lens=20)
cam=camera('11_Classroom_A_Slow_Dolly',(9.15,8.3,1.85),(.35,8.4,1.75),lens=22)
for f,xx in [(1,9.15),(96,7.45)]:cam.location.x=xx;cam.keyframe_insert('location',frame=f)
cam=camera('12_Campus_Cluster_Dolly',(705,-180,108),(705,28,0),lens=35)
for f,xx in [(1,695),(96,715)]:cam.location.x=xx;cam.rotation_euler=(Vector((705,28,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f)

scene.frame_set(96)
scene.camera=cameras[2]
scene['PROJECT']='Grand Chukuchuku — GBHS campus and first-days classroom environment assets'
scene['CANON']='User confirmed 13 November 2026: Episodes 2 and 3 follow the first-days-at-GBHS sequence, not the older Well Water/Lunch Money numbering.'
scene['SCALE_STATUS']='Proposed reconstruction. 500 m / 10 m / 500 m separations retain the existing edge interpretation. Footprints and classroom fittings are design proposals, not measured survey.'
scene['SPORTS_LOCK']='Football between Forms 1 and 3. Basketball starts beside Form 3; basketball, handball and long jump share Y=32. Jump sandpit immediately beside cafeteria.'
scene['SET_DISTINCTION']='GBHS campus is separate from the Professional School opposite Zino compound. Do not add compound, mango well courtyard or landlord to this campus.'
scene['CREDIT_COST']='Built and rendered locally. No OpenArt generation submitted.'

readme=bpy.data.texts.new('READ_ME_GBHS_ASSET_PACK')
readme.write('GBHS KUMBA | Grand Chukuchuku\n\nEditable environment reconstruction. Metres.\nSelect named cameras from 12_Cameras. Furnished Form One rooms A and B are built inside the actual campus block, not disconnected replicas.\nDoor and gate HINGE empties rotate rigid panels about Z. Timeline 1-96 opens the Classroom A door and contains two four-second camera moves.\nNo character likenesses, crowds or dialogue are generated in this environment pack.\nClassroom A: first-day welcome; classroom B: generic first-lessons arithmetic. Text and seating remain proposed, editable set dressing.\nPhysical materials and geometry remain consistent between views.\nOpenArt receives rendered PNG/MP4 references; .blend and GLB remain the editable local source.\n')
# Useful initial viewport when the file is opened in Blender.
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_distance=300
            area.spaces.active.region_3d.view_location=(700,25,0)
            area.spaces.active.clip_end=6000

manifest={
 'title':'GBHS Kumba campus and first-days classroom asset pack',
 'version':'1.0', 'date':'2026-11-13','blender_version':bpy.app.version_string,
 'units':'metres','status':'Editable reconstruction for creator review; unsurveyed dimensions and classroom fittings proposed',
 'episode_direction':'First days at GBHS after the pilot (creator confirmed)',
 'cameras':[{'name':c.name,'location':list(c.location),'lens':c.data.lens,'type':c.data.type} for c in cameras],
 'classrooms':{'A':{'bounds':[0,10,3,14],'seats':30,'purpose':'First day, arrival, welcome, teacher/pupil reverses'},'B':{'bounds':[10,20,3,14],'seats':30,'purpose':'First lessons and reusable dialogue coverage'}},
 'geometry_checks':{'form_1_to_form_3_gap_m':580-80,'form_3_to_forms_4_5_gap_m':630-620,'forms_4_5_to_sixth_gap_m':1210-710,'sports_centerline_y':32,'boundary':[-40,1330,-110,180]},
 'objects':len(bpy.data.objects),'collections':list(COL),
 'no_paid_generation':True
}
(ROOT/'asset_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'models/GBHS_Campus_Classrooms_v1.blend'))
print('GBHS_BUILD_SAVED',len(bpy.data.objects),'objects',flush=True)
if '--render-preview' in sys.argv:
    scene.render.resolution_x=1280;scene.render.resolution_y=720
    for name in ['03_Main_Cluster_Sports','07_Classroom_A_Back_To_Board','08_Classroom_A_Teacher_Reverse']:
        scene.camera=bpy.data.objects[name];scene.render.filepath=str(ROOT/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
