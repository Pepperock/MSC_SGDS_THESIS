import matplotlib.pyplot as plt
from shapely.geometry import Point
import pandas as pd
import osmnx as ox
import networkx as nxx
import numpy as np
import geopandas as gpd
import os
import random 

bristol_graph = ox.graph_from_place('Bristol, UK', network_type = 'drive')
bristol_nodes = ox.graph_to_gdfs(bristol_graph, edges = False) #network nodes into gdf with point geometry
bristol_lsoa = gpd.read_file("./bristol/lsoa110.shp") #LSOA shp for Bristol
bristol_lsoa = bristol_lsoa.to_crs(epsg = 4326)

bristol_sample = pd.DataFrame({'code':[], 'x':[], 'y':[]})
small_bristol = [] #record samples <10
zero_bristol = [] #record samples = 0

#Sampling: 10 sample locations for every LSOA
for row in bristol_lsoa.iterrows():
  lsoa_name = row[1]['lsoa11cd']
  polygon = row[1]['geometry']
  node_intersect = bristol_nodes[bristol_nodes.intersects(polygon)] #find every node within the current LSOA polygons
  if node_intersect.shape[0] < 10:
    small_bristol.append(lsoa_name)
  if node_intersect.shape[0] == 0:
    zero_bristol.append(lsoa_name)
    continue
  node_df = node_intersect[['x','y']] #the lat and lon of the points
  print(node_df.shape)
  sample_df = node_df.sample(10, replace = True) #sample 10
  sample_df['code'] = lsoa_name
  bristol_sample = pd.concat([bristol_sample, sample_df], axis = 0) #put every df of lsoa and samples into the df dynamically

bristol_sample.to_csv("./data/bristol_sample.csv")


#same process for manchester
man_lsoa = gpd.read_file('./manchester_lsoa.shp')
man_lsoa = man_lsoa.set_crs(epsg = 27700)
man_lsoa = man_lsoa.to_crs(epsg = 4326)
man_g = ox.graph_from_place('Manchester, UK', network_type = 'drive')
man_nodes = ox.graph_to_gdfs(man_g, edges = False)

man_sample = pd.DataFrame({'code':[], 'x':[], 'y':[]})
small_man = []
zero_man = []
for row in man_lsoa.iterrows():
  lsoa_name = row[1]['geo_code']
  polygon = row[1]['geometry']
  node_intersect = man_nodes[man_nodes.intersects(polygon)]
  if node_intersect.shape[0] < 10:
    small_man.append(lsoa_name)
  if node_intersect.shape[0] == 0:
    zero_man.append(lsoa_name)
    continue
  node_df = node_intersect[['x','y']]
  print(node_df.shape)
  sample_df = node_df.sample(10, replace = True)
  #sample_df = sample_df[['x', 'y']]
  sample_df['code'] = lsoa_name
  man_sample = pd.concat([man_sample, sample_df], axis = 0)

man_sample.to_csv('./data/manchester_sample.csv')



from img_retrieve import StreetViewer_random
from img_retrieve import street_retrieve_random

api_key = " " #put your own google street view api

#download street views for bristol and manchester
bristol_path = "./bristol_str_img/"
street_retrieve_random(bristol_sample, bristol_path, api_key)

man_path = "./man_str_img/"
street_retrieve_random(man_sample, man_path, api_key)