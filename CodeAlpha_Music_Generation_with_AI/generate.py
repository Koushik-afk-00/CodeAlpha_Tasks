import pickle
import random
import subprocess
import numpy as np

from music21 import stream, note, chord
from tensorflow.keras.models import load_model

SEQUENCE_LENGTH = 50
GENERATE_LENGTH = 200

MODEL_FILE = "music_model.keras"
NOTES_FILE = "notes.pkl"
MAPPING_FILE = "note_mapping.pkl"

SOUNDFONT = "FluidR3_GM.sf2"
MIDI_FILE = "generated_music.mid"
WAV_FILE = "generated_music.wav"

FLUIDSYNTH = (
    r"fluidsynth-v2.6.0-win10-x64-cpp11"
    r"\bin\fluidsynth.exe"
)

print("Loading trained model...")

model = load_model(MODEL_FILE)

with open(NOTES_FILE, "rb") as file:
    notes = pickle.load(file)

with open(MAPPING_FILE, "rb") as file:
    mapping = pickle.load(file)

unique_notes = mapping["unique_notes"]
note_to_int = mapping["note_to_int"]

int_to_note = {
    value: key
    for key, value in note_to_int.items()
}

start = random.randint(
    0,
    len(notes) - SEQUENCE_LENGTH - 1
)

pattern = notes[
    start:start + SEQUENCE_LENGTH
]

generated_notes = []

print("Generating music...")

for _ in range(GENERATE_LENGTH):

    input_sequence = [
        note_to_int[n]
        for n in pattern
    ]

    input_data = np.array(input_sequence)

    input_data = input_data.reshape(
        1,
        SEQUENCE_LENGTH,
        1
    )

    input_data = (
        input_data / float(len(unique_notes))
    )

    prediction = model.predict(
        input_data,
        verbose=0
    )

    index = np.argmax(prediction)

    result = int_to_note[index]

    generated_notes.append(result)

    pattern.append(result)
    pattern = pattern[1:]

print("Creating MIDI file...")

output = stream.Stream()

for item in generated_notes:

    if "." in item:

        chord_notes = [
            int(n)
            for n in item.split(".")
        ]

        output.append(
            chord.Chord(chord_notes)
        )

    else:

        output.append(
            note.Note(item)
        )

output.write(
    "midi",
    fp=MIDI_FILE
)

print("MIDI created successfully!")

print("Converting MIDI to WAV...")

try:

    subprocess.run(
        [
            FLUIDSYNTH,
            "-ni",
            "-F",
            WAV_FILE,
            "-r",
            "44100",
            SOUNDFONT,
            MIDI_FILE
        ],
        check=True
    )

    print("\n==============================")
    print("Music generated successfully!")
    print("MIDI :", MIDI_FILE)
    print("WAV  :", WAV_FILE)
    print("==============================")

except FileNotFoundError:

    print("\nFluidSynth was not found.")
    print("Check the FLUIDSYNTH path in generate.py.")

except subprocess.CalledProcessError:

    print("\nWAV conversion failed.")
    print("Check your SoundFont file and FluidSynth installation.")