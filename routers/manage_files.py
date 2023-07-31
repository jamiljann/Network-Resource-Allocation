from .models import RouterConfig_model
import os
import re, sys
from os import path
from datetime import date
import datetime

class Read_configfiles():
    def __init__(self):
        self.config_dir = '/home/jamil/2023/reproject/allconfigs/routers/myftp'
        self.full_path = str(path.realpath(self.config_dir))       #Full Path
        self.file_list = os.listdir(self.config_dir)               #All Files    
    #++++++++++++++++++++++++++++++++++++++++++   
    def Read_Router_Files(self):
        i=1
        lines =''
        if path.isdir(self.config_dir): 
            for each_file in self.file_list:
                if each_file.endswith(".cfg"):
                    Router_Name = each_file.split('.cfg')[0]
                    print (i,'-Router Name= ', Router_Name)
                    i+=1
                    file_name = self.full_path + '/'+ each_file
                    try:
                        with open(file_name, 'r', encoding='utf-8') as f:
                                for line in f.readlines():
                                     lines += line
                        t= os.path.getmtime(file_name)
                        Database_router = RouterConfig_model(Name = Router_Name, 
                                                            Showrun = lines,
                                                            Filedate= datetime.datetime.fromtimestamp(t))
                        Database_router.save()
                    except Exception as e:
                         print('Error while openning a config File.',e)
    #++++++++++++++++++++++++++++++++++++++++++   
    def Delete_Router_Files(self):
                i =1
                Database_router = RouterConfig_model.objects.all()
                for router in Database_router:
                      i += 1
                      print(i, '-Router =', router.Name, " is deleted.")
                      router.delete()

                    
        
        
        
        
