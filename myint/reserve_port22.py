from .models import Interface
from .models import ReservePort

from os import path

class FindReservePort():
    def __init__(self):
        self.Gateway = None
        self.Gateway_subports = None
        self.filtered_reserved = None
       
        self.Reserved_ports = []
        self.Free_Vlan = []        # free = Port_rangr - Exist - Reserved_Ports
        self.Gateway_PE =''        # equals pe in QinQ interfaces or dot1q in Dot1q interfaces of Gateway
        self.Gateway_CE ='' 
        self.Gateway_Dot1 ='' 
        self.Gateway_encap_type = [] #Gateway's' Encapsulation Type
        self.Gateway_routetrname = None
        self.Gateway_intname = ''
              
    #++++++++++++++++++++++++++++++++++++++++++   
    def Return_gateway(self, dslam_IP):
        Last_oct = 256
        Gateway_subfilter = None
        finded_encap = None

        DSLAM_split = dslam_IP.split(".")
        if (len(DSLAM_split) == 4) and (1 <= int(DSLAM_split[0]) <= 223) and (int(DSLAM_split[0]) != 127) and (int(DSLAM_split[0]) != 169 or int(DSLAM_split[1]) != 254) and (0 <= int(DSLAM_split[1]) <= 255 and 0 <= int(DSLAM_split[2]) <= 255 and 0 <= int(DSLAM_split[3]) <= 255):
            DSLAM_ip1= DSLAM_split[0]
            DSLAM_ip2= DSLAM_split[1]
            DSLAM_ip3= DSLAM_split[2]
            DSLAM_ip4= DSLAM_split[3]

            first_three_part = DSLAM_ip1 +'.'+DSLAM_ip2+'.'+DSLAM_ip3+'.'
            try:
                finded_records= Interface.objects.filter(IP__contains= first_three_part).values()
            except:
                return False
            for record in finded_records:        
                not_mask = record['IP'].split(" ")[0]
                record_forth_part = not_mask.split(".")[3]
                if int(record_forth_part) > int(DSLAM_ip4):
                    if int(record_forth_part) <= Last_oct :
                        Last_oct = int(record_forth_part)
                        full_IP = record['IP']
                        if record['Int_type'] == 'Vlan' or record['Int_type'] =='LoopBack':
                            continue
                        try:
                            self.Gateway = Interface.objects.filter(IP__contains= full_IP).values()
                            print('-----Gateway:--', self.Gateway)
                            myGateway = Interface.objects.get(IP = full_IP) 
                        except:
                            return False
            
            if self.Gateway:
                if self.Gateway[0]['Encapsulation']:
                    #print('++++++++++:', self.Gateway[0]['Encapsulation'])
                    if self.Gateway[0]['Encapsulation'].find('QinQ') != -1:
                        self.Gateway_encap_type = 'QinQ'
                        self.Gateway_PE =  self.Gateway[0]['Encapsulation'].split(',')[1]
                        self.Gateway_PE = self.Gateway_PE[2: len(self.Gateway_PE) -1]
                        self.Gateway_CE =  self.Gateway[0]['Encapsulation'].split(',')[2]  
                        self.Gateway_CE = self.Gateway_CE[2: len(self.Gateway_CE) -2]

                    elif self.Gateway[0]['Encapsulation'].find('Dot1q') != -1:
                        self.Gateway_encap_type = 'Dot1q'
                        self.Gateway_Dot1 =  self.Gateway[0]['Encapsulation'].split(',')[1]  
                    else:
                        return False
                    
                    self.Gateway_intname =       self.Gateway[0]['int_Name'].split('.')[0] 
                    self.Gateway_routetrname =   myGateway.Router_Name.Name
                    self.Gateway_router =        myGateway.Router_Name
                    print('+++++++++++++G.int = ', Gateway_intname)
                    print('+++++++++++++G.Router = ', Gateway_routername)
                    #self.Gateway_routetrname =   self.Gateway_routetrname.Name
                    try:
                        Gateway_subfilter = Interface.objects.filter(int_Name__contains= self.Gateway_intname, Router_Name__Name = self.Gateway_routetrname).values() 
                        if self.Gateway_encap_type == 'QinQ':
                            finded_qinq = Gateway_subfilter.filter(Encapsulation__contains= 'QinQ')
                            if finded_qinq != None:
                                finded_encap = finded_qinq.filter(Encapsulation__contains= self.Gateway_PE)
                        elif self.Gateway_encap_type == 'Dot1q':
                            finded_dot1q = Gateway_subfilter.filter(Encapsulation__contains= 'Dot1q')
                            if finded_dot1q != None:
                                finded_encap = finded_dot1q.filter(int_Name__contains= self.Gateway_intname)
                        
                        if finded_encap != None :
                            self.Gateway_subports = finded_encap
                            print('+++++++++++++G.Sub = ', Gateway_subports)
                    except:
                        Gateway_subfilter = None   
                    
                else:
                    print('=========Encapsulation:', Encapsulation)
                    return False
            else:
                print('=========self.Gateway:', self.Gateway)
                return False 
        else:
            print('=========DSLAM_split:', DSLAM_split)
            return False
    #++++++++++++++++++++++++++++++++++++++++++   
    def Return_FreeVlans(self): 
        return (self.Free_Vlan) 
    #++++++++++++++++++++++++++++++++++++++++++   
    def Return_Intname(self): 
        return (self.Gateway_intname)   
    #++++++++++++++++++++++++++++++++++++++++++ 
    def Return_Router(self): 
        return (self.Gateway_router)
    #++++++++++++++++++++++++++++++++++++++++++   
    def Return_Routername(self): 
        return (self.Gateway_routetrname)  
    #++++++++++++++++++++++++++++++++++++++++++   
    def Return_Encap(self): 
        return (self.Gateway_encap_type)  
    #++++++++++++++++++++++++++++++++++++++++++  
    def Return_PE(self): 
        return (self.Gateway_PE)
    #++++++++++++++++++++++++++++++++++++++++++  
    def Return_CE(self): 
        return (self.Gateway_CE)
    #++++++++++++++++++++++++++++++++++++++++++
    def Return_subports(self): 
        #print('Gateway_encap_type===',     self.Gateway_encap_type)
        #print('Gateway_PE===',             self.Gateway_PE)
        #print('Gateway_CE===',             self.Gateway_CE)
        #print('Gateway_intname===',        self.Gateway_intname)
        #print('Gateway_routetrname===',    self.Gateway_routetrname)
        #print('Free Vlans===',             self.Free_Vlan)
        return (self.Gateway_subports) 
    #++++++++++++++++++++++++++++++++++++++++++
    def Return_reserved_ports(self): 
        return (self.filtered_reserved)
        
    #++++++++++++++++++++++++++++++++++++++++++
     
    def Find_Vlan_inrange(self, start_vlan, end_vlan):
        ''' Find CE vlan if encap=QinQ or Dot1q vlan if encap= Dot1q'''
        self.Free_Vlan = []
        Exist_CE_s = []
        Reserved_CE_s = []
        Port_range = range(start_vlan, end_vlan)
        vlan_range = list(Port_range)
        ###############
        #Find vlans are configured on the existing ports
        if self.Gateway_subports:
            for item in self.Gateway_subports:
                if self.Gateway_encap_type == 'QinQ':
                    port_vlan = item['Encapsulation'].split(',')[2]

                    port_vlan_num =""
                    for i in port_vlan:
                        if i.isnumeric():
                            port_vlan_num += i
                    if port_vlan_num.isnumeric():
                        Exist_CE_s.append(port_vlan_num)
                        
                elif self.Gateway_encap_type == 'Dot1q':
                    port_vlan = item['Encapsulation'].split(',')[1]
                    port_vlan_num =""
                    for i in port_vlan:
                        if i.isnumeric():
                            port_vlan_num += i
                    if port_vlan_num.isnumeric():
                        Exist_CE_s.append(port_vlan_num)
            print('Exist Port Vlans===', Exist_CE_s)
        ##############
        #Find vlans of reserved ports are stored in database
        if self.Gateway:
            all_obj = ReservePort.objects.all()
            print('Reserved Ports ===', all_obj)
            if all_obj:
                filter_obj = all_obj.objects.filter(Int__contains = self.Gateway_intname)
                filter_obj = filter_obj.objects.filter(PE__contains = self.Gateway_PE)
                filter_obj = filter_obj.objects.filter(Int__contains = self.Gateway_intname)
                print('Matched Reserved ===', filter_obj)
                '''
                for counter in all_obj.filter(Int__contains = self.Gateway_intname)
                    if counter['Int'] == self.Gateway_intname:
                        if counter['PE'] == self.self.Gateway_PE:
                            self.filtered_reserved = counter
                            print('===========' , self.filtered_reserved)'''
            #self.filtered_reserved = ReservePort.objects.filter(Router__Name__contains=  self.Gateway_routetrname)
            #self.filtered_reserved = ReservePort.objects.filter(Int__contains = self.Gateway_intname)
            #if self.filtered_reserved:
            #    self.filtered_reserved = self.filtered_reserved.objects.filter(PE__contains = self.Gateway_PE).values()

            if self.filtered_reserved:
                #if orgs.exists():
                # Do this...
                print("xxxxxxxxxx   Reserved Ports with the same Int_name & Router_name as Gateway =", self.filtered_reserved)      
                for item in self.filtered_reserved:
                    Reserved_CE_s.append(str(item['VLAN'])) 
                print("Reserved Port Vlans===", Reserved_CE_s)
        ##############
        finded_vlans = Exist_CE_s + Reserved_CE_s
        #print(str(vlan_range), finded_vlans)            
        if len(finded_vlans) != 0:
            for i in Port_range:
                if str(i) not in finded_vlans:
                    self.Free_Vlan.append(str(i))
        print('(((((((((((self.Free_Vlan)))))))))))))', self.Free_Vlan)
        return (self.Free_Vlan)
