#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 11:52:06 2020

@author: hayden

Combine/Merge multiple CSV files using the Pandas library
Source: https://www.techbeamers.com/pandas-merge-csv-files/

The output MAL.csv should be moved to the AnimeRecommender/data folder
"""


from os import chdir
from glob import glob
import pandas as pdlib

# Produce a single CSV after combining all files
def mergeCSV(list_of_files, file_out):
   # Consolidate all CSV files into one object
   result_obj = pdlib.concat([pdlib.read_csv(file) for file in list_of_files])
   # Convert the above object into a csv file and export
   result_obj.to_csv(file_out, index=False, encoding="utf-8")

# Move to the path that holds our CSV files
csv_file_path = "/home/hayden/Projects/AnimeRecommender/raw_data/temp/"
chdir(csv_file_path)

# List all CSV files in the working dir
file_pattern = ".csv"
list_of_files = glob('*.csv')
print(len(list_of_files))

#file_out = "MAL.csv"
#mergeCSV(list_of_files, file_out)
