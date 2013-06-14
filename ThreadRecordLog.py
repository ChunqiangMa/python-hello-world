def LogRecord(tn,path):
    while True:
        pattern='\n'
        (index,match,data)=tn.expect([pattern],timeout=5)
        work.writelogtofile(path,data)
        if globalvar.Console_print_detect == 'stop':
            return

def ThreadRecordLog(tn_list,path_list):
    import threading
    threads=[]
    num = len(tn_list)
    for i in range(0,int(num)):
        tn=tn_list[i]
        path=path_list[i]
        th = threading.Thread(target=LogRecord,args=(tn,path))
        threads.append(th)
    
    for th in threads:
        th.start() 

def RecordConsolePrint():
    cfginfos = globalvar.CFG_INFOS
    csip = cfginfos['SETTING']['cs_ip']
    csport = cfginfos['SETTING']['cs_port']
    tn1 = connection.TelnetServer(csip, csport)
    if tn1 == ERROR_RT or tn1 == OTHER_ERROR:
        return ERROR_RT
        
    tn2 = connection.TelnetServer(csip, int(csport)+1)
    if tn2 == ERROR_RT or tn2 == OTHER_ERROR:
        return ERROR_RT
        
    tn3 = connection.TelnetServer(csip, int(csport)+2)
    if tn3 == ERROR_RT or tn3 == OTHER_ERROR:
        return ERROR_RT 
    globalvar.Console_print_detect = 'start'
    tn_list = [tn1,tn2,tn3]
    path_list = [os.path.join(globalvar.LOG_DIR, 'ConsolePrint1.log'),os.path.join(globalvar.LOG_DIR, 'ConsolePrint2.log'),os.path.join(globalvar.LOG_DIR, 'ConsolePrint3.log')]
    ThreadRecordLog(tn_list,path_list) 
