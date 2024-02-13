# -*- coding: utf-8 -*-
"""
@author:Jordan Pierre
"""
import pandas as pd
import xarray as xr
import rasterio as rio
import geopandas as gpd
import rasterstats as rstats
import numpy as np
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import netCDF4

nc_fo = r'C:/Users/Jordan/Documents/Bluegreen/GEBCO_07_Dec_2023_7cfdb93e4c12/gebco_2023_n46.2_s45.6_w-2.25_e-1.0.nc'
shp_fo1 = r'C:/Users/Jordan/Documents/Bluegreen/shape/N_Eolien_AO7_Sud_Atlantique_epsg2154_092022_shape/N_Eolien_AO7_Sud_Atlantique_Parc1_epsg2154_S.shp'
shp_fo2 = r'C:/Users/Jordan/Documents/Bluegreen/shape/N_Eolien_AO7_Sud_Atlantique_epsg2154_092022_shape/N_Eolien_AO7_Sud_Atlantique_Parc2_epsg2154_S.shp'


def stat(file_shape,file_dpth):

    shp_df = gpd.read_file(file_shape)
    shp_df = shp_df.to_crs('epsg:4326')

    nc_ds = xr.open_dataset(file_dpth)
    nc_var = nc_ds['elevation']

    affine = rio.open(nc_fo).transform
    nc_arr = nc_var
    nc_arr_vals = nc_arr.values

    S=rstats.zonal_stats(shp_df.geometry, nc_arr_vals, affine=affine, stats="mean min max")
    return(S[0])

def map(shape1,bathy,shape2=False):
    nc1 = netCDF4.Dataset(bathy)
    Blat1 = nc1.variables['lat'][:].data
    Blon1 = nc1.variables['lon'][:].data
    Bdepth1 = nc1.variables['elevation'][:].data
    shp_df1 = gpd.read_file(shape1)
    shp_df1 = shp_df1.to_crs('epsg:4326')

    lat1,lon1 = np.meshgrid (Blat1,Blon1)
    fig,ax = plt.subplots()
    
    if shape2 is False:
        shp_df1.plot(ax=ax,column='Nom',cmap="Spectral",zorder=9,legend=True, legend_kwds={'bbox_to_anchor': (1.9, 1.12)})
       
        CF1=ax.contourf(Blon1,Blat1,Bdepth1,levels=100,cmap='terrain',zorder=1)
        CS1=ax.contour(Blon1,Blat1,Bdepth1,levels=4,colors='teal',zorder=2)
        cbat =fig.colorbar(CF1)
        cbat.set_label('Bathymetry [m]')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        

    else:
        
        shp_df2 = gpd.read_file(shape2)
        shp_df2 = shp_df2.to_crs('epsg:4326')
        
        double = gpd.pd.concat([shp_df1, shp_df2])
        
        double.plot(ax=ax,column='Nom',cmap="Spectral",zorder=9,legend=True, legend_kwds={'bbox_to_anchor': (1.9, 1.12)})
       
        CF1=ax.contourf(Blon1,Blat1,Bdepth1,levels=100,cmap='terrain',zorder=1)
        CS1=ax.contour(Blon1,Blat1,Bdepth1,levels=4,colors='teal',zorder=2)
        cbat =fig.colorbar(CF1)
        cbat.set_label('Bathymetry [m]')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        ax.set_title('Bathymétrie et Position de Parcs Eoliens')
        



map(shp_fo1,nc_fo)
S=stat(shp_fo1,nc_fo)
dict()
