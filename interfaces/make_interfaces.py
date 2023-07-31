import re
from .models import Router_model, Interface_model

###########################################
class Create_router_interfaces():
    Int_types = {'isis enable': 'ISIS',
                 'ip router isis':'ISIS', 
                 'ip binding vpn-instance IPOSS':'IPOSS', 
                 'shutdown': 'Shut Down', 
                 'Shut Down': 'Shut Down', 
                 'LoopBack': 'Loop Back', 
                 'Loopback': 'Loop Back', 
                 'NULL':'Null', 
                 'vty':'Vty', 
                 'vlanif': 'Vlan Interface',
                 "Vlan": 'Vlan'
                 }
    VPN_types = {'xconnect ':               'Xconnect',
                'ip vrf forwarding ':      'IP-vrf-forwarding',
                'mpls l2vc ':              'MPLS-l2',
                'l2 binding vsi ':         'l2-VSI',
                'ip binding vpn-instance ':'vpn-instance' }
    Encapsulation_types = {'qinq vid':                            'QinQ', 
                        'qinq termination pe-vid':             'QinQ',
                        'qinq stacking pe-vid':                'QinQ',
                        'qinq stacking vid':                   'QinQ',
                        'dot1Q ':                              'Dot1q',
                        'dot1q ':                              'Dot1q',
                        'ppp':                                 'PPP',  
                        'switchport trunk allowed vlan':       'Trunk',
                        'port trunk allow-pass ':              'Trunk',
                        'switchport access vlan':              'Access',
                        'port default access vlan':            'Access',
                        'port default vlan ':                  'Access',
                        'port link-type dot1q-tunnel':         'dot1q-tunnel',
                        }
    def __init__(self):
        pass
        
    ###########        
    def Delete_previous_routers(self):
        routers = Router_model.objects.all()
        for item in routers:
            item.delete()
    ###########
    def Create_arouter(self, router):  
        router_name = router.Name
        # Detect brand of a switch or router
        if ((router_name.find("NAR")!= -1)  or (router_name.find("9300")!= -1) or (router_name.find("PRR")!= -1) or 
        (router_name.find("SER")!= -1)  or (router_name.find("NRR")!= -1)  or (router_name.find("2300")!= -1) or
        (router_name.find("5328")!= -1) or (router_name.find("ME60")!= -1) or (router_name.find("2811")!= -1) or 
        (router_name.find("4620")!= -1) or (router_name.find("4680")!= -1) or (router_name.find("5300")!= -1)):
            new_router_Type = 'Huawei'
            self.separator = '#'
        elif ((router_name.find("ZTE")!= -1) ):
            new_router_Type = 'ZTE'
            self.separator = '!'
        else:
            new_router_Type = 'Cisco'
            self.separator = '!'
        
        self.new_router = Router_model(Name = router_name, Type= new_router_Type, IP ='')
        self.new_router.save()
        #print('Saved Router:', router_name)
    ###########

    def Create_interfaces(self, all_int):
        print('$$$$$$$$$$$$$ Create Interfaces...')
        if all_int:
            for item in all_int: 
                int_name = ''
                int_des =''
                int_id =''
                int_ip =''
                int_vpn =''
                int_type = ''
                int_encap = []
                int_profile = ''
                #--------- Find Int Name ----------
                if self.Find_between(item,'interface ','\n'):
                    int_name = self.Find_between(item,'interface ','\n').group(1)
                if int_name:
                    #--------- Find Int Description ----------
                    if self.Find_between(item,'description','\n'):
                        int_des = self.Find_between(item,'description ','\n').group(1)
                        #--------- Find Int Custumer ID ----------
                        if self.Find_between(int_des,'"', '"'):
                            if self.Find_between(int_des,'"', '"').group(1).isdigit():
                                int_id = self.Find_between(int_des,'"', '"').group(1)
                    #--------- Find Int IP ----------
                    if self.Find_between(item,'ip address ','\n'):
                        int_ip = self.Find_between(item,'ip address ','\n').group(1)
                    #--------- Find VPN type ----------
                    for key in self.VPN_types.keys():
                        if self.Find_between(item, key,'encapsulation'):
                            int_vpn = key + self.Find_between(item, key,'encapsulation').group(1)
                            continue
                    #------- Find Encapsulation Type -------------
                    for key in self.Encapsulation_types.keys():
                        if self.Find_between(item,key,'\n'):
                            int_encap.append(key + self.Find_between(item, key,'\n').group(1))
                    #--------- Find Int type ----------
                    for key in self.Int_types.keys():
                        if  item.find(key) != -1:
                            int_type = key
        
                    interface = Interface_model(Router_Name= self.new_router ,
                                                int_Name = int_name,
                                                Description = int_des,
                                                int_ID =  int_id, 
                                                IP =  int_ip,
                                                Profile = int_profile,
                                                VPN = int_vpn,
                                                Encapsulation =  int_encap,
                                                Int_type = int_type)
                    interface.save()
    ###########
    def Create_interfaces_config(self, router_Config_model):
        #create Router object and save it in the database
        self.Create_arouter(router_Config_model)
        # create separate configs for each interface    
        config = router_Config_model.Showrun
        step = 0
        all_int = []
    
        while(1):
            int_line, step = self.Find_Int_Config("interface ", self.separator, config, step)
            int_line = 'interface '+ int_line
            if step == -1:
                break
            else:
                all_int.append(int_line)
        self.Create_interfaces(all_int)
    
    ###########
    def Find_Int_Config(self, start, end, characters, step=0 ):
        my_parameter = ""
            
        start_param = characters.find(start, step)
        if start_param!= -1:
            end_param = characters.find(end, start_param +1)
            if end_param != -1 :
                if ((end_param - start_param) < 600) :
                    my_parameter = characters[start_param + len(start) : end_param-1 ] 
                    return my_parameter, end_param+1
                
            return '', -1
        else:
            return '', -1
    
    ###########

    def Find_between(self, s, first, last):
        try:
            regex = rf'{first}(.*?){last}'
            return re.search(regex, s)
        except ValueError:
            return False
    