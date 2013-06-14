def SendPktTestBCM56844_RT3016(tn,flag='Test'):
    ''''test the RT3016 packet sending and receiving'''
    try:
        cfginfos=globalvar.CFG_INFOS
        f_name = sys._getframe().f_code.co_name
        logpath = os.path.join(globalvar.LOG_DIR, '%s.log'%f_name)          
        section = 'RT3016BCM56844'
        strw = recode('开始收发包测试...')
        print strw
        work.writerunlog(strw)          

        #Go to the BCM shell
        rt = connection.GotoBCM(tn)
        if rt == ERROR_RT:
            return ERROR_RT

        #set the VLAN rule
        num = int(cfginfos[section]['vlannum'])
        for i in range(1,num+1):
            idx = 'vlan' + str(i)
            cmd = cfginfos[section][idx]
            
            prompt = 'BCM\.0>'
            waittime = 10       
            pattern = re.escape(cmd)+'.+'+prompt
            prompt_match = re.compile(pattern,re.IGNORECASE | re.DOTALL) 
            rt = CmdGet(tn,cmd,[prompt_match],int(waittime))
            if rt == ERROR_RT:
                return ERROR_RT
            work.writelogtofile(logpath,rt)
            time.sleep(0.2)
            
        time.sleep(5)
        #set the VLAN rule
        num = int(cfginfos[section]['vlannum'])
        for i in range(1,num+1):
            idx = 'vlan' + str(i)
            cmd = cfginfos[section][idx]
            
            prompt = 'BCM\.0>'
            waittime = 10       
            pattern = re.escape(cmd)+'.+'+prompt
            prompt_match = re.compile(pattern,re.IGNORECASE | re.DOTALL) 
            rt = CmdGet(tn,cmd,[prompt_match],int(waittime))
            if rt == ERROR_RT:
                return ERROR_RT
            work.writelogtofile(logpath,rt)
            time.sleep(0.2)
            
        time.sleep(5)
        #get the port list
        portlist_items = ['portlist','portlist_backplane','portlist_cpu','portlist_other_port']
        for item in portlist_items:
            num_list = check.ParseRange_(cfginfos[section][item])
            if num_list == ERROR_RT:
                strw = recode('%s中%s设置错误'%(section,item))
                print strw
                work.writerunlog(strw)
                return ERROR_RT
            locals()[item] = ['xe'+str(i) for i in num_list] 
              
        rt = LinkCheck(tn,locals()['portlist'])
        if rt == ERROR_RT:
            return ERROR_RT 

        #send the packet
        num = int(cfginfos[section]['sendnum'])
        for i in range(1,num+1):
            idx = 'send' + str(i)
            cmd = cfginfos[section][idx]
            
            prompt = 'BCM\.0>'
            waittime = 10
            pattern = re.escape(cmd)+'.+'+prompt
            prompt_match = re.compile(pattern,re.IGNORECASE | re.DOTALL) 
            rt = CmdGet(tn,cmd,[prompt_match],int(waittime))
            work.writelogtofile(logpath,rt)
            if rt == ERROR_RT:
                return ERROR_RT
            time.sleep(0.5)       
        
        time.sleep(2)
        #send the packet for some time
        sendtime = cfginfos[section]['sendtime']
        time.sleep(int(sendtime))
        
        num = int(cfginfos[section]['errnum'])
        for i in range(1,num+1):
            idx = 'err' + str(i)
            cmd = cfginfos[section][idx]
            
            prompt = 'BCM\.0>'
            tn.write(cmd + ENTER)
            tn.expect([prompt],timeout=5)                                    
            waittime = 10
            strmatch = '(RFCS|RERPKT)\.xe(\d+)'            
            pattern = re.escape(cmd)+'.+'+prompt
            prompt_match = re.compile(pattern,re.IGNORECASE | re.DOTALL)             
            rt = CmdGet(tn,cmd,[prompt_match],int(waittime))
            work.writelogtofile(logpath,rt)
            if rt == ERROR_RT:
                return ERROR_RT
            p = re.compile(strmatch,re.IGNORECASE | re.DOTALL)
            s = p.search(rt)
            if s:
                strw = recode('端口%s收发包测试出现错包'%s.group(2))
                print strw
                work.writerunlog(strw)
                return ERROR_RT

        if flag == 'BurnIn':
            BurnInWait()
                   
        #get the TX speed and RX speed
        speed_dict={}
        for counter in ['RPKT','TPKT']:
            if counter == 'TPKT':
                cmd = cfginfos[section]['gettpkt']
            else:
                cmd = cfginfos[section]['getrpkt']
            
            pattern = cmd + '.+BCM.0>'
            p = re.compile(pattern, re.DOTALL | re.IGNORECASE)
            rt = CmdGet(tn,cmd,[p],10)    
            work.writelogtofile(logpath,rt)
            if rt == ERROR_RT:
                return ERROR_RT        
            rt = SpeedGet(rt,counter,locals()['portlist'])
            if rt == ERROR_RT:
                return ERROR_RT        
            speed_dict[counter]={}
            speed_dict[counter]=rt
        
        for counter in ['RPKT','TPKT']:
            for key,item in speed_dict[counter].items():
                port = key.strip(counter).strip('.')
                if port in locals()['portlist_backplane']:
                    speed = cfginfos[section]['backplane_speed']
                elif port in locals()['portlist_cpu']:
                    speed = cfginfos[section]['cpu_speed']
                elif port in locals()['portlist_other_port']:
                    speed= cfginfos[section]['other_port_speed']
                if int(item) < int(speed):
                    strw = recode('端口%s速率不在范围内'%key)
                    print strw
                    work.writerunlog(strw)
                    return ERROR_RT                     
            
        
        strw = recode('端口的收发包速率正常')
        print strw
        work.writerunlog(strw)
        
        #stop the packet
        num = int(cfginfos[section]['stopnum'])
        for i in range(1,num+1):
            idx = 'stop' + str(i)
            cmd = cfginfos[section][idx]
            
            prompt = 'BCM\.0>'
            waittime = 10
            pattern = re.escape(cmd)+'.+'+prompt
            prompt_match = re.compile(pattern,re.IGNORECASE | re.DOTALL) 
            rt = CmdGet(tn,cmd,[prompt_match],int(waittime))
            work.writelogtofile(logpath,rt)
            if rt == ERROR_RT:
                return ERROR_RT
            time.sleep(0.5)         
        time.sleep(5)        

        num = int(cfginfos[section]['errnum'])
        for i in range(1,num+1):
            idx = 'err' + str(i)
            cmd = cfginfos[section][idx]            
            prompt = 'BCM\.0>'                                 
            waittime = 10
            strmatch = '(RFCS|RERPKT)\.xe(\d+)'            
            pattern = re.escape(cmd)+'.+'+prompt
            prompt_match = re.compile(pattern,re.IGNORECASE | re.DOTALL)             
            rt = CmdGet(tn,cmd,[prompt_match],int(waittime))
            work.writelogtofile(logpath,rt)
            if rt == ERROR_RT:
                return ERROR_RT
            p = re.compile(strmatch,re.IGNORECASE | re.DOTALL)
            s = p.search(rt)
            if s:
                strw = recode('端口%s收发包测试出现错包'%s.group(2))
                print strw
                work.writerunlog(strw)
                return ERROR_RT

        #get the TX speed and RX speed
        counter_dict={}
        for counter in ['RPKT','TPKT']:
            if counter == 'TPKT':
                cmd = cfginfos[section]['gettpkt']
            else:
                cmd = cfginfos[section]['getrpkt']
            
            pattern = cmd + '.+BCM.0>'
            p = re.compile(pattern, re.DOTALL | re.IGNORECASE)
            rt = CmdGet(tn,cmd,[p],10)    
            work.writelogtofile(logpath,rt)
            if rt == ERROR_RT:
                return ERROR_RT        
            rt = PacketParse(rt,counter,locals()['portlist'])
            if rt == ERROR_RT:
                return ERROR_RT        
            counter_dict[counter]={}
            counter_dict[counter]=rt
        
        for c,pkt in counter_dict['RPKT'].items():
            if cfginfos['MODE']['passthrough_pkt_check'] == '0':
                if c[c.find('.')+1:] in locals()['portlist_cpu']:continue                
            if pkt != counter_dict['TPKT'][c.replace('R','T')]:
                strw = recode('端口%s收发包不等'%c.strip('TRPKT.'))
                print strw
                work.writerunlog(strw)
                return ERROR_RT                
        
        strw = recode('端口收发包测试通过')
        print strw
        work.writerunlog(strw)

        if connection.ExitBCM(tn) == ERROR_RT:
            return ERROR_RT
        return SUCCESS_RT
    except KeyboardInterrupt:
        strW = 'Keyboard interrupt'
        print strW         
        return ERROR_RT
