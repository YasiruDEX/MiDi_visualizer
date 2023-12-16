#========================
# Parsing the text file
#========================
print("==== Parsing the text file ====")



# Path to the midi - to -text result file
filepath = 'C:/Users/Yasiru/Desktop/Song to notes/test_2_song.txt'

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
                if ('Off' in i) and (index > current_ind):
                    # separating the note events into a list
                    current_off_item = i.split(' ')
                    #finding out weather it's the one
                    if (current_on_item[3] == current_off_item[3]):
                        break

            #for debugging only
            print (f"Reading {current_on_item} Ending {current_off_item}")

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

