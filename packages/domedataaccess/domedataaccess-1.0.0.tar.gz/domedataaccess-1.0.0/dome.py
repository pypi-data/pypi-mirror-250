"""
Class to interact with Dome API's
"""


import os
import json
import requests
import pandas as pd

class Product:
 
 # Initialize Product class
  def __init__(self, productId):
    
    self.productId = productId
    
    # Set request header to Dome APIs
    self.headers = {
                 "Content_Type": "application/json",
                 "Accept": "application/json",
                 "Dome-Token": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJpYXQiOjE2ODA0NTM0NzV9.SlSX6T1DE-la2Slqd-EDwTUu-b9DPb-yvKjbF2WdniQ"
    }
    
    # Set Dome API's URL
    self.dome_api_url = {}
    self.dome_api_url['info'] = f"https://3txpi4x952.execute-api.us-east-1.amazonaws.com/development/api/v1/meta/product/{productId}"
    self.dome_api_url['series_members'] = f"https://la9m90rb7g.execute-api.us-east-1.amazonaws.com/development/api/v1/data/product/{productId}/seriesmembers"
    self.dome_api_url['intents'] = f"https://3txpi4x952.execute-api.us-east-1.amazonaws.com/development/api/v1/meta/intent/product/{productId}"
    self.dome_api_url['read'] = f"https://la9m90rb7g.execute-api.us-east-1.amazonaws.com/development/api/v1/data/product/{productId}"

  # Get Product Information
  def info(self):
    
    # Send GET request to Dome API
    respond = requests.get(url=self.dome_api_url['info'], headers=self.headers)
    
    if respond.status_code!=200:
        raise Exception (f"Request failed with {respond.status_code} code and {respond.reason} reason")
    
    return respond.json()['data']

  # Get Product series members
  def series_members(self):   
        
    # Send GET request to Dome API
    respond = requests.get(url=self.dome_api_url['series_members'], headers=self.headers)
    
    if respond.status_code!=200:
        raise Exception (f"Request failed with {respond.status_code} code and {respond.reason} reason")  
        
    # API returns json
    # Will format to pandas dataframe
    df = pd.DataFrame.from_records(respond.json()['data'])
    
    return df
    
  # Get Product intents
  def intents(self):   
        
    # Send GET request to Dome API
    respond = requests.get(url=self.dome_api_url['intents'], headers=self.headers)
    
    if respond.status_code!=200:
        raise Exception (f"Request failed with {respond.status_code} code and {respond.reason} reason")  
        
    return respond.json()['data']

  # Read Product
  def read(self, limit = None):   
        
    if limit is not None:
        url = f"{self.dome_api_url['read']}?limit={limit}"
    else:
        url = f"{self.dome_api_url['read']}"
        
    # Send GET request to Dome API
    respond = requests.get(url=url, headers=self.headers)
    
    if respond.status_code!=200:
        raise Exception (f"Request failed with {respond.status_code} code and {respond.reason} reason") 
        
    # API returns json
    # Will format to pandas dataframe
    df = pd.DataFrame.from_records(respond.json()['data'])
    
    return df
