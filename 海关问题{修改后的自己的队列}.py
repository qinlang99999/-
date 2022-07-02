import random
##队列类
#1 3 6 8 3 100
class Queue:
    def __init__(self, limit=100):
        self.data = [None] * limit
        self.head =-1
        self.tail =-1

    def enqueue(self, val):
        if self.head==-1:
            self.head=0
        if self.tail==len(self.data)-1:
            if self.data[0]==None:
                a=[None]*self.head
                b=self.data[self.head:]
                self.data=(b+a)
                self.tail-=self.head
                self.head=-1
            else:
                raise RuntimeError
        self.tail+=1
        self.data[self.tail]=val
        
        
    def dequeue(self):    
        if self.head==-1:
            self.head=0
        if self.data[self.head]==None:
            raise RuntimeError      
        a=self.data[self.head]
        self.data[self.head]=None
        self.head+=1
        if self.empty():
            self.head=self.tail=-1
        return a
    
    def resize(self, newsize):
        assert(len(self.data) < newsize)
        if self.head==-1:
            self.head=0
        a=[None]*newsize
        for i in range(self.tail-self.head+1):
            a[i]=self.data[i+self.head]
        self.data=a
        self.tail-=self.head
        self.head=-1
    
    def empty(self):
        a=self.head
        if a==-1:
            a=0
        return a==self.tail+1
    
    def __bool__(self):
        return not self.empty()
    
    def __str__(self):
        if not(self):
            return ''
        return ', '.join(str(x) for x in self)
    
    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        if self.head==-1:
            self.head=0
        a=self.head
        while a!=self.tail+1:
            yield self.data[a]
            a+=1

##车类
class Car:
    def __init__(self,cartime,carid):
        self.ID=carid##车辆ID
        self.Timein=cartime#车辆到达的时间


##海关类
class Customs:
    def __init__(self,WT_Min,WT_Max):
       self.State=0##海关状态
       self.Should_WT=0##（随机数）本海关的所需等待时间（out功能包含计时功能）
       self.CheckCar=None#所作用的对象：车类
       ##检查时间随机数上下限
       self.WT_Max=WT_Max
       self.WT_Min=WT_Min
       self.WT_team=Queue()
    
       
    ##弹出和倒计时
    def OutCustoms(self,Timeout):
        if self.State==0:
            return
        elif self.Should_WT!=1:
            self.Should_WT-=1
            return
        else:
            ##NumT=Timeout-self.CheckCar.Timein
            Car_BT=self.CheckCar
            self.CheckCar=None
            self.State=0
            self.Should_WT-=1
            return Car_BT
    

    ##进入检查点和赋予倒计时，记录状态           
    def InCustoms(self,CheckCar):
        self.Should_WT=random.randint(self.WT_Min,self.WT_Max)
        self.CheckCar=CheckCar
        self.State=1
        




print("以下所有数据的单位均为分钟，只能输入整数")
ArriaveTime_Min=int(input("请输入车辆进入间隔时间下限："))
ArriaveTime_Max=int(input("请输入车辆进入间隔时间上限："))
CheckTime_Min=int(input("请输入检查时间下限："))
CheckTime_Max=int(input("请输入检查时间上限："))
KLis_NB=int(input("请输入检查口个数："))
WaitTime=int(input("请输入需要模拟的时长："))
###     输入系统

KLis=[]
for i in range(KLis_NB):
    KLis.append(Customs(CheckTime_Min,CheckTime_Max))
##按照需求制造指定量的海关口，存储在一个列表里


IDNum=1#记录车的编号
SumTime=0#车辆随即来临时间匹配的计时
Totlenum=0#记录一共进入队列的车辆
AC_num=0#记录已经过境车辆
TeamWait_average=[]##排队时间大数据
AcrossWait_average=[]##过境时间大数据
Text_Show=[]#为文件存储文本
Sys_A=0#模式判断器，判断是否有事件发生

ArriaveTime_Standard=random.randint(ArriaveTime_Min,ArriaveTime_Max)
#初始随机入队间隔时间




for Ti in range(WaitTime):
    Sys_A=0
    SumTime+=1
##  计时
    if SumTime==ArriaveTime_Standard:
##      如果时间到达，则会来下一辆车
        ##标记进入队列的时间
        Totlenum+=1
        if Sys_A==0:
            Sys_A=1
            Text_Show.append("".join(["第",str(Ti),"分钟时","\n"]))
        Text_Show.append("".join(["ID为：",str(IDNum),"开始排队."]))
        
##      检查队伍最短的那一队进入车辆
        Cu_T_N=KLis[0].WT_team.tail-KLis[0].WT_team.head+1
        Cu_T_ID=0
        Cu_WT=ArriaveTime_Max
        for Cu_T in range(len(KLis)):
            if KLis[Cu_T].State==0:##第一优先（无车检查）
                Cu_T_N=0
                Cu_T_ID=Cu_T
                break
            elif KLis[Cu_T].WT_team.tail==KLis[Cu_T].WT_team.head==-1 and Cu_WT>KLis[Cu_T].Should_WT:#第二优先，最短排队（前后是-1等于没有车）
                Cu_WT=KLis[Cu_T].Should_WT
                Cu_T_N=0
                Cu_T_ID=Cu_T
            elif KLis[Cu_T].WT_team.tail-KLis[Cu_T].WT_team.head+1<Cu_T_N:
                Cu_T_N=KLis[Cu_T].WT_team.tail-KLis[Cu_T].WT_team.head+1
                Cu_T_ID=Cu_T
        KLis[Cu_T_ID].WT_team.enqueue(Car(Ti,IDNum))
        
        IDNum+=1
##      入队后随机重置车辆到达间隔的时间模拟随机性
        ArriaveTime_Standard=random.randint(ArriaveTime_Min,ArriaveTime_Max)
        Text_Show.append("".join(["他进入的海关号：#",str(Cu_T_ID+1),"\n"]))
        SumTime=0

        
        
    
##      关于检查点检查的计时和弹出
    kkkkk=0
    for Cu in KLis:
        kkkkk+=1
        if Cu.State==1:     
            Tes=Cu.OutCustoms(Ti)
            if not Tes:
                continue
            else:
                if Sys_A==0:
                    Sys_A=1
                    Text_Show.append("".join(["第",str(Ti),"分钟时","\n"]))
                AcrossWait_average.append(Ti-Tes.Timein)
                AC_num+=1
                Text_Show.append("".join(["ID为：",str(Tes.ID),'过境',"\n"])) 
##      关于检查点的进入        
        if not Cu.WT_team.empty() and Cu.State==0:
                if Sys_A==0:
                    Sys_A=1
                    Text_Show.append("".join(["第",str(Ti),"分钟时","\n"]))
                Car_SP=Cu.WT_team.dequeue()
                Cu.InCustoms(Car_SP)
                Text_Show.append("".join(["ID为：",str(Car_SP.ID),'进入检查口:',str(kkkkk),"\n"]))
                TeamWait_average.append(Ti-Car_SP.Timein)
                Text_Show.append("".join(["(本ID预计过境所需时间：",str(Cu.Should_WT),")\n"]))
    
    if Sys_A==1:                    
        Text_Show.append("\n\n")
        
Simplify_Sys=input("选择输出模式\nA：只输出分析结果\nB：详细附加具体过程\n请选择：")  
assert Simplify_Sys=="A" or Simplify_Sys=="B","请输入A或B（大写）"
if Simplify_Sys=="A":
    Text_Show=[]
      
Text_Show.append("".join(["车辆平均等待时间为",str(sum(TeamWait_average)/len(TeamWait_average)),"分钟\n"]))
Text_Show.append("".join(["车辆平均过境时间为",str(sum(AcrossWait_average)/len(AcrossWait_average)),"分钟\n"]))
Text_Show.append("".join(["进入队列车辆共计有",str(Totlenum),"辆","\n"]))
Text_Show.append("".join(["已经过境车辆共计有",str(AC_num),"辆","\n"]))

kkkkk=0
for Cu in KLis:
    kkkkk+=1
    if Cu.WT_team.head!=Cu.WT_team.tail:
        Text_Show.append("".join(["还在海关#",str(kkkkk),"队伍中的车辆的编号分别是：","\n"]))
        for i in range(Cu.WT_team.head,Cu.WT_team.tail+1):
            Text_Show.append("\t#")
            Text_Show.append(str(Cu.WT_team.data[i].ID))
            Text_Show.append("\t")
    else:
        Text_Show.append("".join(["没有车辆在海关#",str(kkkkk),"队列中\n"]))
    Text_Show.append("\n\n")
PD=0
for i in range(len(KLis)):
    if KLis[i].State==1:
        if PD==0:
            Text_Show.append("海关中滞留的车辆:\n")
            PD=1
        Text_Show.append("\t#")
        Text_Show.append(str(KLis[i].CheckCar.ID))
        Text_Show.append("滞留在海关：")
        Text_Show.append(str(i+1))
        Text_Show.append("\n")
        
if PD==0:
    Text_Show.append("没有车辆滞留在海关\n")
with open(r"C:\Users\Administrator\Desktop\Customs_analysis_2.txt","w") as fp:
    for i in Text_Show:
        fp.write(i)
