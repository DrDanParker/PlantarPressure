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

#Repo Functions:
import pp_import as p_in



fdir = '/workspaces/PlantarPressure/Test_Files/'


arrays = p_in.batch_load(fdir)
for key in arrays:
    P_Dataset = arrays[key].to_array()
    PP_Curve = P_Dataset.max(dim=['l','w'])
    plt.figure()
    PP_Curve.plot()

plt.show()


