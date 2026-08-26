import glob
import pickle
from music21 import converter, note, chord

notes = []

midi_files = glob.glob("dataset/*.mid")

print("MIDI files found:", len(midi_files))

for file in midi_files:
    print("Reading:", file)

    try:
        midi = converter.parse(file)

        for element in midi.flatten().notes:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))

            elif isinstance(element, chord.Chord):
                notes.append(
                    ".".join(str(n) for n in element.normalOrder)
                )

    except Exception as e:
        print("Could not read:", file)
        print(e)

print("Total notes collected:", len(notes))

with open("notes.pkl", "wb") as file:
    pickle.dump(notes, file)

print("Done!")
print("Notes saved to notes.pkl")