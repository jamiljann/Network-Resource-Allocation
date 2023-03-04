import os
from os import path
from Database5 import A_database

int_types = ('ISIS_UpLink', 'IPOSS_Uplink', 'ShutDown', 'LoopBack', 'Vlan', 'NULL', 'vty', 'VlanIF')
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

#********************************************
def Find_Int_Param(start, end, characters ):
    my_parameter = ""
        
    start_param = characters.find(start)
    end_param = characters.find(end, start_param +1)
    if start_param != -1 :
        my_parameter = characters[start_param + len(start) : end_param ] 
    return my_parameter
#********************************************    
def Find_Int_Parameters(start, end, characters, step ):
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
def Set_Port(int_config):
    start = "interface "
    end = "\n"
    return( Find_Int_Param(start, end, int_config) )
#********************************************
def Set_Des(int_config):
    start = "description "
    end = "\n"
    return( Find_Int_Param(start, end, int_config) )
#********************************************
def Set_ID(int_config):
    if Set_Des(int_config) != "":
        start = "\""
        end = "\""
        ID_str = Find_Int_Param(start, end, Set_Des(int_config))
        ID_str = ID_str.strip()
        if ID_str.isnumeric():
            return(ID_str)
        else:
            return('')
#********************************************
def Set_IP(int_config):
    step =0
    int_IP = list("",)
    start = "ip address "
    end = "\n"
    i=0
    
    IP1, step = Find_Int_Parameters(start, end, int_config, step )
    while (step!= -1):
        i+=1
        if IP1.split(".")[0].isnumeric():
            int_IP.append(IP1)
            #print('IP: ', IP1)
        IP1, step = Find_Int_Parameters(start, end, int_config, step )
    #if i>=2:
    #    print(i, '=', int_IP, '\n')
    return(int_IP)
#********************************************
def Set_VPN(int_config): 
    VPN = list("",)
    for key, value in VPN_types.items():
        end = "\n"
        if int_config.find(key)!= -1:
            VPN.append(value + ' ')
            start = key
            if key == "xconnect ":
                end = "encapsulation"  
            VPN.append(Find_Int_Param(start, end, int_config).strip())
            return (VPN)
    return (VPN)    
#********************************************
def Set_Type(int_config):
    int_type=""
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
    int_type = int_config.find("LoopBack")
    int_type2= int_config.find("Loopback") 
    if  int_type != -1 or int_type2 != -1:
        int_type = "LoopBack"
        return(int_type)
    
    if int_config.find("ip router isis") != -1:
        int_type = "ISIS_UpLink"
        return (int_type)
    if int_config.find("ip binding vpn-instance IPOSS") != -1:
        int_type = "IPOSS_Uplink"
        return(int_type)
    if int_config.find("Vlan") != -1:
        int_type = "Vlan"
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
def Set_Encapsulation(int_config): 
    Encap =[]
    for key, value in Encapsulation_types.items():
        end = "\n"
        if int_config.find(key)!= -1:
            Encap.append(value)
            start = key
            if (key == "qinq termination pe-vid") or (key == "encapsulation qinq vid"):
                end = "ce-vid "  
                Encap.append(Find_Int_Param(start, end, int_config).strip())
                start = "ce-vid "
                end = "\n"
                Encap.append(Find_Int_Param(start, end, int_config).strip())
                return(Encap)
            Encap.append(Find_Int_Param(start, end, int_config).strip())
            return(Encap) 
    return(Encap)
            
#********************************************
def Set_IP_INET(int_config):
    #if int_config.find('ip route vrf INET') != -1 or int_config.find('ip route-static vpn-instance INET') != -1:
    if  int_config.find('ip binding vpn-instance ') != -1:
        start = 'ip binding vpn-instance '
        end = '\n'
        #print('==============', Find_Int_Param(start, end, int_config) )
        return(Find_Int_Param(start, end, int_config))
    if int_config.find('ip vrf forwarding ') != -1: 
        start = 'ip vrf forwarding '
        end = '\n'
        #print('==============', Find_Int_Param(start, end, int_config) )
        return(Find_Int_Param(start, end, int_config))
    else:
        #print('Not INET..')
        return('')
#********************************************
def Export_to_database(record):
    global my_database
    my_database.Insert_record(record) 

#++++++++++++++++++++++++++++++++++++
    def Find_H_profile(self):
        Port_qos = ""
    
        Por_location = self.config.find("qos-profile")
        ening = self.config.find("inbound", Por_location + 1) -1
        
        if Por_location != -1 :
            Port_qos = self.config[Por_location + len("qos-profile") +1: ening ]
        self.Profile = Port_qos
    #++++++++++++++++++++++++++++++++++++
    def Find_CR_profile(self):
        Port_qos = ""
      
        Por_location = self.config.find("service-policy input")
        ening = self.config.find("\n", Por_location +1 + len ("service-policy input"))
    
        if Por_location != -1 :
            Port_qos = self.config[Por_location + len("service-policy input") +1: ening ]
    
        self.Profile = Port_qos   
#********************************************
def Set_Profile(int_config):
    Prof = ""
    start = "qos-profile"
    end = "inbound"
    step =0
    
    finded, s = Find_Int_Parameters(start, end, int_config, step )
    if s != -1:
        Prof = finded
        return Prof
    start = "service-policy input"
    end = "\n"
    finded, s = Find_Int_Parameters(start, end, int_config, step )
    if s != -1:
        Prof = finded
        return Prof
    
#********************************************
def Each_Int_Param(int_config, Router_Name): 
    global counter
    int_Encap = list("",)
    int_Profile = ""
    int_VPN = list("",)
    
    int_Name = Set_Port(int_config)
    int_Description = Set_Des(int_config)
    int_ID = Set_ID(int_config)
    int_IP = Set_IP(int_config)
    int_VPN = Set_VPN(int_config)
    int_Type = Set_Type(int_config)
    int_Encap = Set_Encapsulation(int_config)
    int_Profile = Set_Profile(int_config)
    INET = Set_IP_INET(int_config)
    counter+=1
    #Router_Name int_Name Description int_ID IP Profile VPN Encapsulation Int_type  
    result = [ counter, str(int_Name), str(int_Description), str(int_ID), str(int_IP), str(int_Profile), 
              str(Router_Name), str(int_Encap), str(int_VPN), str(int_Type)] 
    #print(int_Encap)
    Export_to_database(result)
   
    return (result)
#********************************************
def Each_Router_Interfaces(full_path, each_file):    
    lines = ''
    step = 0
    all_lines =''
    int_param = list("",)
    IP_route_result =[]
    i=0
    
    file_name = full_path + '/'+ each_file
    Router_Name = each_file.split('.cfg')[0]
    
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
    print('device_type= ', device_type)
    #print('Config= ', lines)
    while(1):
        #Find int config of each interface
        i+=1
        int_line, step = Find_Int_Parameters("interface ", device_type, lines, step)
        int_line = "interface " + int_line
        if step == -1:
            break
        else:
            int_param.append(Each_Int_Param(int_line, Router_Name))
            all_lines += int_line
    
    #print('Router Name= ', Router_Name, '\n                         Number of Interfaces= ', i)
    #print (all_lines)
    return all_lines
#********************************************  


config_dir = '/home/jamjam/myftp'
full_path = str(path.realpath(config_dir))      #Full Path
file_list = os.listdir(config_dir)               #All Files

my_database = A_database("/home/jamjam/20-11-2022/db.sqlite3", "myint_interface")
my_database.Delete_All_record()
print("All records deleted...\n")


counter =1
i=0
if path.isdir(config_dir): 
    for each_file in file_list:
        print('Config= ', each_file)
        if each_file.endswith(".cfg"):
            Each_Router_Interfaces(full_path, each_file)
            i+=1
print('Number of Routers: ', i)     

my_database.Close_connect()    
           
             

 
