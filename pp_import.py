#########################################################
#
#  Plantar Pressure Import 
#	For inshoe pressure systems with fixed sensor number
#	Uses XArray to build stacked 2D Grid 
#
#	Author D Parker - University of Salford - 30-01-23
#
#########################################################

import os,csv
import xarray as xr
from matplotlib import pyplot	as plt

#########################################################
### Basic Fuctions:

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def import_csv(file, cutpoint=0):
    s = []
    with open(fname, newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)

        for row in reader:
            s.append(row)
    
    return(s)


#########################################################
### System Specific Functions:

# XSENSOR
def XSENSOR_import(fname):
    dat = import_csv(fname)
    
    #XSENSOR FILE CONSTANTS
    sensor_name = dat[8]
    sensor_area = float(dat[12][1])**2
    '''
    #To Calc Coords
    len = 
    wid = 
    '''
    first_frame = 25
    frame_size = 31
    gap_size = 22
    
    #STACK FRAMES UNTIL NO FRAMES REMAIN
    length = len(dat)
    container = []
    s = first_frame
    while length > 31:
        e = s+frame_size
        frame = dat[s:e]
        container.append(frame)
        s = e + gap_size 
        length = length- (frame_size + gap_size)

    #FLOAT AND ADD TO DATASET    
    datasets = []
    for con in range(0,len(container)):
        holder = []
        for i in container[con]:
            res = [float(j) for j in i]
            holder = holder + [res]
        da = xr.DataArray(data=holder,dims=['l','w'])
        datasets.append(da)
    combined = xr.concat(datasets,dim='t')

    return(sensor_name, sensor_area, combined)



#########################################################
### Example Test Code:

f = 'your_file_name.csv'
fext = 'your_file_type'
fdir = 'your_directory'
fname = fdir + f

## Returns XSENSOR data as xarray dataset: 
sensor_name, sensor_area, P_Dataset = XSENSOR_import(fname)

### Simple Xarray functions:
# Peak Pressure Map: highest sensor value for each sesor over time
PP = P_Dataset.max(dim='t')

# Peak Pressure Curve: highest sensor value for each timepoint
PP_Curve = P_Dataset.max(dim=['l','w'])

plt.figure()
plt.plot(PP_Curve)
plt.show()
