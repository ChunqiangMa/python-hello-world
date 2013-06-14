##转换portrange为一个列表
#
#传入参数的方式
#10001
#10001-10005
#10001-10005,10009
#注意port每位数字只能是五位,中间的连接符号只能是','
def ParseRange(string):
    '''
    传入参数    string  portrange格式的字符串
    返回值      rangelist转换后的列表
                ERROR_RT错误
    '''
    try:
        if not isinstance(string,str):
            strw = recode('传入参数%s不是字符串' %string)
            print strw
            return ERROR_RT
        
        p1 = r'^\d{5}$'
        p2 = r'^\d{5}\-\d{5}$'
        if string.find(',') == -1:
            if re.match(p1, string) == None  and  re.match(p2, string) == None:
                strw = recode('传入参数%s格式错误' %string)
                print strw
                return ERROR_RT        
        else:
            for port in string.split(','):
                port = port.strip()
                if re.match(p1, port) == None  and  re.match(p2, port) == None:
                    strw = recode('传入参数%s格式错误' %string)
                    print strw                  
                    return ERROR_RT            
        
        rangelist = []
        if string.find(',') == -1 and string.find('-') == -1:
            rangelist.append(string)
            return rangelist
        tmplist = string.split(',')        
        for i in tmplist:
            if i.find('-') == -1:
                rangelist.append(i)
            else:
                tmp = i.split('-')
                start = tmp[0].strip()
                end = tmp[1].strip()
                if int(start) > int(end):
                    strw = recode('传入参数%s格式错误' %string)
                    print strw
                    return ERROR_RT
                for j in range(int(start), int(end)+1):
                    rangelist.append(str(j))
        
        for i in rangelist:
            if rangelist.count(i) != 1:
                strw = recode('%s中含有重复的port' %string)
                print strw
                return ERROR_RT
                
        rangelist.sort()
        return rangelist

    except KeyboardInterrupt:
        strw = recode('程序执行中断!')
        print strw
        return OTHER_ERROR
        
    except Exception, err:
        strw = recode('程序异常退出!,ParseRange,异常信息为%s' %err)
        print strw
        return ERROR_RT  
