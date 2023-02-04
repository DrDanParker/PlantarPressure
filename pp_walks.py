#########################################################
#
#  Plantar Pressure Walks 
#	For identifying gait features in plantar pressure data
#
#	Author D Parker - University of Salford - 31-01-23
#
#########################################################

# %%

#Dependencies: 
import xarray as xr
from matplotlib import pyplot	as plt
from scipy.signal import find_peaks

#Repo Functions:
import pp_import as p_in



fdir = '/workspaces/PlantarPressure/Test_Files/'


arrays = p_in.batch_load(fdir)
for key in arrays:
    P_Dataset = arrays[key].to_array()
    PP_Curve = P_Dataset.max(dim=['l','w'])
    peaks = find_peaks(PP_Curve, height=200, threshold=5, distance=40)
    
    plt.figure()
    PP_Curve.plot()
    plt.plot(peaks[0],peaks[1]['peak_heights'], '*')

plt.show()


