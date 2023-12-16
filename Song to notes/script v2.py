import bpy

#========================
# Parsing the text file
#========================

# Path to the midi - to -text result file
filepath = 'C:/Users/Yasiru/Desktop/Song to notes/On note_Only_Cube_length_check01.txt'

#current index we are looking for
current_ind = -1

with open(filepath) as file:
    # make a list out of the line of the input .txt file
    data = file.read().splitlines()

    # splitting line to 2 if there's multiple note events on one line
    for index, i in enumerate(data):
        #finding the next start note
        if ('On' in i) and (index > current_ind):
            # separating the note events into a list
            current_on_item = i.split(' ')
            
            current_ind = index

            #finding the end line for the current note
            for index, i in enumerate(data):
                if (('Off' in i) or ('v=0' in i)) and (index > current_ind):
                    # separating the note events into a list
                    current_off_item = i.split(' ')
                    #finding out weather it's the one
                    if (current_on_item[3] == current_off_item[3]):
                        break
            #for debugging only
            #print (f"Reading {current_on_item} Ending {current_off_item}")

            #getting tile's Z position
            temp_String = current_on_item[4]
            tile_z = int(temp_String[2::])

            #getting tiles track
            temp_String = current_on_item[3]
            tile_x = int(temp_String[2::])-60

            #getting tile length
            temp_String = current_off_item[0]
            tile_length = int(temp_String)
            temp_String = current_on_item[0]
            tile_length = tile_length - int(temp_String)

            #getting the y position of the tile
            temp_String = current_off_item[0]
            tile_y = int(temp_String)
            temp_String = current_on_item[0]
            tile_y = (tile_y + int(temp_String))/2
            
            
            #building the 3d tiles
            
            #adding the cube
            bpy.ops.mesh.primitive_cube_add(size=0.02, enter_editmode=False, align='WORLD', location=(tile_x/1000000*20000+0.01, tile_y/10000, tile_z/100), scale=(1, 1, 1))
            
            #scalling the cube
            bpy.ops.transform.resize(value=(1,tile_length/2/100, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


