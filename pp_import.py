#########################################################
#
#  Plantar Pressure Import
#	For inshoe pressure systems with fixed sensor number
#	Uses XArray to build stacked 2D Grid
#
#	Author D Parker - University of Salford - 30-01-23
#
#########################################################

# %%
import os,csv
import xarray as xr
from matplotlib import pyplot	as plt


#########################################################
### Basic Fuctions:

def chunks(lst, n_size):
    """Yield successive n-sized chunks from lst"""
    for i in range(0, len(lst), n_size):
        yield lst[i:i + n_size]

def import_csv(fname):
    """read csv file into memory"""
    s = []
    with open(fname, newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        for row in reader:
            s.append(row)
    return(s)

def batch_convert(data_path,pressure_syst=None,ext_type='.csv'):
    """converts all full data csv files to xarray"""
    files = os.listdir(data_path)
    print('Converting to nc files:')
    for i in range(len(files)):
        (fileBaseName, fileExtension)=os.path.splitext(files[i])
        if fileExtension == ext_type:
            print(fileBaseName)
            f = data_path + files[i]
            o = data_path + fileBaseName + '.nc'
            print(o)
            if pressure_syst == 'XSENSOR':
                P_DataArray = XSENSOR_import(f)
                ds = xr.Dataset({'pressure':P_DataArray})
                ds.to_netcdf(o)
            
            elif pressure_syst == None:
                print('pressure system not input')

def batch_load(data_path,ext_type='.nc'):
    """load xarray data"""
    input_data = {}
    files = os.listdir(data_path)
    print('importing files:')
    for i in range(len(files)):
        (fileBaseName, fileExtension)=os.path.splitext(files[i])
        if fileExtension == ext_type:
            print(fileBaseName)
            f = data_path + files[i]
            fdat = xr.open_dataset(f)
            input_data[fileBaseName] = fdat
    return(input_data)

#########################################################
### System Specific Functions:

# XSENSOR
def XSENSOR_import(fname):
    """Data import for XSENSOR files"""
    """Currently works for main export not group/mask export"""
    dat = import_csv(fname)
    
    #XSENSOR FILE CONSTANTS
    sensor_name = dat[8]
    sensor_area = float(dat[12][1])**2
    #len = 
    #wid = 
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
        da = xr.DataArray(data=holder,dims=['l','w'],name=sensor_name, attrs={'area':sensor_area})
        datasets.append(da)
    combined = xr.concat(datasets,dim='t')

    return(combined)

#########################################################
### Example Test Code:

file = 'TestWalk1.csv'
fext = '.csv'
fdir = '/workspaces/PlantarPressure/Test_Files/'
filename = fdir + file

arrays = batch_load(fdir)
for key in arrays:
    P_Dataset = arrays[key].to_array()
    PP_Curve = P_Dataset.max(dim=['l','w'])
    plt.figure()
    plt.plot(PP_Curve)

plt.show()

## Batch Convert files to nc:
#batch_convert(fdir,pressure_syst='XSENSOR')

## Returns XSENSOR data as xarray dataset: 
#P_Dataset = XSENSOR_import(filename)

### Simple Xarray functions:
# Peak Pressure Map: highest sensor value for each sesor over time
#PP = P_Dataset.max(dim='t')

# Peak Pressure Curve: highest sensor value for each timepoint
#PP_Curve = P_Dataset.max(dim=['l','w'])

# plt.figure()
# plt.plot(PP_Curve)
# plt.show()
