import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import num2date
import cmocean


class Reader:

    def __init__(self, folder_name, yr):
        self.yr = str(yr)
        file_prefix = folder_name + 'CMEMS_GLPHYS_D_full_'
        filename = file_prefix + self.yr + '.nc'
        nc_file = nc.Dataset(filename)
        vtemp = 'thetao'
        vtime = 'time'
        vlon = 'longitude'
        vlat = 'latitude'
        self.temp = nc_file[vtemp]
        time = nc_file[vtime]
        self.time = num2date(time, time.units)
        self.lon = nc_file[vlon]
        self.lat = nc_file[vlat]
        return

class Plot:

    def __init__(self):
        self.figures_path = 'C:/Users/ciank/PycharmProjects/sinmod/copView/figures/'
        self.load_bathymetry()
        return

    def init_plot(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection=ccrs.PlateCarree())
        return

    def plot_temperature(self, reader, temperature):
        self.init_plot()
        self.plot_background()
        plt.contourf(reader.lon[:], reader.lat[:], temperature, levels = np.arange(0, 3, 0.01), transform=ccrs.PlateCarree(), cmap=cmocean.cm.thermal)
        plt.colorbar()
        plt.title(reader.yr + '_june_temperature')
        self.save_plot(plt_name= reader.yr + '_june_temperature')

    def save_plot(self, plt_name):
        savefile = self.figures_path + plt_name + '.png'
        print('Saving file: ' + savefile)
        plt.savefig(savefile, dpi=400)
        plt.close()
        return


    def load_bathymetry(self):
        self.bath_res = 0.04  # bathymetry resolution
        self.bath_file = self.figures_path + 'bath.npy'
        self.bath_file_lon = self.figures_path + 'bath_lon.npy'
        self.bath_file_lat = self.figures_path + 'bath_lat.npy'
        self.bath_contours = np.linspace(0, 3000, 10)
        self.bath = np.load(self.bath_file)
        self.bath_lon = np.load(self.bath_file_lon)
        self.bath_lat = np.load(self.bath_file_lat)
        return

    def plot_background(self):
        land_10m = cfeature.NaturalEarthFeature('physical', 'land', '10m',
                                                edgecolor='face',
                                                facecolor='lightgrey')
        self.ax.add_feature(land_10m)
        self.ax.coastlines(resolution='10m', linewidth=0.7)
        plt.contour(self.bath_lon, self.bath_lat, self.bath, self.bath_contours, colors='k', alpha=0.2,
                    linewidths=0.7,
                    transform=ccrs.PlateCarree())

        # set extent and grid lines;
        gl = self.ax.gridlines(draw_labels=True, alpha=0.4)
        gl.top_labels = False
        gl.right_labels = False
        # self.ax.set_extent(
        # [self.min_lon, self.max_lon, self.min_lat, self.max_lat])
        self.gen_lon_lat_extent()
        self.ax.set_extent(
                [self.min_lon, self.max_lon, self.min_lat,
                 self.max_lat])
        return


    def gen_lon_lat_extent(self):
        # SG extent;
        self.min_lon = -42
        self.max_lon = -32
        self.min_lat = -58
        self.max_lat = -50
        return
