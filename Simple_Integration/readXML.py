import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import sys

# Function to change xml to pdf

def replace_last_three_letters(string, replacement):
    if len(string) < 3:
        raise ValueError("String length should be at least 3 characters.")
    if len(replacement) != 3:
        raise ValueError("Replacement should be a string of length 3.")
    return string[:-3] + replacement

# Function to read in digitizer properties

def readDigitizer(r):
    child = r.find('digitizer')
    frequency = child.find('frequency').get('hz')
    samples = child.find('maxsamples').get('maxsamples')
    
    return frequency, samples
 
# Function to read in events
def readEvents(r,freq,name):
    res = 50
    mins = []
    locs = []
    charge  = [] 
    time = []
    charge1 = [] 
    coulombArr = []
    locV = 0
    first_element1 = []
    overflow_location1 = []
    first_element = []
    overflow_location = []
    newArr = []
    tot_charge = 0
    Max_charge = 0
    charge_average = 0
    name = replace_last_three_letters(name,"pdf")

    for a in r.findall('event/trace'):
        testArr = [] # array to hold the voltages of the wave
        st = a.text # read in the voltages
        testArr = [float(b) for b in st.split()] # convert text to float
        mean = sum(testArr)/len(testArr) # mean (claculating the baseline)
        newArr = [(b  - mean) for b in testArr] # array with baseline correction (centered around 0)
        coulombArr = [((float(c)*(10.0**-3)/(res*float(freq)))) for c in newArr] # convert mV array into pC (voltage to charge) (HINT: frequency will give you the time in the bin)
        charge_average = sum(coulombArr)/len(coulombArr)
        for i in range(0,len(newArr)) :
            if (newArr[i] > 100 ):
                first_element.append(newArr[i] * (10.0**-3)/(res*float(freq)))
                #first_element.append(coulombArr[i])
                overflow_location.append(i * 1/float(freq))   
                
        for i in range(0,len(coulombArr)) :
            if (coulombArr[i] > charge_average ):
                #first_element1.append(newArr[i] * (10.0**-3)/(res*float(freq)))
                first_element1.append(coulombArr[i])
                overflow_location1.append(i * 1/float(freq))    
           
        minV,locV,Q = findpeak(coulombArr)
        #put if code , save it to png , limit the number of plots to save individual waves 
        mins.append(minV*(-1))
        charge.append(minV )
        locs.append(locV * 1/ float(freq))
        time.append(locV * 1/float(freq)) 
        charge1.append(float(Q) * (-1)) #     
    
    #print("No of Events",len(time))
    
    # Distribution of charge
    print("\n Charge Distribution ; ", "No of Events",len(time))
    hist,bins,_ = plt.hist(mins,100,color = "brown",lw = 0)
    plt.hist(charge1,bins = 100)
    plt.yscale('log')
    plt.xlabel ("charge [C]")
    plt.ylabel("Events")
    plt.savefig(name,format="pdf")
    #plt.show()
    
    
    # plot for the peak 
    
    print("\n Charge Vs Time Plot for Peak")
    fig,ax = plt.subplots()
    ax.scatter(locs,mins, color= "green")
    ax.set(xlabel ="Time[s]",ylabel="charge[C]")
    #plt.show()   

    #Plot for Time Distribution 
    
    print("\n Time Distribution ; ","No of Events",len(time))
    plt.subplot(211)
    plt.xlabel ("Time [s]")
    plt.ylabel("Events")
    plt.xlim([3e-6, 3.2e-6])
    hist,bins,_ = plt.hist(time,1000,color = "brown",lw = 0)
    
    plt.subplot(212)
    plt.hist(time,bins = 1000)
    plt.yscale('log')
    plt.xlim([3e-6, 3.2e-6])
    plt.xlabel ("Time [s]")
    plt.ylabel("Events")
    #plt.show()
    
    #Plot for Charge Distribution of the peak  
    
    print("\n Minimum recorded charge for each wave ")    
    plt.subplot(211)
    plt.xlabel ("Charge [C]")
    plt.ylabel("Events")
    hist, bins, _  = plt.hist(charge, 100)
    plt.xlim([-4e-11, -6e-11])
    #plt.ylim([0,80])  (Use for 210811 and 210817)
    plt.ylim([0,200])
       
    plt.subplot(212)
    plt.hist(charge,bins = 100)
    plt.yscale('log')
    plt.xlim([-6e-11, -4e-11])
    plt.xlabel ("Charge [C]")
    plt.ylabel("Events")
    #plt.show()
    return charge1
 
    
    

# TODO
   
    
def findpeak(r): # make function to find minimum in array (findpeak)
    min_value = float(r[0])
    loc_value = 0
    total_charge = 0
 #findpeak    

    for i in range (0,len(r)):
        if (min_value > r[i]):
            min_value = r[i]
            loc_value = i
            
#integration code   

    for i in range(loc_value, len(r)):      
        if (r[i] < 0):    
            total_charge += float(r[i])
        else:
            break    
    for i in range(1, loc_value):
        if (r[loc_value - i] < 0):
            total_charge += float(r[loc_value - i])  
        else:
            break      
        
    return(min_value,loc_value,total_charge)

    
# EXTRA: you may end up with more than one peak in a wave, find some way of dealing with it (HINT: Threshold)
def main(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    frequency, samples = readDigitizer(root)
    print(frequency, samples)
    readEvents(root, frequency, xml_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the XML file as a command-line argument.")
        sys.exit(1)
    xml_file = sys.argv[1]
    print(xml_file)
    main(xml_file)
