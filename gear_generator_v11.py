import maya.cmds as cmds

#create gear
def create_gear(teeth=20, inner_radius=0.0, outer_radius=2.0, height=0.5, length=0.3, bevel=False):
    if cmds.objExists('gear'):
        cmds.delete('gear')
        
    side_faces = teeth * 2
    
    #main pipe
    transform, _ = cmds.polyPipe(name='gear', radius=outer_radius, height=height, thickness=outer_radius - inner_radius, subdivisionsAxis=side_faces)

    #select teeth faces
    side_faces = range(side_faces * 2, side_faces * 3, 2)
    cmds.select(clear=True)
    
    for face in side_faces:
        cmds.select('%s.f[%s]' % (transform, face), add=True)
    
    cmds.polyExtrudeFacet(localTranslateZ=length)
    
    if bevel:
        cmds.polyBevel3(offset=0.1, segments=1, offsetAsFraction=False)
        
        
#realtime update
def update_gear(*args):
    teeth = cmds.intSliderGrp('teethSlider', q=True, value=True)
    inner_radius = cmds.floatSliderGrp('innerRadiusSlider', q=True, value=True)
    outer_radius = cmds.floatSliderGrp('outerRadiusSlider', q=True, value=True)
    height = cmds.floatSliderGrp('heightSlider', q=True, value=True)
    length = cmds.floatSliderGrp('lengthSlider', q=True, value=True)
    bevel = cmds.checkBox('bevelCheckbox', q=True, value=True)
    
    if inner_radius >= outer_radius:
        inner_radius = outer_radius - 0.01
        cmds.floatSliderGrp('innerRadiusSlider', edit=True, value=inner_radius)
    
    create_gear(teeth, inner_radius, outer_radius, height, length, bevel)

def delete_gear_and_close(*args):
    if cmds.objExists('gear'):
        cmds.delete('gear')
    
    if cmds.window("gearWindow", exists=True):
        cmds.deleteUI("gearWindow")
        
def create_gear_and_close(*args):
    # Check if a gear exists
    if cmds.objExists('gear'):
        # Generate a unique name for the gear
        counter = 1
        gear_name = f"gear{counter}"  # Start with "gear1"
        while cmds.objExists(gear_name):
            counter += 1
            gear_name = f"gear{counter}"
        
        # Rename the existing gear
        cmds.rename('gear', gear_name)
    
    # Close the window if it exists
    if cmds.window("gearWindow", exists=True):
        cmds.deleteUI("gearWindow")

#ui window
def create_gear_window():
    if cmds.workspaceControl("gearWorkspace", exists=True):
        cmds.deleteUI("gearWorkspace", control=True)

    # create a workspaceControl for the gear creator, which allows it to be docked in the Maya UI
    workspace = cmds.workspaceControl("gearWorkspace", label="Procedural Gear Creator", retain=False)

    # set parent to the workspaceControl
    cmds.setParent(workspace)
    cmds.columnLayout(adjustableColumn=True)

    # sliders
    cmds.intSliderGrp('teethSlider', label='Teeth Count', min=5, max=50, value=20, step=1, field=True, dragCommand=update_gear)
    cmds.floatSliderGrp('innerRadiusSlider', label='Inner Radius', min=0.0, max=5.0, value=0.5, step=0.1, field=True, dragCommand=update_gear)
    cmds.floatSliderGrp('outerRadiusSlider', label='Outer Radius', min=0.5, max=10.0, value=2.0, step=0.1, field=True, dragCommand=update_gear)
    cmds.floatSliderGrp('heightSlider', label='Gear Height', min=0.1, max=5.0, value=0.5, step=0.1, field=True, dragCommand=update_gear)
    cmds.floatSliderGrp('lengthSlider', label='Tooth Length', min=0.1, max=2.0, value=0.3, step=0.1, field=True, dragCommand=update_gear)

    # bevel
    cmds.checkBox('bevelCheckbox', label='Bevel Gear Teeth', value=False, changeCommand=update_gear)

    cmds.button(label="Delete Gear and Close Window", command=delete_gear_and_close)
    cmds.button(label="Create Gear and Close Window", command=create_gear_and_close)

# show workspaceControl
create_gear_window()