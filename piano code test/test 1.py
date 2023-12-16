import bpy

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)


#========================
# Parsing the text file
#========================
print("==== Parsing the text file ====")

# Path to the midi - to -text result file
filepath = 'C:/Users/Techtooth/Desktop/piano code test/test.txt'

with open(filepath) as file:
    
    # make a list out of the line of the input .txt file
    data = file.read().splitlines()
    
    #This is the variable for the current height
    height = 0
    
    for index, i in enumerate(data):
        if ',' in i:
            #print (i)
            split_item = i.split(',')
            
            raw = int(split_item[0])*2
            length = int(split_item[1])
            
            #increasing height
            height = height + length/2
            
            #generating 3D
            
            #genarating the plane
            bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(raw, 0, height), scale=(1,1,1))
            
            
            #giving material
            bpy.context.active_object.data.materials.append(bpy.data.materials.get("Material"))
            
            #giving the plane a length
            bpy.ops.transform.resize(value=(1, length, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

            #rotating the planes to stay straight
            bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            
            #increasing height
            height = height + length/2
            
            


            
            
           

            
            