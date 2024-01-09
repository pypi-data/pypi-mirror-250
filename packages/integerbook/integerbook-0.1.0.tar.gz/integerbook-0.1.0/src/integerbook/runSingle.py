import json
import os

from integerbook.main import Visualiser

f = open('settings.json')
settings = json.load(f)

settings["measuresPerLine"] = 4
settings["romanNumerals"] = False
settings["numbersRelativeToChord"] = False
settings["setInMajorKey"] = False
settings["coloursVoices"] = True
settings["lyrics"] = True
settings["chordVerbosity"] = 2
settings["fontSizeChordsPerFontSizeNotes"] = 1
settings["setInMajorKey"] = False

settings["fontSizeNotes"] = 10
settings["saveCropped"] = True


# let it snow 
# settings["ignoreSecondaryDominants"] = [(15, 1), (15, 2), (15, 3)]

if False:
    settings['fontDirectory'] = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/fonts/Vulf Mono/Vulf Mono/Desktop/"
    settings['font'] = 'Vulf Mono'
    settings['fontStyle'] = 'italic'
    settings['fontWeight'] = 'light'

pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/popular-sheets/Lullaby_of_Birdland_453af5e8-18cb-4b4c-9f0a-4baf7a27db8d.musicxml"
pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/popular-sheets/All_Of_Me_de3dd464-e2bc-484a-837d-b9b77a7c28c9.musicxml"
# pathToSong = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/documents/bladmuziek/test-files/notes-relative-to-chord.musicxml"
# pathToSong = "/Users/jvo/Downloads/output/notes-relative-to-chord.musicxml"
# pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/DSAll/Giant_Steps_d43d4d4c-7bf9-4c23-ade4-7352a541ccac.musicxml"
# pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/in-progress/Giant_Steps.musicxml"
# pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/popular-sheets/Lovely_day.musicxml"
pathToSong = "/Users/jvo/Downloads/output/giant_steps_with_keys.musicxml"
# pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/DSAll/All_The_Things_You_Are_c0959048-6195-4a57-beb3-42941ab3db80.musicxml"
pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/in-progress/all the things you are.musicxml"
pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/popular-sheets/Autumn_Leaves_18ae0812-5600-4fcc-8a30-170c9edcd876.musicxml"
pathToSong = "/Users/jvo/Downloads/baby it's cold outside.musicxml"
pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/Jingle_Bells_9eab83c4-7086-4e48-9af2-c7d89971293f.musicxml"
pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/Silent_Night_f40b33cf-1456-402c-8e56-c23cb4050ca8.musicxml"
pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/jesse/Santa_Baby.musicxml"
pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/jesse/Santa_Baby-without-key-change.musicxml"
pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/Winter_Wonderland-keychange.musicxml"
pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/Have_Yourself_a_Merry_Little_Christmas.musicxml"
pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/Rudolph_the_Red-nosed_Reindeer.musicxml"
s1 = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/Jingle_Bells_9eab83c4-7086-4e48-9af2-c7d89971293f.musicxml"
s2 = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/baby it's cold outside.musicxml"
s3 = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/Baby_its_Cold_Outside_74cb8436-d4de-409e-9f78-7437a722256b.musicxml"
s4 = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/Rudolph_the_Red-nosed_Reindeer_358d7681-467a-4736-a109-22d026e9b9bd.musicxml"
s5 = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/Let_it_snow.musicxml"
s6 = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/Its_Beginning_to_Look_a_Lot_Like_Christmas_86281fba-6d63-4ff5-9f99-823c2d4caa5b.musicxml"
s7 = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/The_Christmas_Song_1538abdd-35a0-4a29-aa7c-f37a93b33673.musicxml"
s8 = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/Santa_Claus_is_Coming_to_Town_5bdcaea8-5be7-4015-ba02-3236368d13ba.musicxml"
s9 = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/Have_Yourself_a_Merry_Little_Christmas_6068e21a-cda6-4fd4-9af6-293285d1e940.musicxml"
s11 = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/Santa_Baby_e93130e1-77d4-4d00-be33-8c85e5c917b3.musicxml"
s12 = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/The_Christmas_Song_1538abdd-35a0-4a29-aa7c-f37a93b33673.musicxml"
s13 = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection/Let_It_Snow_235c3558-b290-41fc-9f4f-c89d9d956bdc.musicxml"
s14 = "/Users/jvo/Documents/programming/sheet-music/sheets/popular-sheets/Autumn_Leaves_18ae0812-5600-4fcc-8a30-170c9edcd876.musicxml"
s15 = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/icloudDocuments/bladmuziek/test-files/tied-note-to-next-line.musicxml"
s16 = "/Users/jvo/Documents/programming/music-visualisation/testsuite/71a-Chordnames.musicxml"
s17 = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/icloudDocuments/bladmuziek/test-files/chords1.musicxml"
s18 = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/icloudDocuments/bladmuziek/test-files/slash-chords.musicxml"

fullPath = s6

songPath = os.path.basename(fullPath)

ff = open('manualSettings.json')
songSettings = json.load(ff)
if songPath in songSettings.keys():
    for key in songSettings[songPath].keys():
        settings[key] = songSettings[songPath][key]


vis = Visualiser(fullPath, settings)

vis.saveFig("/Users/jvo/Downloads/output")
