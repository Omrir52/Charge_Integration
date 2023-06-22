#!/bin/bash

# Compile the C++ code
g++ -std=c++11 -o overlay_histograms Overlay.C `root-config --cflags --libs` -lGui -lCore -lImt

# Check if compilation was successful
if [ $? -eq 0 ]; then
    echo "Compilation successful."
else
    echo "Compilation failed."
    exit 1
fi

# Run the compiled program
./overlay_histograms

echo "Script execution completed."
