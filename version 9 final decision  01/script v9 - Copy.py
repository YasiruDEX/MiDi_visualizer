import bpy

#========================
# Parsing the text file
#========================

# Path to the midi - to -text result file
filepath = 'C:/Users/Techtooth/Desktop/Song to notes/version 9 final decision  01/01 fix tempo/05 Other random tempo final check.txt'

#current index we are looking for
current_ind = -1
Tempos = []
Tempo_time = []

with open(filepath) as file:
    # make a list out of the line of the input .txt file
    data = file.read().splitlines()
    
    #creating the collection
    Notes_pres = False
    for collection in bpy.data.collections:
        if collection.name == "Notes":
            Notes_pres = True
    if Notes_pres == False:         
        bpy.ops.collection.create(name = "Notes")
        bpy.context.scene.collection.children.link(bpy.data.collections["Notes"])
    # splitting line to 2 if there's multiple note events on one line
    for index, i in enumerate(data):
        
        #finding the tempo
        if ('Tempo' in i):
            # separating the note events into a list
            current_tempo_item = i.split(' ')
            beat_temp = int(current_tempo_item[2])
            Tempos.append(beat_temp)
            Tempo_time.append(int(current_tempo_item[0]))
            #print ("Tempos:  " + str(Tempos))
            
        #finding the next start note
        if ('On' in i) and not('v=0' in i) and (index > current_ind) and ('n=' in i):
            # separating the note events into a list
            current_on_item = i.split(' ')
            
            current_ind = index

            #finding the end line for the current note
            for index, i in enumerate(data):
                if (('Off' in i) or ('v=0' in i)) and (index > current_ind) and ('n=' in i):
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
            
            #getting the channel
            temp_String = current_off_item[2]
            tile_channel = int(temp_String[3::]) 
            if tile_channel < 10:
                tile_mat = f"Midi Ch 0{tile_channel} material"
            else:
                tile_mat = f"Midi Ch {tile_channel} material"
            
            
            #building the 3d tiles
            
            #adding the cube
            bpy.ops.mesh.primitive_cube_add(size=0.02, enter_editmode=False, align='WORLD', location=(tile_x/1000000*20000+0.01, tile_y/10000, tile_z/100))


            #giving tiles custom names
            if tile_channel < 10:
                note_name = f"ch 0{tile_channel} n {tile_x+60}"
            else:
                note_name = f"ch {tile_channel} n {tile_x+60}"
            bpy.context.object.name = note_name
            
            #giving tiles custom materials
            mat = bpy.data.materials.get(tile_mat)
            bpy.context.active_object.data.materials.append(mat)
            bpy.ops.object.move_to_collection(collection_index=2)
            
            #scalling the cube
            bpy.ops.transform.resize(value=(1,tile_length/2/100, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    
            #getting origin forward
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.transform.translate(value=(0,tile_length/20000, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            bpy.ops.object.editmode_toggle()
            bpy.ops.transform.translate(value=(-0, -tile_length/20000, -0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


            #setting color key frames
            ob = bpy.context.active_object
            
            #new formula for time using tempo
            temp_val = current_on_item[0]
            value = int(temp_val)
            for index3, x in enumerate(Tempo_time):
                if value > x:
                    until_time = index3
            total_time = 0
            for x in range(until_time):
                total_time = total_time + Tempos[x] * (Tempo_time[x+1] - Tempo_time[x])
            
            total_time = total_time + Tempos[until_time] * (value - Tempo_time[until_time]) 
                        
            bpy.context.object.color = (0, 0, 0, 1)
            ob.keyframe_insert(data_path = "color" , frame = bpy.context.scene.render.fps * total_time / 48000 / 10000)
            
            bpy.context.object.color = (1, 1, 1, 1)
            ob.keyframe_insert(data_path = "color" , frame = bpy.context.scene.render.fps * total_time / 48000 / 10000 + 1)
            
            #new formula for time using tempo
            temp_val = current_off_item[0]
            value = int(temp_val)
            for index3, x in enumerate(Tempo_time):
                if value > x:
                    until_time = index3
            total_time = 0
            for x in range(until_time):
                total_time = total_time + Tempos[x] * (Tempo_time[x+1] - Tempo_time[x])
            
            total_time = total_time + Tempos[until_time] * (value - Tempo_time[until_time]) 
            
            bpy.context.object.color = (1, 1, 1, 1)
            ob.keyframe_insert(data_path = "color" , frame = bpy.context.scene.render.fps * total_time / 48000 / 10000)
    
            bpy.context.object.color = (0, 0, 0, 1)
            ob.keyframe_insert(data_path = "color" , frame = bpy.context.scene.render.fps * total_time / 48000 / 10000 + 1)
            
            
def formula(temp_val):
    value = int(temp_val)
    for index3, x in enumerate(Tempo_time):
        if value > x:
            until_time = index3
    total_time = 0
    for x in range(until_time):
        total_time = total_time + Tempos[x] * (Tempo_time[x+1] - Tempo_time[x])
    
    total_time = total_time + Tempos[until_time] * (value - Tempo_time[until_time]) 
    return total_time
