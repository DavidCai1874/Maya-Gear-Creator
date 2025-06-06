# 如何使用
1. 开启maya
2. 点击右下角唤出代码窗口
<img width="25" alt="1" src="https://github.com/user-attachments/assets/3db8f240-13cc-4308-8bc9-3ad32263e2a7">


3. 选择python并且粘贴 'gear_generator_v10.py' 文件中的代码
<img width="677" alt="2" src="https://github.com/user-attachments/assets/90c3cca5-ac1b-4eab-b2de-7ed437635c0e">


4. 运行
<img width="676" alt="3" src="https://github.com/user-attachments/assets/89ba9ae6-55d6-4dbe-a9c0-b7c715078c7e">


# 演示视频(Youtube)
[![Watch on YouTube](https://img.youtube.com/vi/_GapDayaKHE/0.jpg)](https://www.youtube.com/watch?v=_GapDayaKHE)


#### 以防万一
代码在此
```
import maya.cmds as cmds

#create gear
def create_gear(teeth=20, inner_radius=0.0, outer_radius=2.0, height=0.5, length=0.3, bevel=False):
    if cmds.objExists('gear'):
        cmds.delete('gear')
        
    spans = teeth * 2
    
    #main pipe
    transform, constructor = cmds.polyPipe(name='gear', radius=outer_radius, height=height, thickness=outer_radius - inner_radius, subdivisionsAxis=spans)

    #select teeth faces
    side_faces = range(spans * 2, spans * 3, 2)
    cmds.select(clear=True)
    
    for face in side_faces:
        cmds.select('%s.f[%s]' % (transform, face), add=True)
    
    cmds.polyExtrudeFacet(localTranslateZ=length)
    
    if bevel:
        cmds.polyBevel3(offset=0.1, segments=1, offsetAsFraction=False)
        
    return transform, constructor

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

#ui window
def create_gear_window():
    if cmds.window("gearWindow", exists=True):
        cmds.deleteUI("gearWindow")
        
    cmds.window("gearWindow", title="Procedural Gear Creator", widthHeight=(300, 250))
    
    cmds.columnLayout(adjustableColumn=True)
    
    #sliders
    cmds.intSliderGrp('teethSlider', label='Teeth Count', min=5, max=50, value=20, step=1, field=True, dragCommand=update_gear)
    cmds.floatSliderGrp('innerRadiusSlider', label='Inner Radius', min=0.0, max=5.0, value=0.5, step=0.1, field=True, dragCommand=update_gear)
    cmds.floatSliderGrp('outerRadiusSlider', label='Outer Radius', min=0.5, max=10.0, value=2.0, step=0.1, field=True, dragCommand=update_gear)
    cmds.floatSliderGrp('heightSlider', label='Gear Height', min=0.1, max=5.0, value=0.5, step=0.1, field=True, dragCommand=update_gear)
    cmds.floatSliderGrp('lengthSlider', label='Tooth Length', min=0.1, max=2.0, value=0.3, step=0.1, field=True, dragCommand=update_gear)
    
    #bevel
    cmds.checkBox('bevelCheckbox', label='Bevel Gear Teeth', value=False, changeCommand=update_gear)
    
    cmds.button(label="Create Gear", command=update_gear)
    
    cmds.showWindow("gearWindow")

# show window
create_gear_window()
```

