import pickle
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras.utils import to_categorical

SEQUENCE_LENGTH = 50

print("Loading notes...")

with open("notes.pkl", "rb") as file:
    notes = pickle.load(file)

print("Total notes:", len(notes))

unique_notes = sorted(set(notes))

note_to_int = {
    note: i for i, note in enumerate(unique_notes)
}

X = []
y = []

for i in range(len(notes) - SEQUENCE_LENGTH):
    sequence = notes[i:i + SEQUENCE_LENGTH]
    next_note = notes[i + SEQUENCE_LENGTH]

    X.append([note_to_int[n] for n in sequence])
    y.append(note_to_int[next_note])

print("Training sequences:", len(X))
print("Unique notes:", len(unique_notes))

X = np.array(X)
y = np.array(y)

X = X.reshape(X.shape[0], X.shape[1], 1)
X = X / float(len(unique_notes))

y = to_categorical(
    y,
    num_classes=len(unique_notes)
)

print("Building model...")

model = Sequential()

model.add(
    LSTM(
        128,
        input_shape=(SEQUENCE_LENGTH, 1),
        return_sequences=True
    )
)

model.add(Dropout(0.3))

model.add(
    LSTM(128)
)

model.add(Dropout(0.3))

model.add(
    Dense(
        len(unique_notes),
        activation="softmax"
    )
)

model.compile(
    loss="categorical_crossentropy",
    optimizer="adam"
)

model.summary()

print("Starting training...")

model.fit(
    X,
    y,
    epochs=30,
    batch_size=32
)

model.save("music_model.keras")

with open("note_mapping.pkl", "wb") as file:
    pickle.dump(
        {
            "unique_notes": unique_notes,
            "note_to_int": note_to_int
        },
        file
    )

print("================================")
print("Training completed!")
print("Model saved as music_model.keras")
print("Mapping saved as note_mapping.pkl")
print("================================")