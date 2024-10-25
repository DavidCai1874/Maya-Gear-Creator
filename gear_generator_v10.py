import maya.cmds as cmds

def create_gear(teeth=20, inner_radius=0.0, outer_radius=1, length=0.3, height=1, bevel=False):
    # delete existing gear
    if cmds.objExists('gear'):
        cmds.delete('gear')
    
    subdivisions = teeth * 2
    
    thickness = outer_radius - inner_radius
    
    #polyPipe
    gear_transform, gear_history = cmds.polyPipe(name='gear', radius=outer_radius, height=height, thickness=thickness, subdivisionsAxis=subdivisions)
    
    #select side faces for gear teeth
    teeth_faces = range(subdivisions * 2, subdivisions * 3, 2)
    cmds.select(clear=True)
    
    # extrude selected faces
    for face_id in teeth_faces:
        cmds.select(f"{gear_transform}.f[{face_id}]", add=True)
    
    cmds.polyExtrudeFacet(localTranslateZ=length)
    
    # if checked bevel option
    if bevel:
        cmds.polyBevel3(offset=0.1, segments=1, offsetAsFraction=False)
        
    return gear_transform, gear_history

# realtime adjustment
def update_gear(*args):
    # get values from window
    teeth = cmds.intSliderGrp('teethSlider', q=True, value=True)
    inner_radius = cmds.floatSliderGrp('innerRadiusSlider', q=True, value=True)
    outer_radius = cmds.floatSliderGrp('outerRadiusSlider', q=True, value=True)
    height = cmds.floatSliderGrp('heightSlider', q=True, value=True)
    length = cmds.floatSliderGrp('lengthSlider', q=True, value=True)
    bevel = cmds.checkBox('bevelCheckbox', q=True, value=True)
    
    # make sure inner radius is smaller than outer
    if inner_radius >= outer_radius:
        inner_radius = outer_radius - 0.01
        cmds.floatSliderGrp('innerRadiusSlider', edit=True, value=inner_radius)
    
    create_gear(teeth, inner_radius, outer_radius, height, length, bevel)

# UI window setup for gear creator
def create_gear_window():
    if cmds.window("gearWindow", exists=True):
        cmds.deleteUI("gearWindow")
        
    cmds.window("gearWindow", title="Procedural Gear Creator", widthHeight=(300, 250))
    
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.intSliderGrp('teethSlider', label='Teeth Count', min=5, max=50, value=20, step=1, field=True, dragCommand=update_gear)
    cmds.floatSliderGrp('innerRadiusSlider', label='Inner Radius', min=0.0, max=5.0, value=0.5, step=0.1, field=True, dragCommand=update_gear)
    cmds.floatSliderGrp('outerRadiusSlider', label='Outer Radius', min=0.5, max=10.0, value=2.0, step=0.1, field=True, dragCommand=update_gear)
    cmds.floatSliderGrp('lengthSlider', label='Tooth Length', min=0.1, max=2.0, value=0.3, step=0.1, field=True, dragCommand=update_gear)
    cmds.floatSliderGrp('heightSlider', label='Gear Height', min=0.1, max=5.0, value=0.5, step=0.1, field=True, dragCommand=update_gear)
    
    #bevel
    cmds.checkBox('bevelCheckbox', label='Bevel Gear Teeth', value=False, changeCommand=update_gear)
    
    #finalize gear creation
    cmds.button(label="Create Gear", command=update_gear)
    
    cmds.showWindow("gearWindow")

#call window
create_gear_window()
