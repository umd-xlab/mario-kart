# Post Processing and Plotting in MATLAB

Authors:
Kristy Sakano   
Joe Mockler  
Alexis Chen  

Purpose: this branch includes the scripts for deriving richer state data and creating paper-ready plots in MATLAB. 
-'Data': folder with csv data for parsing and plotting. 
-'csv_parse.py': this script will parse the data in the format found in 'Data' to a table that may then be plotted. In it, you must specify which file you want to read and what data headings you want to look for. Data is dumped into parsed_agent_data folder.
-'parsed_agent_data': this folder will have the table-ready data from the read csv. It includes one csv per agent evaluated. NOTE: data in this folder DOES get overwritten each time csv_parse.py is run!
-'csv_parsing_and_analysis.m': takes derivatives, computes body angles, calculates reset and trims data, and creates paper-ready plots. This script WILL pull from the parsed_agent_data folder! So the workflow should look something like:



