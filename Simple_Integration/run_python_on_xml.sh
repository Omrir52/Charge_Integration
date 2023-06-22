#!/bin/bash

# Set the directory path where the XML files are located
xml_dir="/home/omrir52/software/Data_Integral/XML"

# Change to the XML directory
cd "$xml_dir" || exit

# Loop through each XML file in the directory
for file in *.xml; do
  # Check if the file is a regular file
  if [[ -f "$file" ]]; then
    echo "Processing $file"
    
    # Run your Python program on the XML file
    python3 /home/omrir52/software/Data_Integral/readXML.py "$file"
    
    echo "Finished processing $file"
  fi
done