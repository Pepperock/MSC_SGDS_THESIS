import pandas as pd
import numpy as np
import os 
import shutil
import random
import time
import requests
from Image_retrieve import get_aerial

bing_api = "Aqo_Xouitwfh2w9fCOusUuBLdbbWVA59mSd0Hc2hBUd2ncK6NeShYzmV8lQkBCnT"
safe_path = "./safe_aerial/" #directory for downloaded imgs
wealth_path = "./wealth_aerial/"
lively_path = "./lively_aerial/"

safe_df = pd.read_csv("./safe_total.csv")
wealth_df = pd.read_csv("./wealth_total.csv")
lively_df = pd.read_csv("./lively_total.csv")

get_aerial(safe_df, safe_path)
get_aerial(wealth_df, wealth_path)
get_aerial(lively_df, lively_path)