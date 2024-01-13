from typing import List
import os
from images_collector.tools import GoogleSerperTool
import urllib.request
from logging import Logger
import requests




class Collector:
    

    def __init__(self,api_key : str = None,classes : List[str] = None,images_per_class : int = None):
        self.classes = classes 
        self._serper = GoogleSerperTool()
        self._serper.serper_api_key = api_key
        self._images_per_class = images_per_class
        self._logger = Logger(name="Image collector")

    def load(self):
        if self.classes is not None :
            for _class in self.classes :
                image_count = 0
                while image_count < self._images_per_class :
                    self._serper.page += 1
                    image_count += self._serper.k
                    result = self._serper.results(query = _class)
                    for img in result["images"]:
                        data = requests.get(img["imageUrl"]).content 
                        if os.path.isdir(f"{_class}/") == False :
                            os.mkdir(f"{_class}/")
                        f = open(f"{_class}/{result['searchParameters']['page']}{img['position']}.jpg","wb")
                        f.write(data)
                        f.close()
                        self._logger.log(level=1,msg=f"Loading {img['imageUrl']} in {_class}/{result['searchParameters']}{img['position']}")
                        