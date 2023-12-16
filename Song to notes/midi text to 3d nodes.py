import re




#========================
# Parsing the text file
#========================
print("==== Parsing the text file ====")



# Path to the midi - to -text result file
filepath = 'C:/Users/Techtooth/Desktop/Midi_Test_02.txt  '

#List of lists, to store tracks and their notes
Tracks_notes = []

# variable to store the current track while looping throug the text
current_track = 0
current_notelist = 0


with open(filepath) as file:
    
    # make a list out of the line of the input .txt file
    data = file.read().splitlines()
    
    # splitting line to 2 if there's multiple note events on one line
    for index, i in enumerate(data):
        if ',' in i:
            print (i)
            timestamp = re.search(r'.+:', i)
            print(timestamp)
            #print("timestamp = ", timestamp.group())
            
            # separating the note events into a list
            split_item = i.split(',')
            
            # going through eash event and inserting them in a suitable place in date
            for x in split_item:
                
                print("index = ", index)
                
                if timestamp.group() in x:
                    data.insert((index + 1), x)
                    print("time is in group,", "insertion index = ", (index +1))
                    
                if timestamp.gtoup() not in x:
                    print("time isn't in group, ", "insertion index = ", (index +1))
                    timestamp_added = re.sub(',', '', timestamp.group() + str(x))
                    data.insert((index + 1), timestamp_added)
                    
            #deleting the orginal line that had multiple events
            del date[index]
            
            
    #making the list of tracks/note.events
    for i in data:
        
        # when " and (are in the line, it marke a track name in the text file
        if (    '"' in i
            and '(' in i
            ):
                
            current_track += 1
            current_notelist = 0
            
            #appending anew track as an empty list
            track_notes.append([])
            
        # when these are true, a line is a note event in the text file
        if (    '"' not in i
            and '(' not in i
            and len(i) > 1
            and current_track != 0
            ):
                
            current_notelist += 1
            
            # appending anew list in the current track's list with a value of i or 0
            # depending on if the line is a note-on or note-off event
            if 'on' in i:
                tracks_notes[current_track - 1].append([1])
                
            if 'off' in i:
                tracks_notes[current_track - 1].append([1])
                
            #looping through each word of the line (separated by a space
            for a in i.split():
                
                # finding only the relevant charaters (number stuff) from splitted words
                numbermatch = re.search(r'[^:onfv;]+', a)
                
                #when getting a number we convert it into fleat/int and assing it to a new variable
                if numbermatch != None:
                    number = evel(numbermatch.group())
                    
                    # adding this number to the notelist
                    tracks_notes[current_track - 1][current_notelist - 1].append(number)
                    
                    
                    
                    
#==============
#==============
#==============
print("==== Generating the 3d note objects ====")



# collection in which to plece the note block objects
#target_collection = bpy.data.collection["notes"]

# all the notes in the MIDI protocol (0-128)
notes = list(range(0, 129))

# temporary list of on/off event timestamps
on_off_sequence = []

# horizontal scale factor for 3d notes
