from .models import Interface, IP_model, Router, ReservePort1, ReservePort
from .Database5 import A_database
import os
from os import path
import re, sys

VPN_types = {'xconnect ':               'Xconnect',
             'ip vrf forwarding ':      'IP-vrf-forwarding',
             'mpls l2vc ':              'MPLS-l2',
             'l2 binding vsi ':         'l2-VSI',
             'ip binding vpn-instance ':'vpn-instance' }
Encapsulation_types = {'encapsulation qinq vid':              'QinQ', 
                       'qinq termination pe-vid':             'QinQ',
                       'qinq stacking pe-vid':                'QinQ',
                       'qinq stacking vid':                   'QinQ',
                       'qinq vid':                            'QinQ',
                       'dot1q termination vid':               'Dot1q',
                       'vlan-type dot1q':                     'Dot1q',
                       'encapsulation dot1Q ':                'Dot1q',
                       'encapsulation dot1q ':                'Dot1q',
                       'encapsulation ppp':                   'PPP',  
                       'switchport trunk allowed vlan':       'Trunk',
                       'port trunk allow-pass ':              'Trunk',
                       'switchport access vlan':              'Access',
                       'port default access vlan':            'Access'}

class Fill_database():
    def __init__(self):
        self.config_dir = '/home/jamjam/myftp'
        self.full_path = str(path.realpath(self.config_dir))      #Full Path
        self.file_list = os.listdir(self.config_dir)               #All Files 
        
        self.Delete_records()
        self.Read_Router_Files()  
        #self.Migration()
    #++++++++++++++++++++++++++++++++++++++++++   
    def Migration(self):
        i=0
        
        #last_res = ReservePort1()Downloads/8-1-2023-V2/manage.py
        last_database = A_database("/home/jamil/Downloads/8-1-2023-V2/db.sqlite3", "myint_reserveport1")
        last_records = last_database.Select_all()
        last_database.Close_connect()
        #print('++++++++++++', last_records)
        for row in last_records:
            print('++++++++++++',i ,'=', row[0])
            print('++++++++++++Router_Name',i ,'=', row[1])
            print('++++++++++++newID',i ,'=', row[2])
            print('++++++++++++newint',i ,'=', row[3])
            print('++++++++++++Description',i ,'=', row[4])
            print('++++++++++++IP',i ,'=', row[5])
            print('++++++++++++VLAN',i ,'=', row[6])
            print('++++++++++++Rdate',i ,'=', row[7])
            print('++++++++++++',i ,'=', row[8])
            print('++++++++++++Encapsulation',i ,'=', row[9])
            print('++++++++++++PE_vlan',i ,'=', row[10])
            print('++++++++++++User_type',i ,'=', row[11])
            print('++++++++++++',i ,'=', row[12])
            print('++++++++++++',i ,'=', row[13], '\n')
            i+=1
            new_res = ReservePort(
                Router =   Router.objects.get(Name = row[1]),
                Newint =   row[3],
                Peygiri =  row[2],
                Des =      row[4],
                IP =       row[5],
                VLAN =     row[6],
                PE =       row[10],
                Date =     row[7],
                Dayer =    False,
                Info =     ''
            )
            new_res.save()
        
        
    #++++++++++++++++++++++++++++++++++++++++++   
    def Delete_records(self):
        Interface.objects.all().delete()
        IP_model.objects.all().delete()
        Router.objects.all().delete()

    #++++++++++++++++++++++++++++++++++++++++++
    def Find_Int_Param(self,start, end, characters ):
        my_parameter = ""
            
        start_param = characters.find(start)
        end_param = characters.find(end, start_param +1)
        if start_param != -1 :
            my_parameter = characters[start_param + len(start) : end_param ] 
        return my_parameter
    #++++++++++++++++++++++++++++++++++++++++++
    def Find_Int_Parameters(self, start, end, characters, step ):
        my_parameter = ""
            
        start_param = characters.find(start, step)
        if start_param!= -1:
            end_param = characters.find(end, start_param +1)
            if end_param != -1 :
                if ((end_param - start_param) < 6000) :
                    my_parameter = characters[start_param + len(start) : end_param ] 
                    return my_parameter, end_param+1
                
            return '', -1
        else:
            return '', -1   
    
    #********************************************
    #############################################
    #********************************************
    def Set_Port(self, int_config):
        start = "interface "
        end = "\n"
        return( self.Find_Int_Param(start, end, int_config) )
    #********************************************
    def Set_Des(self, int_config):
        start = "description "
        end = "\n"
        return( self.Find_Int_Param(start, end, int_config) )
    #********************************************
    def Set_ID(self, int_config):
        if self.Set_Des(int_config) != "":
            start = "\""
            end = "\""
            ID_str = self.Find_Int_Param(start, end, self.Set_Des(int_config))
            ID_str = ID_str.strip()
            if ID_str.isnumeric():
                return(ID_str)
            else:
                return('')
    #********************************************
    def Set_IP(self, int_config):
        step =0
        int_IP = list("",)
        start = "ip address "
        end = "\n"
        i=0
        
        IP1, step = self.Find_Int_Parameters(start, end, int_config, step )
        while (step!= -1):
            i+=1
            if IP1.split(".")[0].isnumeric():
                int_IP.append(IP1)
                #print('IP: ', IP1)
            IP1, step = self.Find_Int_Parameters(start, end, int_config, step )
        #if i>=2:
        #    print(i, '=', int_IP, '\n')
        return(int_IP)
    #********************************************
    def Set_VPN(self, int_config): 
        VPN = list("",)
        for key, value in VPN_types.items():
            end = "\n"
            if int_config.find(key)!= -1:
                VPN.append(value + ' ')
                start = key
                if key == "xconnect ":
                    end = "encapsulation"  
                VPN.append(self.Find_Int_Param(start, end, int_config).strip())
                return (VPN)
        return (VPN)    
    #********************************************
    def Set_Type(self, int_config):
        int_type=""

        int_type = int_config.find("LoopBack")
        int_type2= int_config.find("Loopback") 
        if  int_type != -1 or int_type2 != -1:
            int_type = "LoopBack"
            return(int_type)
        
        if int_config.find("Vlan") != -1:
            int_type = "Vlan"
            return(int_type)

        int_type = int_config.find("isis enable ")
        if int_type != -1:
            int_type = "ISIS_UpLink"
            return(int_type)
        int_type = int_config.find("ip binding vpn-instance IPOSS")
        if int_type != -1:
            int_type = "IPOSS_Uplink"
            return(int_type)
        int_type = int_config.find("shutdown")
        if  int_type != -1:
            int_type = "Shut Down"
            return(int_type)
        
        
        if int_config.find("ip router isis") != -1:
            int_type = "ISIS_UpLink"
            return (int_type)
        if int_config.find("ip binding vpn-instance IPOSS") != -1:
            int_type = "IPOSS_Uplink"
            return(int_type)
        
        if int_config.find("Vlanif") != -1:
            int_type = "VlanIF"
            return(int_type)
        int_type = int_config.find("NULL")   
        if  int_type != -1:
            int_type = "Null"
            return(int_type)
        int_type = int_config.find("vty")
        if  int_type != -1:
            int_type = "vty"
            return(int_type)

    #++++++++++++++++++++++++++++++++++++
    def Set_Encapsulation(self, int_config): 
        Encap =[]
        for key, value in Encapsulation_types.items():
            end = "\n"
            if int_config.find(key)!= -1:
                Encap.append(value)
                start = key
                if (key == "qinq termination pe-vid") or (key == "encapsulation qinq vid"):
                    end = "ce-vid "  
                    Encap.append(self.Find_Int_Param(start, end, int_config).strip())
                    start = "ce-vid "
                    end = "\n"
                    Encap.append(self.Find_Int_Param(start, end, int_config).strip())
                    return(Encap)
                Encap.append(self.Find_Int_Param(start, end, int_config).strip())
                return(Encap) 
        return(Encap)
                
    #********************************************
    def Set_IP_INET(self, int_config):
        #if int_config.find('ip route vrf INET') != -1 or int_config.find('ip route-static vpn-instance INET') != -1:
        if  int_config.find('ip binding vpn-instance ') != -1:
            start = 'ip binding vpn-instance '
            end = '\n'
            #print('==============', Find_Int_Param(start, end, int_config) )
            return(self.Find_Int_Param(start, end, int_config))
        if int_config.find('ip vrf forwarding ') != -1: 
            start = 'ip vrf forwarding '
            end = '\n'
            #print('==============', Find_Int_Param(start, end, int_config) )
            return(self.Find_Int_Param(start, end, int_config))
        else:
            #print('Not INET..')
            return('')

    #********************************************
    def Set_Profile(self, int_config):
        Prof = ""
        start = "qos-profile"
        end = "inbound"
        step =0
        
        finded, s = self.Find_Int_Parameters(start, end, int_config, step )
        if s != -1:
            Prof = finded
            return Prof
        start = "service-policy input"
        end = "\n"
        finded, s = self.Find_Int_Parameters(start, end, int_config, step )
        if s != -1:
            Prof = finded
            return Prof
    #********************************************
    #############################################
    #********************************************
    def Each_Int_Param(self, int_config): 
        global counter
        int_Encap = list("",)
        int_Profile = ""
        int_VPN = list("",)
        counter =0
        int_Name =          self.Set_Port(int_config)
        int_Description =   self.Set_Des(int_config)
        int_ID =            self.Set_ID(int_config)
        int_IP =            self.Set_IP(int_config)
        int_VPN =           self.Set_VPN(int_config)
        int_Type =          self.Set_Type(int_config)
        int_Encap =         self.Set_Encapsulation(int_config)
        int_Profile =       self.Set_Profile(int_config)
        INET =              self.Set_IP_INET(int_config)
        counter+=1
        #Router_Name int_Name Description int_ID IP Profile VPN Encapsulation Int_type  
        result = [str(int_Name), str(int_Description), str(int_ID), str(int_IP), str(int_Profile), str(int_VPN), str(int_Encap), str(int_Type)] 
        return (result)

    #++++++++++++++++++++++++++++++++++++++++++   
    def Read_Router_Files(self):
        lines = ''
        step = 0
        int_result = list("",)

        if path.isdir(self.config_dir): 
            for each_file in self.file_list:
                if each_file.endswith(".cfg"):
                    #self.Each_Router_Interfaces(self.full_path, each_file)
                    file_name = self.full_path + '/'+ each_file
                    Router_Name = each_file.split('.cfg')[0]
                    lines = ''
                    print('Router= ', Router_Name)
                    
                    try:
                        with open(file_name, 'r', encoding='utf-8') as f:
                            for line in f.readlines():
                                lines += line
                    except Exception as e:
                        print(e)
                    
                    if ((Router_Name.find("NAR")!= -1)  or (Router_Name.find("9300")!= -1) or (Router_Name.find("PRR")!= -1) or 
                        (Router_Name.find("SER")!= -1)  or (Router_Name.find("NRR")!= -1)  or (Router_Name.find("2300")!= -1) or
                        (Router_Name.find("5328")!= -1) or (Router_Name.find("ME60")!= -1) or (Router_Name.find("2811")!= -1) or 
                        (Router_Name.find("4620")!= -1) or (Router_Name.find("4680")!= -1) or (Router_Name.find("5300")!= -1)):
                        device_type = '#'
                    else:
                        device_type = '!'
                    # Write each Router to database
                    if device_type == '#':
                        Router_type = "Huawei"
                    else:
                        Router_type = "Cisco"
                    
                    router_result = [Router_Name, Router_type, '']
                    self.Export_Router_to_database(router_result) 
                    finded_Router= Router.objects.filter(Name= Router_Name)[0]

                    # Write each interface to database
                    step = 0
                    each_router_ips= []           
                    while(1):
                        record =""
                        #Find int config of each interface
                        int_line, step = self.Find_Int_Parameters("interface ", device_type, lines, step)
                        int_line = "interface " + int_line
                        if step == -1:
                            break
                        else:
                            int_result = self.Each_Int_Param(int_line)
                            self.Export_Interface_to_database(int_result, finded_Router)
                            finded_Interface= Interface.objects.filter(int_Name= int_result[0])[0]
                            
                            record = int_result[3]
                            a="sub"
                            b="secondary"
                            
                            if len(record) >= 3:
                                if record.find(a) !=-1:
                                    c= record.split(" ",4)
                                    #print("IP1(sub)= ",c[0][2:], '+++++++++++++ Mask1= ', c[1][ : -2])
                                    #print("IP2= ",c[2], '+++++++++++++ Mask2= ', c[3])
                                    IP1 = c[0][2:]
                                    Mask1 = c[1][ : -2]
                                    #IP=Mask=VRF=Destination=Router=Interface=Parvande=Description=Type=     
                                    IP_result = [IP1, Mask1, int_result[5], "", Router_Name, int_result[2], int_result[1], "Address"]
                                    self.Export_IP_to_database(IP_result, finded_Interface)
                                    IP2 = c[2]
                                    Mask2 = c[3]
                                    IP_result = [IP2, Mask2, int_result[5], "", Router_Name, int_result[2], int_result[1], "Address"]
                                    self.Export_IP_to_database(IP_result, finded_Interface)
                                elif record.find(b) !=-1:
                                    c= record.split(" ",4)
                                    #print("IP1(sec)= ",c[0][2:] ,'+++++++++++++ Mask1= ', c[1])
                                    #print("IP2= ",c[3][1:], '+++++++++++++ Mask2= ', c[4][: -2])
                                    IP1 = c[0][2:]
                                    Mask1 = c[1]
                                    IP_result = [IP1, Mask1, int_result[5], "", Router_Name, int_result[2], int_result[1], "Address"]
                                    self.Export_IP_to_database(IP_result, finded_Interface)
                                    #self.Export_IP_to_database()
                                    IP2 = c[3][1:]
                                    Mask2 = c[4][: -2]
                                    IP_result = [IP2, Mask2, int_result[5], "", Router_Name, int_result[2], int_result[1], "Address"]
                                    self.Export_IP_to_database(IP_result, finded_Interface)
                                    #self.Export_IP_to_database()
                                else:
                                    c= record.split(" ",2)
                                    x = c[0].partition("'")
                                    y = c[1].partition("'")
                                    #print("IP= ",x[2], '+++++++++++++ Mask= ', y[0])
                                    IP = x[2]
                                    Mask = y[0]
                                    IP_result = [IP, Mask, int_result[5], "", Router_Name, int_result[2], int_result[1], "Address"]
                                    self.Export_IP_to_database(IP_result, finded_Interface)
                    
    #********************************************
    
    #********************************************
    def Export_Interface_to_database(self, record, router):
        myinttable = Interface (
            Router_Name =      router,
            int_Name =         record[0],
            Description=       record[1],
            int_ID=            record[2],
            IP=                record[3],
            Profile=           record[4],
            VPN=               record[5],
            Encapsulation=     record[6],
            Int_type=          record[7],
        )
        myinttable.save()

    #********************************************
    def Export_Router_to_database(self, record):
        myroutertable = Router (
            Name =          record[0],
            Type =          record[1],
            IP=             record[2],
        )
        myroutertable.save()
    #********************************************
    def Export_IP_to_database(self, record, Int):
        myroutertable = IP_model (
            IP =            record[0],
            Mask =          record[1],
            VRF=            record[2],
            Destination =   record[3],
            Router=         record[4],
            Int=            Int,
            Parvande=       record[5],
            Description=    record[6],
            Type=           record[7],
        )   
        myroutertable.save()
        
        