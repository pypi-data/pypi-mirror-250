"""
  Product class use Dome API's
"""
import os
import json
import requests
import pandas as pd
from IPython.display import display


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
    
    if bool(respond.json()['success']) is False:
        raise Exception (f"API execution failed with message {respond.json()['message']}")

    api_output = respond.json()['data']
    if (api_output is not None and len(api_output) > 0 ):
        # API output includes both product as well as attributes
        # we will split them and return a dataframe for each 

        # Get attributes array from product
        attributes = api_output.pop('attributes')
        product_df = pd.json_normalize(api_output)
        attributes_df = pd.json_normalize(attributes)

        return product_df, attributes_df
    else: 
       raise Exception (f"No Product found for product {self.productId}")

    

  # Get Product series members
  def series_members(self):   
        
    # Send GET request to Dome API
    respond = requests.get(url=self.dome_api_url['series_members'], headers=self.headers)
    
    if respond.status_code!=200:
        raise Exception (f"Request failed with {respond.status_code} code and {respond.reason} reason")  
    
    if bool(respond.json()['success']) is False:
        raise Exception (f"API execution failed with message {respond.json()['message']}")

    api_output = respond.json()['data']    
    # API returns json 
    # Will format to pandas dataframe
    if (api_output is not None and len(api_output) > 0 ):
        # API output includes both product as well as attributes
        # we will split them and return a dataframe for each 
        df = pd.json_normalize(api_output)
        return df
    else: 
       raise Exception (f"No Product found for product {self.productId}")
    
    
  # Get Product intents
  def intents(self):   
        
    # Send GET request to Dome API
    respond = requests.get(url=self.dome_api_url['intents'], headers=self.headers)
    
    if respond.status_code!=200:
        raise Exception (f"Request failed with {respond.status_code} code and {respond.reason} reason")  

    if bool(respond.json()['success']) is False:
        raise Exception (f"API execution failed with message {respond.json()['message']}")

    api_output = respond.json()['data']
    if (api_output is not None and len(api_output) > 0 ):
        df = pd.json_normalize(api_output)
        return df #respond.json()['data']
    else: 
       raise Exception (f"No Product found for product {self.productId}")


  # Read Product
  def read(self, columns = None, where = None, group_by = None, having = None, order_by = None, limit = None, elevated_access = False):   

    params = {}
    if columns is not None:
        params['columns'] = columns
    if where is not None:
        params['where'] = where 
    if group_by is not None:
        params['group_by'] = group_by
    if having is not None:
        params['having'] = having
    if order_by is not None:
        params['order_by'] = order_by
    if limit is not None:
        params['limit'] = limit
    if elevated_access: 
       params['access_level'] = 'elevated'


      
    url = f"{self.dome_api_url['read']}"
        
    # Send GET request to Dome API
    respond = requests.post(url=url, json=params, headers=self.headers)
    
    if respond.status_code!=200:
        raise Exception (f"Request failed with {respond.status_code} code and {respond.reason} reason") 

    if bool(respond.json()['success']) is False:
        raise Exception (f"API execution failed with message {respond.json()['message']}")

    api_output = respond.json()['data']    
    if (api_output is not None and len(api_output) > 0 ):
        # API returns json
        # Will format to pandas dataframe
        df = pd.json_normalize(api_output)
    else: 
       raise Exception (f"No Product found for product {self.productId}")
    
    
    return df
