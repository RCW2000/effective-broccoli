import math
import util
#partition via tree
class PartitionNode:
    def __init__(self,data:list,isRoot:bool,parent=None, grandparent=None, titi=None, sibling=None,root=None):
        self.data=data
        self.color='blue'
        self.isRoot=isRoot
        self.parent=parent
        self.grandparent=grandparent
        self.titi=titi
        self.sibling=sibling
        self.root=root

        if self.data==[]:
            self.values=[]
            self.uniqueClasses=[]
            self.card=len(self.values)
            self.classFrequencies = []
        else:
            self.values=[data[1] for data in self.data]
            self.uniqueClasses=list(set([data[2] for data in self.data]))
            self.card=len([data[1] for data in self.data])
            self.classFrequencies=[[data[2] for data in self.data].count(value) for value in self.uniqueClasses]
        
        if isRoot==False:
            self.isStopped=self.STOP()
            self.entropy=self.Entropy()
            self.infogain=None
        
        
        
    
    def splitNode(self,threshold,root):
        #partition
        left=PartitionNode([self.data[i] for i in range(len(self.data)) if self.data[i][1] < threshold ],False,self,self.parent,self.sibling,root=root)
        right=PartitionNode([self.data[i] for i in range(len(self.data)) if self.data[i][1] > threshold or self.data[i][1] == threshold],False,self,self.parent,self.sibling,left,root=root)
        left.sibling=right
        self.color='orange'
        left.color='blue'
        right.color='blue'
        return right,left
    
    def STOP(self)->bool:
        #stop condition
        if self.data!=[]:
            n=len(list(set(self.root.data[:][1])))
            if len(self.uniqueClasses)==1:
                self.color='purple'
                return True
            if min(self.classFrequencies)/max(self.classFrequencies) <0.5:
                if len(self.uniqueClasses) < math.floor(n/2) or len(self.uniqueClasses) == math.floor(n/2):
                    self.color='purple'
                    return True
            
            return False
    
    def Entropy(self):
        #calculate entropy
        sum=0
        for i in range(len(self.uniqueClasses)):
           sum=sum + (-1*(self.classFrequencies[i])*math.log2(self.classFrequencies[i]))
        return sum

class PartitionTree:
    def __init__(self,data:list):
        #print("hello")
        self.root=PartitionNode(data,True)
        #print(len(self.root.data))
        self.nodes=[]
        self.medfinPartitions=[]
        self.medPartitions=[]
        self.medfinPartitions,self.medPartitions=self.Partition(util.median)
        self.meanfinPartitions=[]
        self.meanPartitions=[]
        self.meanfinPartitions,self.meanPartitions=self.Partition(util.mean)
        self.gains=self.InfoGain()
        if  self.gains[0] >self.gains[1]:
            self.finPartitions=[self.medfinPartitions[i].data for i in range(len(self.medfinPartitions))]
            #print(len(self.medfinPartitions[0].data))
        else:
            self.finPartitions=[self.meanfinPartitions[i].data for i in range(len(self.meanfinPartitions))]
            #print(len(self.meanfinPartitions[0].data))
        print(len(self.finPartitions))


    def Partition(self,function):
        #dfs
        closed=set()
        fringe=[]
        fringe.insert(0,(self.root,self.nodes))
        while(True):
            #print('yo')
            if len(fringe)==0:
                return self.medfinPartitions,partitions
            node: PartitionNode
            node,partitions=fringe.pop(0)
            if node.color=='purple':
                node.infogain=(((node.card/node.parent.card)*node.entropy) + ((node.sibling.card/node.parent.card)*node.sibling.entropy))
                if function==util.median:
                    self.medfinPartitions.append(node)
                elif function==util.mean:
                     self.meanfinPartitions.append(node)
                continue
            elif node.parent is not None and node.grandparent is not None and node.card==node.parent.card:
                node.color='black'
                node.parent.color='purple'
                node.parent.infogain=(((node.parent.card/node.grandparent.card)*node.parent.entropy) + ((node.titi.card/node.grandparent.card)*node.titi.entropy))
                if function==util.median:
                    self.medfinPartitions.append(node.parent)
                elif function==util.mean:
                    self.meanfinPartitions.append(node.parent)
                continue
            elif node.card<1:
                continue
            if str(node) not in closed:
                closed.add(str(node))
                if node.color=='blue' and node.card>0:
                    for state in node.splitNode(function(node.values),self.root):
                        fringe.insert(0,(state,partitions+[node]))

    def InfoGain(self):
        medgain=0
        meangain=0
        for i in range(len(self.medfinPartitions)):
            if i-1>-1:
                if self.medfinPartitions[i].sibling==self.medfinPartitions[i-1]:
                    continue
            medgain=medgain+self.medfinPartitions[i].infogain
        for i in range(len(self.meanfinPartitions)):
            if i-1>-1:
                if self.meanfinPartitions[i].sibling==self.meanfinPartitions[i-1]:
                    continue
            meangain=meangain+self.meanfinPartitions[i].infogain
        return [medgain,meangain]

                
    