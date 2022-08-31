import numpy as np
import networkx
import pandas as pd
import os
import requests
import json
import cv2
import time 
import shutil 
import random 
import matplotlib.pyplot as plt 

class StreetViewer_random(object):
    def __init__(self, api_key, location, output_directory, picname, size="640x640",
                verbose=True):
        self.picname = picname
        self._key = api_key
        self.location = location
        self.heading = heading
        self.size = size
        self.output_directory = output_directory
        self._meta_params = dict(key=self._key,
                                location=self.location)
        self._pic_params = dict(key=self._key,
                                location=self.location,
                                size=self.size,
                                #heading=self.heading,
                                fov = 120,
                                pitch = 0)
        self.verbose = verbose

    def get_meta(self):
        self.meta_path = "{}meta_{}.json".format(
            self.output_directory, self.location.replace("/", ""))
        self._meta_response = requests.get(
            'https://maps.googleapis.com/maps/api/streetview/metadata?',
            params=self._meta_params)
        self.meta_info = self._meta_response.json()
        # meta_status attribute is used in get_pic method to avoid
        # query when no picture will be available
        self.meta_status = self.meta_info['status']
        if self._meta_response.ok:
            if self.verbose:
                print(">>> Obtained Meta from StreetView API:")
                print(self.meta_info)
            #with open(self.meta_path, 'w') as file:
                #json.dump(self.meta_info, file)
        else:
            print(">>> Failed to obtain Meta from StreetView API!!!")
        self._meta_response.close()

    def get_pic(self):
        self.pic_path = "{}{}.jpg".format(
            self.output_directory, self.picname.replace("/", "")) #probably change the name here 
        #self.header_path = "{}header_{}.json".format(
               # self.output_directory, self.location.replace("/", ""))
            # only when meta_status is OK will the code run to query picture (cost incurred)
        if self.meta_status == 'OK':
                if self.verbose:
                    print(">>> Picture available, requesting now...")
                self._pic_response = requests.get(
                    'https://maps.googleapis.com/maps/api/streetview?',
                    params=self._pic_params)
                self.pic_header = dict(self._pic_response.headers)
                if self._pic_response.ok:
                    if self.verbose:
                        print(f">>> Saving objects to {self.output_directory}")
                    with open(self.pic_path, 'wb') as file:
                        file.write(self._pic_response.content)
                        img=cv2.imread(self.pic_path)
                        #cropped_image = img[0:640, 180:460]
                        cropped_image = img[0:460, 0:640]
                        cv2.imwrite(self.pic_path,cropped_image)
                  #  with open(self.header_path, 'w') as file:
                      #  json.dump(self.pic_header, file)
                    self._pic_response.close()
                    if self.verbose:
                        print(">>> COMPLETE!")
        else:
                print(">>> Picture not available in StreetView, ABORTING!")
            
        def display_pic(self):
            """
            Method to display the downloaded street view picture if available
            """
            if self.meta_status == 'OK':
                plt.figure(figsize=(10, 10))
                img= img.imread(self.pic_path)
                imgplot = plt.imshow(img)
                plt.show()
            else:
                print(">>> Picture not available in StreetView, ABORTING!")

class StreetViewer_heading(object):
    def __init__(self, api_key, location, heading,output_directory, picname, size="640x640",
                verbose=True):
        self.picname = picname
        self._key = api_key
        self.location = location
        self.heading = heading
        self.size = size
        self.output_directory = output_directory
        self._meta_params = dict(key=self._key,
                                location=self.location)
        self._pic_params = dict(key=self._key,
                                location=self.location,
                                size=self.size,
                                heading=self.heading,
                                fov = 120,
                                pitch = 0)
        self.verbose = verbose

    def get_meta(self):
        self.meta_path = "{}meta_{}.json".format(
            self.output_directory, self.location.replace("/", ""))
        self._meta_response = requests.get(
            'https://maps.googleapis.com/maps/api/streetview/metadata?',
            params=self._meta_params)
        self.meta_info = self._meta_response.json()
        # meta_status attribute is used in get_pic method to avoid
        # query when no picture will be available
        self.meta_status = self.meta_info['status']
        if self._meta_response.ok:
            if self.verbose:
                print(">>> Obtained Meta from StreetView API:")
                print(self.meta_info)
            #with open(self.meta_path, 'w') as file:
                #json.dump(self.meta_info, file)
        else:
            print(">>> Failed to obtain Meta from StreetView API!!!")
        self._meta_response.close()

    def get_pic(self):
        self.pic_path = "{}{}.jpg".format(
            self.output_directory, self.picname.replace("/", "")) #probably change the name here 
        #self.header_path = "{}header_{}.json".format(
               # self.output_directory, self.location.replace("/", ""))
            # only when meta_status is OK will the code run to query picture (cost incurred)
        if self.meta_status == 'OK':
                if self.verbose:
                    print(">>> Picture available, requesting now...")
                self._pic_response = requests.get(
                    'https://maps.googleapis.com/maps/api/streetview?',
                    params=self._pic_params)
                self.pic_header = dict(self._pic_response.headers)
                if self._pic_response.ok:
                    if self.verbose:
                        print(f">>> Saving objects to {self.output_directory}")
                    with open(self.pic_path, 'wb') as file:
                        file.write(self._pic_response.content)
                        img=cv2.imread(self.pic_path)
                        #cropped_image = img[0:640, 180:460]
                        cropped_image = img[0:460, 0:640]
                        cv2.imwrite(self.pic_path,cropped_image)
                  #  with open(self.header_path, 'w') as file:
                      #  json.dump(self.pic_header, file)
                    self._pic_response.close()
                    if self.verbose:
                        print(">>> COMPLETE!")
        else:
                print(">>> Picture not available in StreetView, ABORTING!")
            
        def display_pic(self):
            """
            Method to display the downloaded street view picture if available
            """
            if self.meta_status == 'OK':
                plt.figure(figsize=(10, 10))
                img= img.imread(self.pic_path)
                imgplot = plt.imshow(img)
                plt.show()
            else:
                print(">>> Picture not available in StreetView, ABORTING!")

def street_retrieve_random(df, output_direct, api_key):
  api_key = api_key
  count = 0
  path = output_direct
  error_list = []
  for row in df.iterrows():
      lon = row[1]['lon']
      lat = row[1]['lat']
      coordinate = str(lat) + ',' + str(lon)
      output_path = path + str(count) + '.jpg'
      count += 1
      street_image = StreetViewer_random(api_key= api_key,location=coordinate, output_directory= output_path)
      
      street_image.get_meta()
      try: 
        street_image.get_pic()
      except:
        error_list.append(count)
    
bing_api = '' #fill your own bing map api key

def request_map(lat, lon, zoom=12, size=(400,400)):

    base_url = 'https://dev.virtualearth.net/REST/v1/Imagery/Map/'
    
    params = dict(
        centerPoint = str(lat) +','+str(lon),
        mapSize = str(size[0]) + ',' + str(size[1]),
        zoomLevel = zoom,
        imagerySet = 'Aerial',
        BingMapsKey = bing_api
    )

    return requests.get(base_url, params=params)

def get_map(*args, **kwargs):
    return request_map(*args, **kwargs).content

def get_aerial(df, path):
    count = -1
    direct = path
    low_fail = []
    for row in df.iterrows():
       count += 1
       lat = row[1]['lat']
       lon = row[1]['lon']
       try_num = 10
       stamp = False
       flag = False
       while stamp == False:
          if try_num == 0:
            low_fail.append(count)
            flag = True
            break
          try:
             map_response = get_map(lat, lon, 19)
             stamp = True
             time.sleep(0.02)
          except: 
             try_num -= 1
             time.sleep(0.02)
    
       if flag == True:
          continue 
        
       picname = str(count)
       directory = direct + picname
       file = open(directory, "wb")
       file.write(map_response)
       file.close()



