# AI Music Generation 🎵🤖

An AI-based music generation project using **Python and LSTM**.

## How It Works

* MIDI files are used as the dataset.
* `preprocess.py` extracts notes and chords.
* `train.py` trains an LSTM model.
* `generate.py` generates new music.
* FluidSynth converts the generated MIDI into WAV audio.

## Project Structure

```text
AI-Music-Generator/
│
├── dataset/
├── preprocess.py
├── train.py
├── generate.py
├── requirements.txt
└── README.md
```

## Requirements

```bash
pip install music21 numpy tensorflow
```

**FluidSynth** is also required for MIDI-to-WAV conversion.

## Run

```bash
py preprocess.py
py train.py
py generate.py
```

The generated music will be saved as:

```text
generated_music.mid
generated_music.wav
```

## Technologies

* Python
* TensorFlow / Keras
* LSTM
* music21
* NumPy
* FluidSynth

## Note

Large files such as the trained model, SoundFont, audio output, and MIDI dataset are not included in this repository.

## Author

**Koushik Ayyappan**