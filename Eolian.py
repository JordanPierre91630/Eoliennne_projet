# -*- coding: utf-8 -*-
"""
@author:Jordan Pierre
"""
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import numpy as np
import netCDF4


nc1 = netCDF4.Dataset('C:/Users/Jordan/Documents/Bluegreen/GEBCO_07_Dec_2023_7cfdb93e4c12/gebco_2023_n46.2_s45.6_w-2.25_e-1.0.nc')
Blat1 = nc1.variables['lat'][:].data
Blon1 = nc1.variables['lon'][:].data
Bdepth1 = nc1.variables['elevation'][:].data

shape1 = gpd.read_file("C:/Users/Jordan/Documents/Bluegreen/shape/N_Eolien_AO7_Sud_Atlantique_epsg2154_092022_shape/N_Eolien_AO7_Sud_Atlantique_Parc1_epsg2154_S.shp")
shape2 = gpd.read_file("C:/Users/Jordan/Documents/Bluegreen/shape/N_Eolien_AO7_Sud_Atlantique_epsg2154_092022_shape/N_Eolien_AO7_Sud_Atlantique_Parc2_epsg2154_S.shp")
projo1= shape1.to_crs('epsg:4326')
projo2= shape2.to_crs('epsg:4326')


lat1,lon1 = np.meshgrid (Blat1,Blon1)
fig,ax1 = plt.subplots(layout='constrained')
projo1.plot(ax=ax1,color='orange', edgecolor='chocolate',zorder=10)
projo2.plot(ax=ax1,color='royalblue', edgecolor='navy',zorder=9)
CF1=ax1.contourf(Blon1,Blat1,Bdepth1,levels=100,cmap='terrain',zorder=1)
CS1=ax1.contour(Blon1,Blat1,Bdepth1,levels=4,colors='teal',zorder=2)
cbat =fig.colorbar(CF1)

