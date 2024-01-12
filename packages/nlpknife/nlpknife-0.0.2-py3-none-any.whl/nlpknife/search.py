'''
Description: 搜索类
Version: 0.0.1
Author: aka.zhp
Date: 2023-12-27 15:21:14
LastEditTime: 2024-01-12 14:04:27
'''
import requests
from pprint import pprint
from baidusearch.baidusearch import search

import os
import yaml
CONFIG = yaml.safe_load(open("config/config.yaml", "r"))

bing_search_url = CONFIG["BING_SERARCH_URL"]
bing_subscription_key = CONFIG["BING_SUBSCRIPTION_KEY"]
class SearchAPIUtils:
    def __init__(self,
                 bing_search_url=bing_search_url,
                 bing_subscription_key=bing_subscription_key):
        self.BING_SEARCH_URL = bing_search_url
        self.BING_SUBSCRIPTION_KEY = bing_subscription_key
    
    def search(self, keyword, num_results, search_engine):
        return search_engine(keyword,num_results)
    
    def _baidu_search(self,keyword,num_results=10):
        return search(keyword, num_results=num_results)

    def _bing_search(self,keyword,num_results=10):
        """
        https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
        """
        result = []
        headers = {"Ocp-Apim-Subscription-Key": self.BING_SUBSCRIPTION_KEY}
        params = {
            "q": keyword,
            "count":num_results,
            "offset":0,
            "textDecorations": True,
            "textFormat": "HTML"
            }
        response = requests.get(self.BING_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        web_pages = response.json().get("webPages",None)
        if web_pages:
            value = web_pages.get("value",None)
            if value:
                for each in value:
                    result.append({
                        "title":each["name"],
                        "abstract":each["snippet"],
                        "url":each["url"],
                        "rank":None
                                   })
        return result
  
