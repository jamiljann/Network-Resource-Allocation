import os, sys
from os import path
import sys


from .router_class20 import Router
#from interface_class19 import Interface

class Network():    
    def __init__(self):
        config_files_path = str(path.realpath('configs/'))
        #If you need the full system path, you can use os.getcwd() to get the current working directory of your executing code.
        self.file_list = []
        self.all_routers = []
        self.NO_Routers = 0
        self.NO_IDs = 0
        self.NO_Interfaces = 0
        self.NO_FCPs = 0
        self.NO_IPs = 0
          
        dir_list = os.listdir(config_files_path)
        for config_file in dir_list:
            if config_file.endswith(".cfg"):
                self.file_list.append(config_file)     
                self.all_routers.append(Router(config_file))
                self.NO_Routers +=1            
        self._calculate_counters ()
 
    #++++++++++++++++++++++++++++++++++++
    def File_Status(self):     
        if  self.ConfigfilesStatus == "Path OK":
            return True
        else:
            return False
    #++++++++++++++++++++++++++++++++++++
    def _calculate_counters(self):
        for router in self.all_routers:
            self.NO_IDs +=  router.NO_ID()
            self.NO_Interfaces +=  router.NO_Int()
            for ints in router.all_interfaces:
                if ints.FCP:
                    self.NO_FCPs += 1
    #++++++++++++++++++++++++++++++++++++
    def Export_router(self, router_name):
        for router in self.all_routers:
            if router.Name == router_name:
                print("Exporting Router interfaces to Excel File...")
                router.Export_interfaces_excel() 
                
    #++++++++++++++++++++++++++++++++++++
    def Write_Config_Summary(self):
        for router in self.all_routers:
            router.Write_Config_Summary()
            
    #++++++++++++++++++++++++++++++++++++
    def Export_Allrouter_ints(self):
        for router in self.all_routers:
            router.Export_interfaces_excel()
    
    #++++++++++++++++++++++++++++++++++++
    def Show_router_interfaces (self, router_name, int_name = None):
        ''' Return all interfaces of a certain Router or a specific interface of certain Router which is given as an input parameter'''
        result = []
        for router in self.all_routers:
            if router.Name == router_name :
                router_interfaces = router.Show_Interfaces()
                if int_name is not None:
                    if router_interfaces:
                        for each_interface in router_interfaces:
                            if int_name != each_interface[1]:
                                continue
                            result.append (each_interface)
                else:
                    result.append (router_interfaces)
        if len(result) != 0 :
            return result
        else:
            return False
    #++++++++++++++++++++++++++++++++++++
    def Find_ID (self, my_id):
        ''' Return a Port of a Router which has the same Customer ID which is given as input parameter'''
        result = []
        for router in self.all_routers:
            router_interfaces = router.Find_ID(my_id)
            if router_interfaces:
                for each_interface in router_interfaces:
                    result.append (each_interface)
        if result == [] :         
            return False
        else:
            return result 
    #++++++++++++++++++++++++++++++++++++
    def Find_Description (self, my_Desc):
        ''' Return a Port of a Router which has the same Description as input parameter'''
        result = []
        for router in self.all_routers:
            router_interfaces = router.Find_Description(my_Desc)
            if router_interfaces:
                for each_interface in router_interfaces:
                    result.append (each_interface)
        if result == [] :         
            return False
        else:
            return result 
        
    #++++++++++++++++++++++++++++++++++++
    def Find_IP (self, my_IP):
        ''' Return a Port of a specific Router which has the same IP as input parameter'''
        result = []
        for router in self.all_routers:
            router_interfaces = router.Find_IP(my_IP)
            if router_interfaces:
                for each_interface in router_interfaces:
                    result.append (each_interface)
        if result == [] :         
            return False
        else:
            return result 
   
    #++++++++++++++++++++++++++++++++++++     
    def Find_Port (self, int_Name, router_name = None):
        ''' Return a certain Port of a specific Router or of each Router'''
        result = []           
        for router in self.all_routers:
            if router_name is not None:
                if router.Name != router_name:
                    continue
            router_interfaces = router.Find_Port(int_Name)
            if router_interfaces:
                for each_interface in router_interfaces:
                    result.append (each_interface)
        if result == [] :         
            return False
        else:
            return result 
        
    #++++++++++++++++++++++++++++++++++++
    def Find_Router (self, router_name):
        ''' Return a certain Router which has the specific Name'''
        for router in self.all_routers:
            if router.Name == router_name:
                return (router)
    #++++++++++++++++++++++++++++++++++++
    def Router_Type (self, router_name):
        ''' Return Type of a certain Router'''
        for router in self.all_routers:
            if router.Name == router_name:
                return (router.Type)
    #++++++++++++++++++++++++++++++++++++
    def Find_Router_IP (self, router_name):
        ''' Return IP Address of a certain Router'''
        for router in self.all_routers:
            if router.Name == router_name:
                return (router._Router_IP())     
        return (False)
    #++++++++++++++++++++++++++++++++++++
    def Router_List (self):
        routers_name = list("",)
        for router in self.all_routers:
            routers_name.append(router.Name)
        return (routers_name)
    #++++++++++++++++++++++++++++++++++++
    def NO_Router (self):
        ''' Return Number of Routers in the Network'''
        return (self.NO_Routers)
    #++++++++++++++++++++++++++++++++++++
    def NO_ID (self):
        ''' Return Number of Cusromer IDs in the Network'''
        return (self.NO_IDs)
    #++++++++++++++++++++++++++++++++++++
    def NO_inerface (self):
        ''' Return Number of Intetrfaces in the Network'''
        return (self.NO_Interfaces)
    #++++++++++++++++++++++++++++++++++++
    def NO_FCP (self):
        ''' Return Number of FCP Cusromers in the Network'''
        return (self.NO_FCPs)
    #+++++++++++++++++++++++++++++++++++
    def Write_To_File(self, file_name, write_text):
        try:
           f = open(file_name, "a", encoding='utf-8') 
           f.write(write_text)
        finally:
           f.close()
    #++++++++++++++++++++++++++++++++++++ 
    def Find_Free_Ports(self):
        result = []
        i = 0
        for router in self.all_routers:
            Router_IPs = router.Find_Free_Ports()
            for item in Router_IPs:
                result.append(item)
                i +=1

        file_name = "Reports/Free_Ports" + ".xls"
        self.Export_to_excel(result, file_name)
        print('Number of free ports is:',i)
    #++++++++++++++++++++++++++++++++++++   
    def Find_IP_INET(self):
        result = []
        i = 0
        for router in self.all_routers:
            Router_IPs = router.Find_IP_INET()
            for item in Router_IPs:
                result.append(item)
                i +=1
        file_name = "Reports/IPs" + ".xls"
        self.Export_to_excel(result, file_name)

     #++++++++++++++++++++++++++++++++++++
    def Export_to_excel(self, show_int, file_name):  
        '''Each Record contains: ( router_name, self.Name, self.Description, self.Encap, self.ID, self.IP, 
                                   self.VPN, self.Profile, self.Type )'''
        i =1
        my_workbook = xlwt.Workbook()
        sheet = my_workbook.add_sheet("All Network IPs")
        sheet.write(0, 0, 'نام تجهیز')
        sheet.write(0, 1, 'شماره پورت')
        sheet.write(0, 2, 'نام مشترک')
        sheet.write(0, 3, 'شماره پرونده')
        sheet.write(0, 4, 'VPN')
        sheet.write(0, 5, 'Type')
        sheet.write(0, 6, 'Encapsulation')
        sheet.write(0, 7, 'IP')
        sheet.write(0, 8, 'Exist QOS')
        
        for item in show_int:
            sheet.write(i, 0, item[0])
            sheet.write(i, 1, item[1])
            sheet.write(i, 2, item[2])
            sheet.write(i, 3, item[4])
            sheet.write(i, 4, item[6])
            sheet.write(i, 5, item[8])
            sheet.write(i, 6, item[3])
            sheet.write(i, 7, item[5])
            sheet.write(i, 8, item[7])            
            i +=1 

        my_workbook.save(file_name)
    #++++++++++++++++++++++++++++++++++++
    def Find_Gateway (self, DSLAM_IP):
        '''Return Value is : (router.Name, interface.Name, interface.Description, interface.Encap, interface.ID, 
        interface.IP, interface.VPN, interface.Profile, interface.Type ) '''
        Last_oct = 256
        result = []
        DSLAM_split = DSLAM_IP.split(".")
        DSLAM_ip1= DSLAM_split[0]
        DSLAM_ip2= DSLAM_split[1]
        DSLAM_ip3= DSLAM_split[2]
        DSLAM_ip4= DSLAM_split[3]
        counter =0
        for router in self.all_routers:
            if router.Name.find("NAR") != -1 or router.Name.find("SER") != -1:
                for interface in router.all_interfaces:
                    IP_add = interface.IP.rstrip()
                    if IP_add != "":
                        if IP_add.split(".")[0].isnumeric():
                            counter +=1
                            
                            subnet_loc = IP_add.find(" ") 
                            IP_add_withoutsubnet = IP_add[0:subnet_loc ]
                            IP_add_split = IP_add_withoutsubnet.split(".")
                    
                            Port_ip1= IP_add_split[0]
                            Port_ip2= IP_add_split[1]
                            Port_ip3= IP_add_split[2]
                            Port_ip4= IP_add_split[3]
                            
                            if (Port_ip1 == DSLAM_ip1) and (Port_ip2 == DSLAM_ip2) and (Port_ip3 == DSLAM_ip3):
                                if int(Port_ip4) > int(DSLAM_ip4):
                                    if int(Port_ip4) <= Last_oct :
                                        Last_oct = int(Port_ip4)
                                        #my_list= (router.Name, interface.Name, interface.Description, interface.Encap, 
                                        #interface.ID, interface.IP, interface.VPN, interface.Profile, interface.Type )
                                        my_list= interface.Show_Interface(router.Name)
                                        if len(result) != 0 :
                                            result.pop()
                                            #'ISIS_UpLink' or 'IPOSS_Uplink'
                                        #print('Gateway Interface----', my_list )
                                        find_loopback = my_list[1].find('LoopBack')
                                        if ( find_loopback == -1) :
                                                result.append(my_list)        
                                        '''for item in my_list:
                                            if (item == 'ISIS_UpLink') or (item == 'IPOSS_Uplink'):
                                                result.append(my_list) '''       
        self.NO_IPs = counter
        #print('Total IPs in the Network = ', self.NO_IPs)
        if len(result) != 0 :
            return (result)
        else:
            return False

    #++++++++++++++++++++++++++++++++++++
    def List_Gateway_Subports (self, Gateway_router_name, Gateway_int_name, Gateway_encap_type, pe_or_dot1q):  
        result = []
        interfaces = self.Find_Port(Gateway_int_name, Gateway_router_name)
        #print(interfaces)
        #print(len(interfaces))
        if len(interfaces) != 0 :
            if Gateway_encap_type == 'QinQ':     
                for each in interfaces: #each ia a tuple
                    for item in each:
                        if 'QinQ' in item: 
                            #print('Encap++++', item)
                            if item[1] == pe_or_dot1q:
                                result.append(each)
    
            elif Gateway_encap_type == 'Dot1q': 
                for each in interfaces:
                    for item in each:
                        if 'Dot1q' in item: 
                            #print('Encap++++', item)
                            #if item[1] == pe_or_dot1q:
                            result.append(each)      
        #print('Sub Ports:------', result)  
        if result == [] :         
            return False
        else:
            return result 
                
    #+++++++++++++++++++++++++++++++++++"
    def Find_Vlan_inrange(self, show_int_List, Gateway_encap_type):
        ''' Find CE vlan if encap=QinQ or Dot1q vlan if encap= Dot1q'''
        CE_s = []
        encap_type =''
        port_encap = ''
        Port_range = range(2300, 2400)
        
        for each_int in show_int_List:
            port_encap = ''
            encap_type = each_int[3][0] 
            if Gateway_encap_type == 'QinQ':
                if encap_type == Gateway_encap_type :
                    port_encap = each_int[3][2]
            elif Gateway_encap_type == 'Dot1q':
                if encap_type == Gateway_encap_type :
                    port_encap = each_int[3][1]
            else:
                continue
            #print('###Encap of Subints:', encap_type , 'Number: ',port_encap)
            if port_encap != '':
                if port_encap.isnumeric():
                    if int(port_encap) in Port_range:
                        CE_s.append(port_encap) 
        #print('###Vlan Used: ', CE_s)
        return (CE_s)
    #+++++++++++++++++++++++++++++++++++"
    
    #++++++++++++++++++++++++++++++++++++
    def Show_int_config(self, Tree_router_name, Tree_int_name):
        for router in self.all_routers:
            if router.Name == Tree_router_name:
                for each_interface in router.all_interfaces:
                    if each_interface.Name == Tree_int_name:
                        return each_interface.Show_Config()
        
    #++++++++++++++++++++++++++++++++++++
    def Read_DCRM(self, router_name ) :
        '''Read an Excel file as Output of CRM System contains all SLA of Customers to compair with SLA is configured on customer's interface' '''
        filename = "Data-Customers14001224.xls"  
        col_name =""
        my_cel = "Not_Found"
        my_find = False
        result = []
        
        workbook = xlrd.open_workbook(filename)
        sheet1 = workbook.sheet_by_index(0)
        rowsCount = sheet1.nrows
        colsCount = sheet1.ncols
        
        for router in self.all_routers:
            if router.Name == router_name:
                for ints in router.all_interfaces:
                    my_cel = "Not_Found"
                    my_find = False
                    # eliminate FCPs from list of QOS_DCRM
                    if ints.FCP:
                        continue  
                    for i in range(1,rowsCount):
                        for j in range(colsCount):
                            col_name = sheet1.cell_value(0, j)
                            if (col_name == "شماره پرونده"):
                                if sheet1.cell_value(i, j):
                                    if (int(sheet1.cell_value(i, j)) == int(ints.ID)):
                                        my_find = True
                                        continue
                            if my_find:
                                if (col_name == "پهنای باند"):
                                    my_cel = sheet1.cell_value(i, j)
                                    ints.DCRM_Profile = my_cel
                                    my_find = False                   
                    result.append(ints.Show_Interface(router.Name))

            if result == [] :         
                return False
            else:
                return result
            