import tkinter as tk
from tkinter import ttk, messagebox
import os
import random
from ttkthemes import ThemedTk
import pretty_midi
import numpy as np


class MIDI_Generator:
    def __init__(self, root):
        self.root = root
        root.title("MIDI Generator")
        root.set_theme("clearlooks")

        # Define the scale patterns
        self.scale_patterns = {
            "Major": [2, 2, 1, 2, 2, 2, 1],
            "Minor": [2, 1, 2, 2, 1, 2, 2],
            "Dorian": [2, 1, 2, 2, 2, 1, 2],
            "Phrygian": [1, 2, 2, 2, 1, 2, 2],
            "Lydian": [2, 2, 2, 1, 2, 2, 1],
            "Mixolydian": [2, 2, 1, 2, 2, 1, 2],
            "Locrian": [1, 2, 2, 1, 2, 2, 2],
            "Major Pentatonic": [2, 2, 3, 2, 3],
            "Minor Pentatonic": [3, 2, 2, 3, 2],
            "Harmonic Minor": [2, 1, 2, 2, 1, 3, 1],
            "Melodic Minor": [2, 1, 2, 2, 2, 2, 1],
            "Whole Tone": [2, 2, 2, 2, 2, 2],
            "Random": []  # Add an empty list for the 'Random' scale pattern
        }

        # Define chord types
        self.chord_types = {
            'major': [4, 3, 5],
            'minor': [3, 4, 5],
            'diminished': [3, 3, 6],
            'augmented': [4, 4, 4],
            'dominant seventh': [4, 3, 3, 2],
            'major seventh': [4, 3, 4, 1],
            'minor seventh': [3, 4, 3, 2],
            'half diminished seventh': [3, 3, 4, 2],
            'minor major seventh': [3, 4, 4, 1],
            'major sixth': [4, 3, 2, 3],
            'minor sixth': [3, 4, 2, 3],
            'dominant ninth': [4, 3, 3, 2, 4],
            'major ninth': [4, 3, 4, 1, 4],
            'minor ninth': [3, 4, 3, 2, 4],
            'dominant eleventh': [4, 3, 3, 2, 4, 3],
            'major eleventh': [4, 3, 4, 1, 4, 3],
            'minor eleventh': [3, 4, 3, 2, 4, 3],
            'dominant thirteenth': [4, 3, 3, 2, 4, 3, 4],
            'major thirteenth': [4, 3, 4, 1, 4, 3, 4],
            'minor thirteenth': [3, 4, 3, 2, 4, 3, 4],
            'suspended second': [2, 5, 5],
            'suspended fourth': [5, 2, 5],
            'neapolitan': [1, 4, 5],
            'lydian': [4, 2, 5],
            'added ninth': [4, 3, 5, 4],
            'six nine': [4, 3, 2, 3, 4]
        }

        # Setup of input fields and buttons
        # Beats per Minute (BPM)
        self.bpm_label = ttk.Label(root, text="Beats Per Minute (BPM):")
        self.bpm_entry = ttk.Entry(root)
        self.bpm_entry.insert(0, "120")  # Default value
        self.bpm_label.grid(row=0, column=0, sticky="W", padx=8, pady=8)
        self.bpm_entry.grid(row=0, column=1, sticky="E", padx=8, pady=8)

        # Length (in seconds)
        self.length_label = ttk.Label(root, text="Length (seconds):")
        self.length_entry = ttk.Entry(root)
        self.length_entry.insert(0, "60")  # Default value
        self.length_label.grid(row=1, column=0, sticky="W", padx=8, pady=8)
        self.length_entry.grid(row=1, column=1, sticky="E", padx=8, pady=8)

        # Time Signature
        self.timesig_label = ttk.Label(root, text="Time Signature:")
        self.time_signature = ttk.Combobox(root, values=[
            "2/4",
            "3/4",
            "4/4",
            "5/4",
            "6/4",
            "7/4",
            "9/8",
            "12/8",
            "1/4",
            "8/4",
            "10/4",
            "11/4",
            "13/4",
            "15/4",
            "6/8",
            "3/8",
            "5/8",
            "7/8",
            "10/8",
            "11/8"],
            state="readonly")

        self.time_signature.current(2)  # Default value
        self.timesig_label.grid(row=2, column=0, sticky="W", padx=8, pady=8)
        self.time_signature.grid(row=2, column=1, sticky="E", padx=8, pady=8)

        # Root Key
        self.root_key_label = ttk.Label(root, text="Root Key:")
        self.root_key = ttk.Combobox(root, values=[pretty_midi.note_number_to_name(
            n) for n in range(36, 96)], state="readonly")  # Adjust the range here
        self.root_key.current(0)  # Default value
        self.root_key_label.grid(row=3, column=0, sticky="W", padx=8, pady=8)
        self.root_key.grid(row=3, column=1, sticky="E", padx=8, pady=8)

        # Scale Patterns
        self.scale_label = ttk.Label(root, text="Scale Pattern:")
        self.scale = ttk.Combobox(root, values=["Random",
                                                "Major",
                                                "Minor",
                                                "Dorian",
                                                "Phrygian",
                                                "Lydian",
                                                "Mixolydian",
                                                "Locrian",
                                                "Major Pentatonic",
                                                "Minor Pentatonic",
                                                "Harmonic Minor",
                                                "Melodic Minor",
                                                "Whole Tone"],
                                  state="readonly")
        self.scale.current(0)
        self.scale_label.grid(row=4, column=0, sticky="W", padx=8, pady=8)
        self.scale.grid(row=4, column=1, sticky="E", padx=8, pady=8)

        # Note lengths
        self.note_length_label = ttk.Label(root, text="Note Length:")
        self.note_length = ttk.Combobox(root, values=[
                                        "Random", "Whole", "Half", "Quarter", "Eighth", "Sixteenth"], state="readonly")
        self.note_length.current(2)
        self.note_length_label.grid(
            row=5, column=0, sticky="W", padx=8, pady=8)
        self.note_length.grid(row=5, column=1, sticky="E", padx=8, pady=8)

        self.min_note_length_label = ttk.Label(
            root, text="Min Note Length (if Random):")
        self.min_note_length = ttk.Combobox(
            root, values=["Whole", "Half", "Quarter", "Eighth", "Sixteenth"], state="readonly")
        self.min_note_length.current(2)
        self.min_note_length_label.grid(
            row=6, column=0, sticky="W", padx=8, pady=8)
        self.min_note_length.grid(row=6, column=1, sticky="E", padx=8, pady=8)

        self.max_note_length_label = ttk.Label(
            root, text="Max Note Length (if Random):")
        self.max_note_length = ttk.Combobox(
            root, values=["Whole", "Half", "Quarter", "Eighth", "Sixteenth"], state="readonly")
        self.max_note_length.current(2)
        self.max_note_length_label.grid(
            row=7, column=0, sticky="W", padx=8, pady=8)
        self.max_note_length.grid(row=7, column=1, sticky="E", padx=8, pady=8)

        # Chord Probability
        self.chord_prob_label = ttk.Label(root, text="Chord Probability (%):")
        self.chord_prob_scale = ttk.Scale(
            root, from_=0, to=100, orient="horizontal")
        self.chord_prob_label.grid(row=8, column=0, sticky="W", padx=8, pady=8)
        self.chord_prob_scale.grid(row=8, column=1, sticky="E", padx=8, pady=8)

        # Chord Type
        self.chord_type_label = ttk.Label(root, text="Chord Type:")
        self.chord_type = ttk.Combobox(root, values=list(
            self.chord_types.keys()), state="readonly")
        self.chord_type.current(0)  # Default value
        self.chord_type_label.grid(row=9, column=0, sticky="W", padx=8, pady=8)
        self.chord_type.grid(row=9, column=1, sticky="E", padx=8, pady=8)

        # Rest probability
        self.rest_chance_label = ttk.Label(root, text="Rest Chance:")
        self.rest_chance_scale = ttk.Scale(
            root, from_=0, to=100, orient="horizontal")
        self.rest_chance_label.grid(
            row=13, column=0, sticky="W", padx=8, pady=8)
        self.rest_chance_scale.grid(
            row=13, column=1, sticky="E", padx=8, pady=8)

        # Filename
        self.file_name_label = ttk.Label(root, text="File Name:")
        self.file_name_entry = ttk.Entry(root)
        self.file_name_entry.insert(0, "output")
        self.file_name_label.grid(row=14, column=0, sticky="W", padx=8, pady=8)
        self.file_name_entry.grid(row=14, column=1, sticky="E", padx=8, pady=8)

        # Generate MIDI button
        self.generate_button = ttk.Button(
            root, text="Generate MIDI", command=self.generate_midi)
        self.generate_button.grid(row=15, column=0, columnspan=2, pady=8)

        # Copyright label
        copyright_label = ttk.Label(
            root, text="© 2023 by Charles H. Jerred III", anchor="center")
        copyright_label.grid(
            row=16, column=0, columnspan=2, pady=(0, 10), sticky="s")

        # automaticmidi.com label
        website_label = ttk.Label(
            root, text="automaticmidi.com", anchor="center")
        website_label.grid(
            row=17, column=0, columnspan=2, sticky="s", pady=8)

    def generate_random_scale(self):
        random_pattern = random.choice(list(self.scale_patterns.keys()))
        return self.scale_patterns[random_pattern]

    def generate_midi(self):
        bpm = int(self.bpm_entry.get())
        song_length = int(self.length_entry.get())
        time_signature = self.time_signature.get()
        root_key = self.root_key.get()
        scale_pattern = self.scale.get()
        note_length = self.note_length.get()
        min_note_length = self.min_note_length.get()
        max_note_length = self.max_note_length.get()
        chord_prob = float(self.chord_prob_scale.get()) / 100
        chord_type = self.chord_type.get()
        # velocity_low = int(self.velocity_scale_low.get())
        # velocity_high = int(self.velocity_scale_high.get())
        rest_prob = float(self.rest_chance_scale.get()) / 100
        filename = self.file_name_entry.get()

        # root key logic ============
        root_key_number = pretty_midi.note_name_to_number(root_key)

        # scale pattern logic ============
        scale_intervals = self.scale_patterns.get(scale_pattern)
        if scale_intervals is None:
            print(f"Invalid scale pattern: {scale_pattern}")
            return

        if scale_pattern == "Random":
            scale_notes = []  # Assign an empty list directly
        else:
            scale_intervals = self.scale_patterns.get(scale_pattern)
            if scale_intervals is None:
                print(f"Invalid scale pattern: {scale_pattern}")
                return
            scale_notes = [root_key_number]
            for interval in scale_intervals:
                scale_notes.append(scale_notes[-1] + interval)

        scale_intervals = self.scale_patterns.get(scale_pattern)
        if scale_intervals is None:
            print(f"Invalid scale pattern: {scale_pattern}")
            return

        scale_notes = [root_key_number]
        for interval in scale_intervals:
            scale_notes.append(scale_notes[-1] + interval)

        # note length logic ============
        note_lengths = {"Whole": 4.0, "Half": 2.0,
                        "Quarter": 1.0, "Eighth": 0.5, "Sixteenth": 0.25}

        if note_length == "Random" and min_note_length and max_note_length:
            min_length = note_lengths[min_note_length]
            max_length = note_lengths[max_note_length]
            note_duration = random.uniform(min_length, max_length)
        else:
            note_duration = note_lengths[note_length]

        # note-generation logic ============
        midi = pretty_midi.PrettyMIDI()
        instrument = pretty_midi.Instrument(program=0)

        for i in np.arange(0, song_length, note_duration * (60.0 / bpm)):
            if random.random() < rest_prob:
                continue
            if random.random() < chord_prob:
                root_note_of_chord = random.choice(scale_notes)
                chord_notes = self.generate_chord(
                    root_note_of_chord, chord_type)
                for note_number in chord_notes:
                    if note_length == "Random" and min_note_length and max_note_length:
                        min_length = note_lengths[min_note_length]
                        max_length = note_lengths[max_note_length]
                        note_duration = random.uniform(min_length, max_length)
                    for note_number in chord_notes:
                        if note_length == "Random" and min_note_length and max_note_length:
                            min_length = note_lengths[min_note_length]
                            max_length = note_lengths[max_note_length]
                            note_duration = random.uniform(
                                min_length, max_length)
                        note = pretty_midi.Note(
                            velocity=random.randint(40, 80),
                            pitch=note_number, start=i, end=i + (note_duration * (60.0 / bpm) - 0.1))
                        instrument.notes.append(note)
            else:
                if scale_pattern == "Random":
                    scale_intervals = self.generate_random_scale()
                else:
                    scale_intervals = self.scale_patterns[scale_pattern]

                scale_notes = [root_key_number]
                for interval in scale_intervals:
                    scale_notes.append(scale_notes[-1] + interval)
                note_number = random.choice(scale_notes)
                if note_length == "Random" and min_note_length and max_note_length:
                    min_length = note_lengths[min_note_length]
                    max_length = note_lengths[max_note_length]
                    note_duration = random.uniform(min_length, max_length)
                note = pretty_midi.Note(velocity=random.randint(
                    40, 80), pitch=note_number, start=i, end=i + (note_duration * (60.0 / bpm) - 0.1))
                instrument.notes.append(note)
                scale_notes = [root_key_number]
                for interval in scale_intervals:
                    scale_notes.append(scale_notes[-1] + interval)
                note_number = random.choice(scale_notes)
                if note_length == "Random" and min_note_length and max_note_length:
                    min_length = note_lengths[min_note_length]
                    max_length = note_lengths[max_note_length]
                    note_duration = random.uniform(min_length, max_length)
                note = pretty_midi.Note(velocity=random.randint(
                    40, 80), pitch=note_number, start=i, end=i + (note_duration * (60.0 / bpm) - 0.1))

        midi.instruments.append(instrument)

        # file-saving logic
        home_dir = os.path.expanduser('~')
        file_path = os.path.join(home_dir, 'Music', '{}.mid'.format(filename))
        midi.write(file_path)
        messagebox.showinfo(
            "MIDI Generation", "MIDI file has been generated and saved at: {}".format(file_path))

        self.velocity_scale_low = ttk.Scale(
            root, from_=0, to=127, orient="horizontal", command=self.update_velocity_scales)
        self.velocity_scale_high = ttk.Scale(
            root, from_=0, to=127, orient="horizontal", command=self.update_velocity_scales)

    def update_velocity_scales(self, event):
        velocity_low = self.velocity_scale_low.get()
        velocity_high = self.velocity_scale_high.get()

        if velocity_low > velocity_high:
            self.velocity_scale_low.set(velocity_high)
        elif velocity_high < velocity_low:
            self.velocity_scale_high.set(velocity_low)

    # chord-generation logic
    def generate_chord(self, root_note, chord_type):
        intervals = self.chord_types[chord_type]
        chord_notes = [root_note]
        for interval in intervals:
            chord_notes.append(chord_notes[-1] + interval)
        return chord_notes


root = ThemedTk(theme="clearlooks")
my_gui = MIDI_Generator(root)
root.mainloop()
