import random
##队列类
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
        



#           输入模块
print("以下所有数据的单位均为分钟，请输入整数")
ArriaveTime_Min=int(input("请输入车辆进入间隔时间下限："))
ArriaveTime_Max=int(input("请输入车辆进入间隔时间上限："))
CheckTime_Min=int(input("请输入检查时间下限："))
CheckTime_Max=int(input("请输入检查时间上限："))
KLis_NB=int(input("请输入检查口个数："))
WaitTime=int(input("请输入需要模拟的时长："))

KLis=[]
for i in range(KLis_NB):
    KLis.append(Customs(CheckTime_Min,CheckTime_Max))
##按照需求制造指定量的海关口，存储在一个列表里


IDNum=1#车辆ID
SumTime=0#计时系统：车辆随机数
Totlenum=0#计数
TeamWait_average=[]##排队时间大数据
AcrossWait_average=[]##过境时间大数据
Text_Show=[]#显示文本
AcrossTeam=Queue()#等待队列
Sys_A=0#判断有无事件产生

ArriaveTime_Standard=random.randint(ArriaveTime_Min,ArriaveTime_Max)






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
        Text_Show.append("".join(["ID为：",str(IDNum),"进入队列","\n"]))
        AcrossTeam.enqueue(Car(Ti,IDNum))
        IDNum+=1
##      入队后随机重置车辆到达间隔的时间模拟随机性
        ArriaveTime_Standard=random.randint(ArriaveTime_Min,ArriaveTime_Max)
        
        SumTime=0

    for Cu in KLis:
##      关于检查点检查的计时和弹出  
        if Cu.State==1:     
            Tes=Cu.OutCustoms(Ti)
            if not Tes:
                continue
            else:
                if Sys_A==0:
                    Sys_A=1
                    Text_Show.append("".join(["第",str(Ti),"分钟时","\n"]))
                AcrossWait_average.append(Ti-Tes.Timein)
                Text_Show.append("".join(["ID为：",str(Tes.ID),'过境',"\n"]))
    
    if not AcrossTeam.empty():
##      关于检查点的进入  
        KKKKK=0
        for Cu in KLis:        
            KKKKK+=1
            if Cu.State==0:
                if Sys_A==0:
                    Sys_A=1
                    Text_Show.append("".join(["第",str(Ti),"分钟时","\n"]))
                Car_SP=AcrossTeam.dequeue()
                Text_Show.append("".join(["ID为：",str(Car_SP.ID),'进入检查口:',str(KKKKK),"\n"]))
                TeamWait_average.append(Ti-Car_SP.Timein)
                Cu.InCustoms(Car_SP)
                Text_Show.append("".join(["（本ID预计过境所需时间：",str(Cu.Should_WT),"）\n"]))
                break          
    
    if Sys_A==1:
        Text_Show.append("\n\n")

#选择需要显示的信息
Simplify_Sys=input("选择输出模式\nA：只输出分析结果\nB：详细附加具体过程\n请选择：")  
assert Simplify_Sys=="A" or Simplify_Sys=="B","请输入A或B（大写）"
if Simplify_Sys=="A":
    Text_Show=[]

###            分析模块
Text_Show.append("".join(["车辆平均等待时间为",str(sum(TeamWait_average)/len(TeamWait_average)),"分钟\n"]))
Text_Show.append("".join(["车辆平均过境时间为",str(sum(AcrossWait_average)/len(AcrossWait_average)),"分钟\n"]))
Text_Show.append("".join(["进入队列车辆共计有",str(Totlenum),"辆","\n"]))


if AcrossTeam.head!=AcrossTeam.tail:
    Text_Show.append("".join(["还在队伍中的车辆的编号分别是：","\n"]))
    for i in range(AcrossTeam.head,AcrossTeam.tail+1):
        Text_Show.append("\t#")
        Text_Show.append(str(AcrossTeam.data[i].ID))
        Text_Show.append("\t")
    Text_Show.append("\n\n")
else:
    Text_Show.append("没有车辆在队列中\n")
PD=0
for i in range(len(KLis)):
    if KLis[i].State==1:
        if PD==0:
            Text_Show.append("海关中滞留的车辆:\n")
            PD=1
        Text_Show.append("\t#")
        Text_Show.append(str(KLis[i].CheckCar.ID))
        Text_Show.append("滞留在海关：#")
        Text_Show.append(str(i+1))
        Text_Show.append("\n")
        
if PD==0:
    Text_Show.append("没有车辆滞留在海关\n")
    
    
    
#     在文件中存储
with open(r"C:\Users\Administrator\Desktop\Customs_analysis_1.txt","w") as fp:
    for i in Text_Show:
        fp.write(i)
