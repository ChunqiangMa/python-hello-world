def SpeedGet(counter_return,type,port_list):
    '''parse the BCM counter return infos--return the speed'''
    try:
        import re
        speed_dic = {}
        for port in port_list:
            name = type + '.' + port            
            pattern = re.escape(name) + '\s+:\s+.+?(\d+(,\d+)*)/s\s'
            #p = re.compile(pattern, re.IGNORECASE | re.DOTALL)
            s=re.search(pattern,counter_return)
            if s:
                #parser the number and delete the ',' in the string
                speed_dic[name] = int(s.group(1).replace(',',''))
                print name, '=', speed_dic[name]
            else:
                strw = recode('获取%s速率信息失败' %name)
                print strw
                return ERROR_RT
    
        return speed_dic    
    except KeyboardInterrupt:
        strW = 'Keyboard interrupt'
        print strW         
        return ERROR_RT
        
def PacketParse(counter_return,type,port_list):
    '''parse the BCM counter return infos--return the port count'''
    try:
        import re
        packet_dic = {}
        for port in port_list:
            name = type + '.' + port            
            pattern = re.escape(name) + '\s+:\s+(\d+(,\d+)*)'
            p = re.compile(pattern, re.IGNORECASE | re.DOTALL)
            s=re.search(p,counter_return)
            if s:
                packet_dic[name] = int(s.group(1).replace(',',''))
                print name, '=', packet_dic[name]
            else:
                strw = recode('获取%s包数量失败' %name)
                print strw
                return ERROR_RT
    
        return packet_dic    
    except KeyboardInterrupt:
        strW = 'Keyboard interrupt'
        print strW         
        return ERROR_RT
