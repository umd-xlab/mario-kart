import pandas as pd
import numpy as np
import Tkinter as tk          # Package for UI selection of folders
import tkFileDialog
import tkMessageBox as messagebox

import matplotlib
matplotlib.use('TkAgg')  # explicitly set backend before pyplot import, Tkinter compatible
import matplotlib.pyplot as plt

import telex.synth
import os
import csv

# Note: TeLEX uses python 2.7.18. Some commands like .to_numpy() and filedialog do not exist in this version of python
# Make sure you are using a version compatible package for python!



def ask_file_or_folder():
    root = tk.Tk()
    root.withdraw()
    win = tk.Toplevel(root)
    win.title("Select Input")

    user_choice = {"choice": None}

    def select_file():
        user_choice["choice"] = "file"
        win.destroy()

    def select_folder():
        user_choice["choice"] = "folder"
        win.destroy()

    tk.Label(win, text="Pick an input type:").pack(pady=10)
    tk.Button(win, text="File", width=10, command=select_file).pack(side="left", padx=20, pady=20)
    tk.Button(win, text="Folder", width=10, command=select_folder).pack(side="right", padx=20, pady=20)

    root.wait_window(win)
    root.destroy()
    return user_choice["choice"]



def import_file():
    # Load Mario's trace or traces

    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = "/home/kvsakano/TeLEX/tests/data/" #    <------------------------------------------ You need to change your folder path, this is the only place it is hardcoded
    path = tkFileDialog.askopenfilename(initialdir=folder_path,  title="Select a file")
    root.destroy()
    return path

def import_folder():
    # Load a folder full of traces
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = "/home/kvsakano/TeLEX/tests/data/" #    <------------------------------------------ You need to change your folder path, this is the only (other) place it is hardcoded
    path = tkFileDialog.askdirectory(initialdir=folder_path,  title="Select a folder")
    root.destroy()
    return path   

def preprocessing(path):
    # If phidot is not part of the file, then this calculates it & adds it as a new file with the {title}_with_phidot.csv

    filename = os.path.splitext(os.path.basename(path))[0]
    df = pd.read_csv(path)

    # Add phidot column if it does not exist
    if "phidot" not in df.head():
        print('phidot is not in the dataframe. Calculating and finding it now')

        x_pos = df['kart1_X'].values
        y_pos = df['kart1_Y'].values

        # Smooth x and y before driving velocity (OPTIONAL)
        window = 10
        x_smooth = pd.Series(x_pos).rolling(window, center=True, min_periods=1).mean().values
        y_smooth = pd.Series(y_pos).rolling(window, center=True, min_periods=1).mean().values
        
        # Calculate velocities
        vx = np.gradient(x_smooth)
        vy = np.gradient(y_smooth)

        # Calculate starting reference point by averaging first 10 (x,y)
        x_start = np.mean(x_smooth[:10])
        y_start = np.mean(y_smooth[:10])

        delx = x_smooth - x_start
        dely = y_smooth - y_start
        
        # Mask for elements where either abs(delx)<1 or abs(dely)<1
        mask = (np.abs(delx) < 1) | (np.abs(dely) < 1)

        # phi - set to 0 where mask is True, otherwise arctan2 result. Avoid loop !!!
        phi = np.where(mask, 0, np.arctan2(vx,-vy)) 
        df['phi'] = phi

        # phidot - gradient of phi
        phidot = np.gradient(phi)
        df['phidot'] = phidot

        # Change the column header of step -> time if it exists
        if 'step' in df.columns:
            df.rename(columns={'step': 'time'}, inplace=True)

        output_file_path =  "/home/kvsakano/TeLEX/tests/data/" + filename + "_with_phidot.csv"
        df.to_csv(output_file_path, index=False)
        return output_file_path
    else:
        print("Looks like phidot was in the file. Using original file now.")
        return path
    

    
def test_stl_file(file_path, templogicdata):
    # Testing STL on a single file
    print("Performing STL analysis on the file. Hold tight....")

    results = []
    for tlStr in templogicdata:
            stlsyn, value, dur = telex.synth.synthSTLParam(tlStr, file_path)
            bres, qres = telex.synth.verifySTL(stlsyn, file_path)
            results.append({"formula": tlStr,
                            "synthesized stl": stlsyn,
                            "theta optimal value": value,
                            "optimization time": dur,
                            "test result": bres,
                            "robustness": qres})

    with open("telex_results.csv", "w") as csvfile:
        fieldnames = ["formula", "synthesized stl", "theta optimal value", "optimization time", "test result", "robustness"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

def test_stl_folder(folder_path, templogicdata):
    # Testing STL on a folder full of csvs
    print("Performing STL analysis on the folder. Hold tight....")

    file_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
    
    results = []
    for file in file_list:
        for tlStr in templogicdata:
                stlsyn, value, dur = telex.synth.synthSTLParam(tlStr, file)
                bres, qres = telex.synth.verifySTL(stlsyn, file)
                results.append({"formula": tlStr,
                                "trace": file,
                                "synthesized stl": stlsyn,
                                "theta optimal value": value,
                                "optimization time": dur,
                                "test result": bres,
                                "robustness": qres})

    with open("telex_results.csv", "w") as csvfile:
        fieldnames = ["formula", "trace", "synthesized stl", "theta optimal value", "optimization time", "test result", "robustness"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    return
    



def main():

    choice = ask_file_or_folder()

    templogicdata = ['G[0, 72] ( ((phidot > 0.5)|(phidot < -0.5)) -> kart1_speed < a? 0;80)', 'F[0, a? 1;70]( kart1_speed < 20 )', 'G[a? 0;60, b? 10;72](phidot < 0.5)']

    if choice == 'file':
        path = import_file()
        print(path + " is a CSV file. Checking for phi, will save new file if phi does not exist.")
        path = preprocessing(path)
        test_stl_file(path, templogicdata)

    elif choice == 'folder':
        path = import_folder()
        test_stl_folder(path, templogicdata)
        
    else:
        print(path + " is neither a CSV file nor a directory. Try again!")



if __name__ == '__main__':
    main()