import bpy

#========================
# Parsing the text file
#========================

# Path to the midi - to -text result file
filepath = 'C:/Users/Techtooth/Documents/gball 01.txt'

#current index we are looking for
current_ind = -1
beat = 2
Tempos = []
Tempo_time = []
beat_change_time = 0
beat_change_length = 0

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
            beat_temp = int(current_tempo_item[2])/500000*2
            Tempos.append(beat_temp)
            Tempo_time.append(int(current_tempo_item[0]))
            print ("Tempos:  " + str(Tempos))
            
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
            tile_loc = ob.location[1]
            
            #checking wheather beat is changes or not
            before_beat = beat
            for index2,k in enumerate(Tempo_time):
                if int(current_on_item[0]) >= k:
                    beat = Tempos[index2] 
            
            #is the beat changed
            if before_beat != beat:
                beat_change_length = last_length
                beat_change_time = end_time
                #print("changed  " + str(beat_change_time) + "   " +str(beat_change_length))       
            
                        
            last_length = int(current_off_item[0])            
                        
            bpy.context.object.color = (0, 0, 0, 1)
            ob.keyframe_insert(data_path = "color" , frame = beat_change_time + bpy.context.scene.render.fps * beat / 0.192 * (tile_loc - beat_change_length/10000)-1)
            #print (beat_change_time + bpy.context.scene.render.fps * beat / 0.192 * (tile_loc - beat_change_length/10000)-1)
            
            bpy.context.object.color = (1, 1, 1, 1)
            ob.keyframe_insert(data_path = "color" , frame = beat_change_time + bpy.context.scene.render.fps * beat / 0.192 * (tile_loc - beat_change_length/10000))

            bpy.context.object.color = (1, 1, 1, 1)
            ob.keyframe_insert(data_path = "color" , frame = beat_change_time + bpy.context.scene.render.fps * beat / 0.192 * (tile_loc - beat_change_length/10000)+1 + bpy.context.scene.render.fps * beat / 0.192 * tile_length/10000)
    
            bpy.context.object.color = (0, 0, 0, 1)
            end_time = beat_change_time + bpy.context.scene.render.fps * beat / 0.192 * (tile_loc - beat_change_length/10000)+1 + bpy.context.scene.render.fps * beat / 0.192 * tile_length/10000 +1
            #print (int(end_time))
            ob.keyframe_insert(data_path = "color" , frame = end_time)
            
            
                