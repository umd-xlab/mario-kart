# Plot Mario driving on track

# start pos is (3712, 2288)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import tkinter as tk          # Package for UI selection of folders
from tkinter import filedialog
import os
import glob # For wildcard selection

# Load the track map

map_img = mpimg.imread("Racetrack_map.jpg")

# Load Mario's trace
root = tk.Tk()
root.withdraw()  # Hide the main window
folder_path= filedialog.askdirectory(initialdir="/home/kvsakano/mario-kart/OUTPUT", title="Select folder containing playback_trace CSVs")
root.destroy()

trace_files = sorted(glob.glob(os.path.join(folder_path, "playback_trace*.csv")))
if not trace_files:
    print("No matching files found.")
    exit()

colors = ['red', 'orange', 'yellow', 'green', 'blue']

plt.figure(figsize=(10, 10))
plt.imshow(map_img, origin='upper',extent=[0, 4200, 4200, 0])
i = 0
for file in trace_files:
    df = pd.read_csv(file)
    print(df['kart1_X'].min(), df['kart1_X'].max())
    print(df['kart1_Y'].min(), df['kart1_Y'].max())

    if 'kart1_X' in df.columns and 'kart1_Y' in df.columns:
        plt.plot(df['kart1_X'], df['kart1_Y'], color=colors[i], linewidth=3, label=os.path.basename(file))
    else:
        print(f"Warning: {file} missing 'kart1_X' or 'kart1_Y' columns. Skipping.")
    i += 1

# Plot map with Mario's trajectory



# Optional: mark start and end
#plt.scatter(df["kart1_X"].iloc[0], df["kart1_Y"].iloc[0], color='green', s=100, label='Start')
#plt.scatter(df["kart1_X"].iloc[-1], df["kart1_Y"].iloc[-1], color='blue', s=100, label='End')

plt.legend()
plt.title("Mario Trace Overlay on Track Map")
plt.axis('off')  # Turn off pixel axis if you want clean visuals
plt.show()