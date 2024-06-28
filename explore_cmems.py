from reader import Reader, Plot
import matplotlib.pyplot as plt
import numpy as np
folder_name = 'A:/Cian_sinmod/copernicus_client/results/'
yr = 2021
reader = Reader(folder_name, yr)
pld = Plot()
t_range = [31, 59] # february
t_range = [152, 182]# june
t_vals = reader.temp[t_range[0]:t_range[1], 1, :, :]
tv = np.mean(t_vals,0)
pld.plot_temperature(reader, tv)
breakpoint()




plt.contourf(tv)
plt.colorbar