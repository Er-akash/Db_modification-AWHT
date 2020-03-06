import sqlite3
from datetime import datetime
import sys
import xlrd
import xlsxwriter
from xlutils.copy import copy
from os.path import isfile, join
import os.path
sys.path.insert(1, '/home/pi/Desktop/AWHT/code/tester_files')
import global_test_var as GV
# =============================================================================
# 
# =============================================================================
def sql_connection():##establish connection with database and return class
    try:
        GV.conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
        print("Connection is established: Database is created in memory")
    except:
        print("error in conn")
    
def sql_Close():## close connection with db
    GV.conn.close()
# =============================================================================
#  
# =============================================================================
def DownLoadCableId_boot(): ##dowload  data in Hlist Location_No PartName from db
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database = conn.cursor()
    sql_statement ="SELECT max(LastUsed) from tblCable_Id"
    my_database.execute(sql_statement)
    output = my_database.fetchall()
     
    sql_statement = "SELECT Location,PartName from tblCable_Id where LastUsed = '"+output[0][0]+"'"
    my_database.execute(sql_statement)
    hlist = my_database.fetchall()
    #print("output",hlist)
    return(hlist)

def DownLoadCableId_change(Location_No):##update data in Hlist PartName frm db
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    Location=Location_No
    my_database = conn.cursor()

    try:
      sql_statement= "SELECT PartName from tblCable_Id where Location = "+str(Location)
      my_database.execute(sql_statement)
      hlist = my_database.fetchall()
      print("DownLoadCableId_change",hlist[0][0])
      return(hlist)
    except:
      print('name not found please insert')

def UpLoadCableId(Location_No,Part_Name):##update Location Part_Name
    print ('Location_No,Part_Name',Location_No,Part_Name)
    Location = Location_No
    PartName = Part_Name
    LastUsed=datetime.now()
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database = conn.cursor()
    sql_statement = "SELECT count(PartName) from tblCable_Id where Location="+str(Location)
    my_database.execute(sql_statement)
    n = my_database.fetchone()[0]
    print('my_database',n)
    if(n == 0):
        print("check point",Location,PartName,LastUsed)
        my_database.execute('INSERT  into tblCable_Id(Location,PartName,LastUsed) values(?,?,?)',(Location,PartName,LastUsed))
        conn.commit()
    else:    
        my_database.execute('update tblCable_Id set PartName = ?, LastUsed = ? where Location = ?',(PartName,LastUsed,Location))
        conn.commit()
    conn.close()
    
def DownloadCableId_All():##update Location Part_Name
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database = conn.cursor()
    sql_statement = "SELECT Location,PartName from tblCable_Id"
    #sql_statement = "SELECT * from tblCable_Id"
    my_database.execute(sql_statement)
    n =my_database.fetchall()
##    print(n)
    return(n)
# =============================================================================
# 
# =============================================================================
def UploadCable_Info(Location_No,x):##upload (CableInfo_Location,PassCount,FailCount,Stage1,Stage1Points,Stage2,Stage2Points) in db
    Local_Cable_Info=x
    CableInfo_Location=Location_No;
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database=conn.cursor()
    sql_statement = "SELECT count(CableInfo_Location) from tblCable_Info where CableInfo_Location="+str(CableInfo_Location)
    my_database = conn.execute(sql_statement)
    n = my_database.fetchone()[0]
    print('n',n)
    if(n == 0):
        my_database.execute('insert into tblCable_Info(CableInfo_Location,PassCount,FailCount,Stage1,Stage1Points,Stage2,Stage2Points) values(?,?,?,?,?,?,?)',(CableInfo_Location,Local_Cable_Info[0][0],Local_Cable_Info[0][1],Local_Cable_Info[0][2],Local_Cable_Info[0][3],Local_Cable_Info[0][4],Local_Cable_Info[0][5]))
    else:    
        my_database.execute('update tblCable_Info set PassCount = ?, FailCount = ?,Stage1 = ?, Stage1Points = ?,Stage2 = ?, Stage2Points = ? where CableInfo_Location = ?',(Local_Cable_Info[0][0],Local_Cable_Info[0][1],Local_Cable_Info[0][2],Local_Cable_Info[0][3],Local_Cable_Info[0][4],Local_Cable_Info[0][5],CableInfo_Location))
    conn.commit()
  
def DownloadCable_Info(Location_No):##download (CableInfo_Location,PassCount,FailCount,Stage1,Stage1Points,Stage2,Stage2Points) in ram
    CableInfo_Location=Location_No
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database=conn.cursor()
    try:
        sql_statement = "SELECT PassCount,FailCount,Stage1,Stage1Points,Stage2,Stage2Points from tblCable_Info where CableInfo_Location="+str(CableInfo_Location)
        my_database = conn.execute(sql_statement)
        x = my_database.fetchall()
        #print("Local_Cable_Info",x)
        return(x)
    except :
        print('Record not found please create')
        
def DownloadCable_Info_all():##update Location Part_Name
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database = conn.cursor()
    sql_statement = "SELECT Stage1Points,Stage2Points from tblCable_Info"
    #sql_statement = "SELECT * from tblCable_Id"
    my_database.execute(sql_statement)
    n =my_database.fetchall()
##    print(n)
    return(n)
# =============================================================================
# 
# =============================================================================
def DownloadConfiguration(Location_No):
    #print('Location_No',Location_No)
    Confi_Location=Location_No
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database =conn.cursor()
    sql_statement = "SELECT Model,HWVersion,SWVersion,LeakageFixNo,LeakageChannel from tblConfiguration \
                    where Id ="+str(Confi_Location)
    my_database.execute(sql_statement)
    output = my_database.fetchall()
    print('output',output)
    return(output)

def uploadConfiguration(lf):
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database=conn.cursor()
    my_database.execute('update tblConfiguration set LeakageFixNo = ? where Id =?',(lf,1))
    conn.commit()

# =============================================================================.
# 
# =============================================================================

def DownloadGlobal_Grp1():
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database = conn.cursor()
    sql_statement = "SELECT ContunityPointNos from tblGlob_Grp1"
   # sql_statement = "SELECT ContunityPointNos,Image from tblGlob_Grp1"
##    print(sql_statement)
    my_database.execute(sql_statement)
    output = my_database.fetchall()
    print('output',output)  
    conn.close()
    return(output)
    
def UploadGlobal_Grp1(Location_No,lgrp1):##Local_Group1_File = [(1,2,3,None,1,10)]
    tuple_Data = lgrp1
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database=conn.cursor()    
   
    for x in range(len(tuple_Data)):
        for y in range(len(tuple_Data[x])):
            print(Location_No,y+1,tuple_Data[x][y])
            my_database.execute('insert into tblGlob_Grp1(ContunityPointNos,Image) values(?,?)',(tuple_Data[x][y],"/home/pi/"))
            conn.commit()
# =============================================================================
# 
# =============================================================================

def myfunc(myTuple,GrpNo,n_tuple_coordinate):
    t=0;
    for point in myTuple:
        print('Point',point)
        my_database.execute('insert into tblGlob_Grp2(GroupNo,Point,XPosition,YPosition) values(?,?,?,?)',(GrpNo,point,n_tuple_coordinate[t][0],n_tuple_coordinate[t][1]))
        conn.commit() 
        t += 1

def UploadGlobal_Grp2(n_tuple_Data,n_tuple_coordinate):
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database=conn.cursor() 
    n_tuple_Data = [(1,5),(3,8,12),(9,10),(15,18,24),(18,19,20)]
    n_tuple_coordinate=[((1,1),(2,2)),((36,37),(4,4),(5,5)),((6,6),(7,7)),((8,8),(9,9),(10,10)),((8,8),(9,9),(10,10))]
    n_tuple_coordinate_cnt=0;
    GrpNo=1;
    for myTuple in n_tuple_Data:
        myfunc(myTuple,GrpNo,n_tuple_coordinate[n_tuple_coordinate_cnt])
        GrpNo += 1
        n_tuple_coordinate_cnt +=1

def DownloadGlobal_Grp2():
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database=conn.cursor() 
    sql_statement = "SELECT GroupNo,Point from tblGlob_Grp2"
    my_database.execute(sql_statement)
    output = my_database.fetchall()
    print('grp2_global',output)

    tp=[[] for i in range(128)]

    key=0
    for y in range(len(output)):
        key=output[y][0]
        for x in range(1,len(output[y])):
            tp[key-1].append(output[y][x])
##    print("tp",tp)
    return(output)
# =============================================================================
# 
# =============================================================================
def DownloadGLobal_Cable_Settings():
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database=conn.cursor()
    sql_statement = "SELECT ReleaseTime,QMarkTime,BuzzerStatus,ExtraPointTest,CutterStatus\
                    ,OpenPointTime,ShortPointTime,InterChangeTime,ExtraPointTime,LablePrint\
                    ,LableNos,BarCodeMatch,BarcodeNos,Diode,DiodeChannelNos\
                    ,OutRelay,OutRelayChannelNos,Sensor,SensorChannelNos,InRelay\
                    ,InRelayChannelNos,Resistance,ResistanceChannelNos,Capacitance,CapacitanceChannelNos\
                    ,LowResistance,LowResistanceChannelNos,mASignal,mASignalChannelNos,VSignal\
                    ,VSignalChannelNos,Insulation,InsulationChannelNo,OpticFiber,OpticFiberChannelNos\
                     from tblGlob_Settings "
                   
    my_database.execute(sql_statement)
    x = my_database.fetchall()
    print('x',x)
    if(len(x)==0):
        print('Record not found please create')
    else:
        return(x)
# =============================================================================
# 
# =============================================================================
def DownloadHarnessData(Location_No):##dowload circuits data of pass  location no from db
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database = conn.cursor()
    sql_statement = "SELECT NetNo,Point1,Point2 from tblHarness_Data where HarnessData_Location="+str(Location_No)
    my_database.execute(sql_statement)
    output = my_database.fetchall()
    
    for x in range (len(output)):
        if None in output[x]:
            hlist=list(output[x])
            hlist.remove(None)
            output[x]=tuple(hlist)
    #print('output',output)

    maxnum=0
    for y in range(len(output)):
        key=output[y][0]
        maxnum=max(maxnum,key)
    tp=[[] for i in range(maxnum)]
   
    key=0
    for y in range(len(output)):
        key=output[y][0]
        for x in range(1,len(output[y])):
            tp[key-1].append(output[y][x])
    #print("tp",tp)
    
    for x in range (len(tp)):
        GV.circuits.append([])
        for y in range (len(tp[x])):
            GV.circuits[x].append(tp[x][y])
    return(output)
##    print('DownloadHarnessData',output)
def UploadHarnessData(Location_No):##upload  circuits data of pass  location no ram to db
    print("harness save")
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    Data=[]
    HarnessData_Location=Location_No
    my_database =conn.cursor()
    sql_statement ='DELETE FROM tblHarness_Data WHERE HarnessData_Location ='+str(Location_No)
    my_database.execute(sql_statement)
    
    if(len(GV.circuits)>0): 
        for x in range(len(GV.circuits)):
            Data.append(())
            if not((len(GV.circuits[x]) % 2) == 0):
                GV.circuits[x].append(None)
            Data[x]=tuple(GV.circuits[x])
        #print(Data)

        for NetNo in range(len(Data)):
            for sub_point in range(round(len(Data[NetNo])/2.0)):
                #print(Data[NetNo][sub_point*2],Data[NetNo][(sub_point*2)+1])
                my_database.execute('insert into tblHarness_Data(HarnessData_Location,NetNo,Point1,Point2) values(?,?,?,?)',(HarnessData_Location,NetNo+1,Data[NetNo][sub_point*2],Data[NetNo][(sub_point*2)+1]))
    conn.commit()          
    conn.close()

def Harnesdata_excel(Location_No):
    storage_path = '/home/pi/Desktop/AWHT/DB'
    try:
        os.mkdir(storage_path + '/' + str(Location_No))
    except FileExistsError:
        print('folder exist')
##    DownloadHarnessData(GV.Location_No)
    DownloadLocal_Grp2(GV.Location_No)
    print('Local_Group2_File1111',GV.Local_Group2_File)
    num_pt=map(len,GV.circuits)
    total_ckt_pt=sum(num_pt)
    hrn_file= storage_path + '/' + str(Location_No) + '/'+'Hrn.xls'
    grp2_file= storage_path + '/' + str(Location_No) + '/'+'Grp2.xls'
    workbook = xlsxwriter.Workbook(hrn_file)
    worksheet = workbook.add_worksheet()
    worksheet.write(0,0,str(total_ckt_pt))
    for i in range(len(GV.circuits)):
            read=(GV.circuits[i])
            for j in range(len(read)):
                display_points=read[j]
                worksheet.write(i+1,j,str(display_points))
    workbook.close()

    workbook = xlsxwriter.Workbook(grp2_file)
    worksheet = workbook.add_worksheet()
    for i in range(len(GV.Local_Group2_File)):
        grp2_data=GV.Local_Group2_File[i]
        for j in range(len(grp2_data)):
            grp_pts=grp2_data[j]
            worksheet.write(i,j,str(grp_pts))
    workbook.close()
    print('Harnesdata_excel',GV.circuits)
# =============================================================================
# 
# =============================================================================
def Download_Help():
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database = conn.cursor()
    sql_statement = "SELECT IsActive from tblHelp Where Id=1"
    my_database.execute(sql_statement)
    n =my_database.fetchall()
    print(n[0][0])
    return(n[0][0])

def Upload_Help(lt):
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database=conn.cursor()
    my_database.execute('update tblHelp set IsActive = ? where Id =?',(lt,1))
    conn.commit()
# =============================================================================
# 
# =============================================================================
def DownloadLocal_Grp1(Location_No):
    print('Location_No',Location_No)
    LocalGrp1_Location=Location_No
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database = conn.cursor()
    sql_statement = "SELECT Group_No,ContunityPointNos from tblLocal_Grp1 \
                    where LocalGrp1_Location ="+str(LocalGrp1_Location)
    #print(sql_statement)
    my_database.execute(sql_statement)
    output = my_database.fetchall()
    #print('output',output)
    
    tp=[[] for i in range(128)]
    key=0
    for y in range(len(output)):
        key=output[y][0]
        for x in range(1,len(output[y])):
            tp[key-1].append(output[y][x])
    print("tp",tp)
    GV.Local_Group1_File=tp
    return(output)

def UploadLocal_Grp1(Location_No,lgrp1):##Local_Group1_File = [(1,2,3,None,1,10)]
    tuple_Data = lgrp1
    LocalGrp1_Location=Location_No
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database=conn.cursor()    
    sql_statement ='DELETE FROM tblLocal_Grp1 WHERE LocalGrp1_Location ='+str(Location_No)
    my_database.execute(sql_statement)

    for x in range(len(tuple_Data)):
        for y in range(len(tuple_Data[x])):
            print(Location_No,y+1,tuple_Data[x][y])
            my_database.execute('insert into tblLocal_Grp1(LocalGrp1_Location,Group_No,ContunityPointNos,Image) values(?,?,?,?)',(LocalGrp1_Location,y+1,tuple_Data[x][y],"/home/pi/"))
            conn.commit()
# =============================================================================
# 
# =============================================================================
def DownloadLocal_Grp2(Location_No):
    LocalGrp2_Location=Location_No
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database = conn.cursor()
    sql_statement = "SELECT GroupNo,Point from tblLocal_Grp2 where LocalGrp2_Location ="+str(LocalGrp2_Location)
    my_database.execute(sql_statement)
    output = my_database.fetchall()
    tp=[[] for i in range(128)]
    key=0
    for y in range(len(output)):
        key=output[y][0]
        for x in range(1,len(output[y])):
            tp[key-1].append(output[y][x])
    GV.Local_Group2_File=tp
    print("Local_Group2_File111",GV.Local_Group2_File)
    return(GV.Local_Group2_File)

def UploadLocal_Grp2(Location_No,lgrp2):
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database=conn.cursor()    
    tuple_Data =lgrp2
    LocalGrp2_Location=Location_No
    
    sql_statement ='DELETE FROM tblLocal_Grp2 WHERE LocalGrp2_Location ='+str(Location_No)
    my_database.execute(sql_statement)
    
    for x in range(len(tuple_Data)):
        for y in range(len(tuple_Data[x])):
            print(Location_No,x+1,tuple_Data[x][y])
            my_database.execute('insert into tblLocal_Grp2(LocalGrp2_Location,GroupNo,Point,XPosition,YPosition) values(?,?,?,?,?)',(LocalGrp2_Location,x+1,tuple_Data[x][y],1,2))
    conn.commit()
# =============================================================================
# 
# =============================================================================
def DownloadCable_Settings(Location_No):
    print("Location_No....",Location_No)
    
    LocalSettings_Location=Location_No;
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database=conn.cursor()
    
    sql_statement = "SELECT ReleaseTime,QMarkTime,BuzzerStatus,ExtraPointTest,CutterStatus\
                    ,OpenPointTime,ShortPointTime,InterChangeTime,ExtraPointTime,LablePrint\
                    ,LableNos,BarCodeMatch,BarcodeNos,Diode,DiodeChannelNos\
                    ,OutRelay,OutRelayChannelNos,Sensor,SensorChannelNos,InRelay\
                    ,InRelayChannelNos,Resistance,ResistanceChannelNos,Capacitance,CapacitanceChannelNos\
                    ,LowResistance,LowResistanceChannelNos,mASignal,mASignalChannelNos,VSignal\
                    ,VSignalChannelNos,Insulation,InsulationChannelNo,OpticFiber,OpticFiberChannelNos\
                     from tblLocal_Settings \
                    where LocalSettings_Location="+str(LocalSettings_Location)
    my_database.execute(sql_statement)
    x = my_database.fetchall()
    print("test",x)
    if(len(x)==0):
        print('Record not found please create')
    else:
        return(x)

def UploadCable_Settings(Location_No):
    LocalSettings_Location=Location_No;
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database=conn.cursor()
    sql_statement = "SELECT count(LocalSettings_Location) from tblLocal_Settings where LocalSettings_Location="+str(LocalSettings_Location)
    my_database = conn.execute(sql_statement)
    n = my_database.fetchone()[0]
    print("n",n)
    if(n == 0):
        my_database.execute('insert into tblLocal_Settings(LocalSettings_Location,ReleaseTime,QMarkTime,BuzzerStatus,ExtraPointTest,CutterStatus,OpenPointTime,ShortPointTime,InterChangeTime,ExtraPointTime,LablePrint,LableNos,BarCodeMatch,BarcodeNos,Diode,DiodeChannelNos,OutRelay,OutRelayChannelNos,Sensor,SensorChannelNos,InRelay,InRelayChannelNos,Resistance,ResistanceChannelNos,Capacitance,CapacitanceChannelNos,LowResistance,LowResistanceChannelNos,mASignal,mASignalChannelNos,VSignal,VSignalChannelNos,Insulation,InsulationChannelNo,OpticFiber,OpticFiberChannelNos) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(LocalSettings_Location,GV.Local_Settings_File[0][0],GV.Local_Settings_File[0][1],GV.Local_Settings_File[0][2],GV.Local_Settings_File[0][3],GV.Local_Settings_File[0][4],GV.Local_Settings_File[0][5],GV.Local_Settings_File[0][6],GV.Local_Settings_File[0][7],GV.Local_Settings_File[0][8],GV.Local_Settings_File[0][9],GV.Local_Settings_File[0][10],GV.Local_Settings_File[0][11],GV.Local_Settings_File[0][12],GV.Local_Settings_File[0][13],GV.Local_Settings_File[0][14],GV.Local_Settings_File[0][15],GV.Local_Settings_File[0][16],GV.Local_Settings_File[0][17],GV.Local_Settings_File[0][18],GV.Local_Settings_File[0][19],GV.Local_Settings_File[0][20],GV.Local_Settings_File[0][21],GV.Local_Settings_File[0][22],GV.Local_Settings_File[0][23],GV.Local_Settings_File[0][24],GV.Local_Settings_File[0][25],GV.Local_Settings_File[0][26],GV.Local_Settings_File[0][27],GV.Local_Settings_File[0][28],GV.Local_Settings_File[0][29],GV.Local_Settings_File[0][30],GV.Local_Settings_File[0][31],GV.Local_Settings_File[0][32],GV.Local_Settings_File[0][33],GV.Local_Settings_File[0][34]))
    else:    
        my_database.execute('update tblLocal_Settings set ReleaseTime = ?,QMarkTime = ?,BuzzerStatus = ?,ExtraPointTest = ?,CutterStatus = ?,OpenPointTime = ?,ShortPointTime = ?,InterChangeTime = ?,ExtraPointTime = ?,LablePrint = ?,LableNos = ?,BarCodeMatch = ?,BarcodeNos = ?,Diode = ?,DiodeChannelNos = ?,OutRelay = ?,OutRelayChannelNos = ?,Sensor = ?,SensorChannelNos = ?,InRelay = ?,InRelayChannelNos = ?,Resistance = ?,ResistanceChannelNos = ?,Capacitance = ?,CapacitanceChannelNos = ?,LowResistance = ?,LowResistanceChannelNos = ?,mASignal = ?,mASignalChannelNos = ?,VSignal = ?,VSignalChannelNos = ?,Insulation = ?,InsulationChannelNo = ?,OpticFiber = ?,OpticFiberChannelNos = ? where LocalSettings_Location = ?',(GV.Local_Settings_File[0][0],GV.Local_Settings_File[0][1],GV.Local_Settings_File[0][2],GV.Local_Settings_File[0][3],GV.Local_Settings_File[0][4],GV.Local_Settings_File[0][5],GV.Local_Settings_File[0][6],GV.Local_Settings_File[0][7],GV.Local_Settings_File[0][8],GV.Local_Settings_File[0][9],GV.Local_Settings_File[0][10],GV.Local_Settings_File[0][11],GV.Local_Settings_File[0][12],GV.Local_Settings_File[0][13],GV.Local_Settings_File[0][14],GV.Local_Settings_File[0][15],GV.Local_Settings_File[0][16],GV.Local_Settings_File[0][17],GV.Local_Settings_File[0][18],GV.Local_Settings_File[0][19],GV.Local_Settings_File[0][20],GV.Local_Settings_File[0][21],GV.Local_Settings_File[0][22],GV.Local_Settings_File[0][23],GV.Local_Settings_File[0][24],GV.Local_Settings_File[0][25],GV.Local_Settings_File[0][26],GV.Local_Settings_File[0][27],GV.Local_Settings_File[0][28],GV.Local_Settings_File[0][29],GV.Local_Settings_File[0][30],GV.Local_Settings_File[0][31],GV.Local_Settings_File[0][32],GV.Local_Settings_File[0][33],GV.Local_Settings_File[0][34],LocalSettings_Location))
    conn.commit()
# =============================================================================
 
# =============================================================================  
def UploadQC_Data(Location_No,Local_Lable_Data,Local_Barcode1_Data,Local_Barcode2_Data): 
    QCData_Location=Location_No
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database=conn.cursor()
    sql_statement = "SELECT count(QCData_Location) from tblQC_Data where QCData_Location="+str(QCData_Location)
    my_database = conn.execute(sql_statement)
    n = my_database.fetchone()[0]
    if(n == 0):
        my_database.execute('insert into tblQC_Data(QCData_Location,LableData,BarCode1Data,BarCode2Data) values(?,?,?,?)',(QCData_Location,Local_Lable_Data,Local_Barcode1_Data,Local_Barcode2_Data))
    else:    
        my_database.execute('update tblQC_Data set LableData = ?, BarCode1Data = ?,BarCode2Data = ? where QCData_Location = ?',(Local_Lable_Data,Local_Barcode1_Data,Local_Barcode2_Data,QCData_Location))
    conn.commit()

def DownloadQC_Data(Location_No):
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    QCData_Location=Location_No
    my_database=conn.cursor()  
 
    sql_statement = "SELECT LableData,BarCode1Data,BarCode2Data from tblQC_Data where QCData_Location="+str(QCData_Location)
    my_database.execute(sql_statement)
    hlist = my_database.fetchall()
    #print(hlist[0][0])
    #print(hlist)
    if(len(hlist)==0):
        print('Record not found please create')
    else:
        return(hlist)
        
# =============================================================================
# 
# =============================================================================
def DownloadSystemInfo(Location_No):
    #print('Location_No',Location_No)
    LocalGrp1_Location=Location_No
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database = conn.cursor()
    sql_statement = "SELECT Key,Value from tblSystem_info \
                    where Id ="+str(LocalGrp1_Location)
    my_database.execute(sql_statement)
    output = my_database.fetchall()
    #print('output',output)
    return(output)

def UploadSystemInfo(val,loc):
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database = conn.cursor()
    my_database.execute('update tblSystem_info set Value = ? where Id =?',(val,loc))
    conn.commit()

# =============================================================================
# 
# =============================================================================
def UploadLog_Data(Location_No,Part_Name,Event,Description):
    conn = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database =conn.cursor()
    Location = Location_No
    PartName = Part_Name
    Description=Description
    my_database.execute('insert into tblLog_Data(Date_Time,LocationNo,PartName,Event,Description) values(?,?,?,?,?)',(datetime.now(),Location,PartName,Event,Description))
    conn.commit() 

def DownloadLog(FromDate,ToDate):
    conn = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database = conn.cursor()
    sql_statement = "SELECT Date_Time,LocationNo,PartName,Event,Description from tblLog_Data \
                    where Date_Time between '"+ FromDate +"' AND '"+ ToDate +"'"
    my_database.execute(sql_statement)
    output = my_database.fetchall()
    cnt=1
    file_name='/home/pi/Desktop/ExportData.xls'
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    worksheet.write(0,0,'Date_Time')
    worksheet.write(0,1,'LocationNo')
    worksheet.write(0,2,'PartName')
    worksheet.write(0,3,'Event')
    worksheet.write(0,4,'Description')
    for myOutput in output:
        worksheet.write(cnt,0,myOutput[0])
        worksheet.write(cnt,1,myOutput[1])
        worksheet.write(cnt,2,myOutput[2])
        worksheet.write(cnt,3,myOutput[3])
        worksheet.write(cnt,4,myOutput[4])
        cnt +=1
    workbook.close()
    conn.close()
# =============================================================================
# 
# =============================================================================

def Sqdb_to_Ram(state):
    if(state==1):
        x=DownLoadCableId_boot()
        GV.Location_No=x[0][0]
        GV.Part_Name=x[0][1]
    elif(state==2):
        x=DownLoadCableId_change(GV.Location_No)
        print('x',x)
        GV.Part_Name=x[0][0]
    print("Location_No PartName...",GV.Location_No)
    
    GV.Local_Cable_Info=DownloadCable_Info(GV.Location_No)
##    print("test",GV.Local_Cable_Info)
    GV.Pass_Count=GV.Local_Cable_Info[0][0]
    GV.Fail_Count=GV.Local_Cable_Info[0][1]
    GV.Stage1_status=GV.Local_Cable_Info[0][2]
    GV.Stage1_Points_No=GV.Local_Cable_Info[0][3]
    GV.Stage2_status=GV.Local_Cable_Info[0][4]
    GV.Stage2_Points_No=GV.Local_Cable_Info[0][5]
##    print("data",global_test_var.Local_Cable_Info)
    print("Pass_Count",GV.Pass_Count)
    print("Fail_Count",GV.Fail_Count)
    print("Stage1_status",GV.Stage1_status)
    print("Stage1_Points_No",GV.Stage1_Points_No)
    print("Stage2_status",GV.Stage2_status)
    print("Stage2_Points_No",GV.Stage2_Points_No)
    print("GV.LeakageFixNo",GV.LeakageFixNo)
    
    GV.Local_Settings_File=DownloadCable_Settings(GV.Location_No)
    print("test",GV.Local_Settings_File)
    GV.Release_Time=GV.Local_Settings_File[0][0]
    GV.Q_Mark_Time=GV.Local_Settings_File[0][1]
    GV.Buzzer_Status=GV.Local_Settings_File[0][2]
    GV.Extra_Point_Test=GV.Local_Settings_File[0][3]
    GV.Cutter_status=GV.Local_Settings_File[0][4]
    GV.Open_point_Timeout=GV.Local_Settings_File[0][5]
    GV.Short_point_Timeout=GV.Local_Settings_File[0][6]
    GV.Interchange_point_Timeout=GV.Local_Settings_File[0][7]
    GV.Extra_point_Timeout=GV.Local_Settings_File[0][8]
    GV.LabelPrint=GV.Local_Settings_File[0][9]
    GV.LabelNos=GV.Local_Settings_File[0][10]
    GV.Barcode_Match=GV.Local_Settings_File[0][11]
    GV.No_Of_Barcodes=GV.Local_Settings_File[0][12]
     #print("Local_Settings_File",GV.Local_Settings_File)
    print("Release_Time",GV.Release_Time)
    print("Q_Mark_Time",GV.Q_Mark_Time)
    print("Buzzer_Status",GV.Buzzer_Status)
    print("Extra_Point_Test",GV.Extra_Point_Test)
    print("Cutter_status",GV.Cutter_status)
    print("Open_point_Timeout",GV.Open_point_Timeout)
    print("Short_point_Timeout",GV.Short_point_Timeout)
    print("Interchange_point_Timeout",GV.Interchange_point_Timeout)
    print("Extra_point_Timeout",GV.Extra_point_Timeout)
    print("LabelPrint",GV.LabelPrint)
    print("LabelNos",GV.LabelNos)
    print("Barcode_Match",GV.Barcode_Match)
    print("No_Of_Barcodes",GV.No_Of_Barcodes)

    
    GV.circuits=[]
    DownloadHarnessData(GV.Location_No)
    print("Circuits",GV.circuits)
    
    GV.Leakage_Testing=Download_Help()
    print("GV.Leakage_Testing",GV.Leakage_Testing)
    
    GV.QC_data_list=DownloadQC_Data(GV.Location_No)
    GV.Local_Label_Data=GV.QC_data_list[0][0]
    GV.Local_Barcode1_Data=GV.QC_data_list[0][1]
    GV.Local_Barcode2_Data=GV.QC_data_list[0][2]
##    print("QC",GV.QC_data_list)
    print("Local_Label_Data",GV.Local_Label_Data)
    print("Local_Barcode1_Data",GV.Local_Barcode1_Data)
    print("Local_Barcode2_Data",GV.Local_Barcode2_Data)

    GV.Local_Group2_File = DownloadLocal_Grp2(GV.Location_No)
    print("Group2_File..",GV.Local_Group2_File)
    
    GV.System_Info=DownloadSystemInfo(1)
    GV.admin_user=GV.System_Info[0]
    print("admin_user",GV.admin_user)

    GV.System_Info=DownloadSystemInfo(2)
    GV.kt_user=GV.System_Info[0]
    print("kt_user",GV.kt_user)

    GV.System_Info=DownloadSystemInfo(3)
    GV.OneD_Barcode_Sample=GV.System_Info[0][1]
    print("GV.OneD_Barcode_Sample",GV.OneD_Barcode_Sample)

    GV.System_Info=DownloadSystemInfo(4)
    GV.TwoD_Barcode_Sample=GV.System_Info[0][1]
    print("TwoD_Barcode_Sample",GV.TwoD_Barcode_Sample)

    GV.System_Info=DownloadSystemInfo(5)
    GV.Barcode_Clear_Flag=GV.System_Info[0][1]
    print("Barcode_Clear_Flag",GV.Barcode_Clear_Flag)

    GV.Config_Info=DownloadConfiguration(1)
    print("Config_Info",GV.Config_Info)
    GV.Model=GV.Config_Info[0][0]
    GV.HWVersion=GV.Config_Info[0][1]
    GV.SWVersion=GV.Config_Info[0][2]
    GV.LeakageFixNo=GV.Config_Info[0][3]
    GV.LeakageChannel=GV.Config_Info[0][4]
    print("Model",GV.Model)
    print("HWVersion",GV.HWVersion)
    print("SWVersion",GV.SWVersion)
    print("LeakageFixNo",GV.LeakageFixNo)
    print("LeakageChannel",GV.LeakageChannel)
# =============================================================================
# 
# =============================================================================
def DownloadCable_Info1():##download (CableInfo_Location,PassCount,FailCount,Stage1,Stage1Points,Stage2,Stage2Points) in ram
    conn  = sqlite3.connect('/home/pi/Desktop/AWHT/code/tester_files/AWHTestDB.db')
    my_database=conn.cursor()
    try:
        sql_statement = "SELECT PassCount,FailCount,Stage1,Stage1Points,Stage2,Stage2Points from tblCable_Info where CableInfo_Location="+str(CableInfo_Location)
        my_database = conn.execute(sql_statement)
        x = my_database.fetchall()
        #print("Local_Cable_Info",x)
        return(x)
    except :
        print('Record not found please create')
if __name__ == '__main__':
##    DownloadLog('2020-01-04 08:52:57.439423','2020-01-04 09:27:38.146780')
##    UploadCable_Settings()
            
##    UploadSystemInfo('KT1234',2)
##    GV.Location_No=1
    Sqdb_to_Ram(1)
##    Harnesdata_excel(1)
##    print(x)
##    Upload_Help(1)
    #uploadConfiguration(12)
    #sql_connection()
##    DownloadCableId_All()
##    DownloadCable_Info_all()
##    for i in range(101,129):
##    UpLoadCableId(17,'part23')
    
##   DownLoadCableId(1)
##    global_test_var.circuits = [[1,2,3,4], [21,64], [32,35,40], [5,50,54]]
##    UploadHarnessData(6)
##    global_test_var.circuits=[]
##    DownloadHarnessData(6)
##    DownLoadCableId_boot()
##    DownLoadCableId_change(1)
   # UpLoadCableId(1,"cableid1234")
##    Local_Cable_Info = [(1,1,1,888,1,545)]
    #Local_Cable_Info=()
##    for i in range(30,128):
##    UploadCable_Info(128,Local_Cable_Info)
##    x=DownloadCable_Info(1)
##    print(x)
##    for i in range(17,129):
##    UploadQC_Data(100,'testdata2222','testbarcode111','testbarcode222')
##    DownloadQC_Data(5)
##    Local_Settings_File=()
##    DownloadCable_Settings(8)
##    GV.Local_Settings_File = [(11,2,1,0,0,60,30,60,60,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)]
##    for i in range(18,129):
##        UploadCable_Settings(i)
##    DownloadLocal_Grp2(1)
##    DownloadGlobal_Grp2()
##    DownloadLocal_Grp1(1)
##    GV.System_Info=DownloadSystemInfo(2)
##    print(GV.System_Info)
##    GV.Barcode_Clear_Flag=GV.System_Info[0][1]
##    print("Barcode_Clear_Flag",GV.Barcode_Clear_Flag)
##    GV.Config_Info=DownloadConfiguration(1)
##    print("Config_Info",GV.Config_Info)
##    UploadLog_Data(1,'TestPart','TestEvent','TestDescription')
##    n_tuple_Data = [(1,5),(3,8,12),(9,10),(16,18,24)]
##    UploadLocal_Grp2(10,n_tuple_Data)
##    DownloadGLobal_Cable_Settings()
    DownloadGlobal_Grp1()
    ##sql_Close()



        
    
    
