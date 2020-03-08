#-*- coding: ms949 -*-
import random
import queue
class Node():
    
    def __init__(self,id):
        self.id=id
        self.path=[
            [(self,0,0)],
            [],
            [],
            [],
            [],
            [],
            []
            ]
  #type
  #0-I     1-L     2-J     3-T    4-Z    5-N    6-O  

class Path():
    def __init__(self,parent,dest,tetrisqueue,tetrimino,ishold,hold,action):
        self.parent=parent;
        self.dest=dest;
        self.tetrisqueue=tetrisqueue;
        self.tetrimino=tetrimino;
        self.ishold=ishold;
        self.hold=hold;
        self.action=action;


case4_0=Node(0)
case4_1=Node(1)
case4_2=Node(2)
case4_3=Node(3)
case4_4=Node(4)
case4_5=Node(5)
case4_6=Node(6)
case4_7=Node(7)
case4_8=Node(8)
case4_9=Node(9)
case4_10=Node(10)
case4_11=Node(11)
case4_12=Node(12)
case4_13=Node(13)
case4_14=Node(14)
case4_15=Node(15)
case4_16=Node(16)
case4_17=Node(17)
case4_18=Node(18)
case4_19=Node(19)
case4_20=Node(20)
case4_21=Node(21)
case4_22=Node(22)
case4_23=Node(23)
case4_24=Node(24)
case4_25=Node(25)
case4_26=Node(26)
  #0-I     1-L(orange)     2-J(blue)     3-T    4-Z(red)    5-N(green)    6-O  
  
  #(case,rotation,move right)
case4_0.path[0].append((case4_14,1,3))
case4_0.path[2].append((case4_1,2,1))
case4_0.path[1].append((case4_3,3,3))
case4_0.path[3].append((case4_9,3,3))
case4_0.path[5].append((case4_7,1,2))

case4_1.path[0].append((case4_15,1,0))
case4_1.path[1].append((case4_0,2,0))
case4_1.path[2].append((case4_2,1,0))
case4_1.path[3].append((case4_8,1,0))
case4_1.path[4].append((case4_6,1,0))


# case4_2.path[3].append((case4_0))
case4_2.path[3].append((case4_18,3,3))
# case4_2.path[4].append((case4_25))
case4_2.path[4].append((case4_22,1,2))
# case4_2.path[5].append((case4_0))
# case4_2.path[1].append((case4_17))
case4_2.path[6].append((case4_16,0,2))

# case4_3.path[2].append((case4_16))
case4_3.path[6].append((case4_17,0,0))
# case4_3.path[5].append((case4_26))
case4_3.path[5].append((case4_23,1,0))
# case4_3.path[4].append((case4_1))
# case4_3.path[4].append((case4_24))
case4_3.path[3].append((case4_19,1,0))
# case4_3.path[3].append((case4_1))

case4_4.path[6].append((case4_1,0,2))
case4_4.path[3].append((case4_21,3,3))
case4_4.path[4].append((case4_13,1,2))

case4_5.path[6].append((case4_0,0,0))
case4_5.path[3].append((case4_20,1,0))
case4_5.path[5].append((case4_12,1,0))

case4_6.path[6].append((case4_1,0,2))
case4_6.path[2].append((case4_21,3,3))

case4_7.path[6].append((case4_0,0,0))
case4_7.path[1].append((case4_20,1,0))

case4_8.path[4].append((case4_0,0,1))
case4_8.path[3].append((case4_0,2,1))
case4_8.path[6].append((case4_16,0,2))
case4_8.path[1].append((case4_11,0,1))
case4_8.path[2].append((case4_6,0,1))
case4_8.path[2].append((case4_17,2,1))
case4_8.path[2].append((case4_18,3,2))

case4_9.path[3].append((case4_1,2,0))
case4_9.path[5].append((case4_1,0,0))
case4_9.path[2].append((case4_10,0,0))
case4_9.path[1].append((case4_7,0,0))
case4_9.path[1].append((case4_19,1,0))
case4_9.path[1].append((case4_16,2,0))
case4_9.path[6].append((case4_17,0,0))

case4_10.path[1].append((case4_9,0,1))
case4_10.path[1].append((case4_1,2,1))
case4_10.path[3].append((case4_7,0,1))

case4_11.path[2].append((case4_8,0,0))
case4_11.path[2].append((case4_0,2,0))
case4_11.path[3].append((case4_6,0,0))

case4_12.path[1].append((case4_13,0,1))
case4_12.path[2].append((case4_1,2,1))

case4_13.path[1].append((case4_0,2,0))
case4_13.path[2].append((case4_12,0,0))
    
case4_14.path[1].append((case4_18,2,0))
case4_14.path[1].append((case4_9,0,0))
case4_14.path[2].append((case4_18,0,0))
case4_14.path[2].append((case4_9,2,0))
case4_14.path[3].append((case4_21,0,0))

case4_15.path[1].append((case4_19,0,1))
case4_15.path[1].append((case4_8,2,1))
case4_15.path[2].append((case4_19,2,1))
case4_15.path[2].append((case4_8,0,1))
case4_15.path[3].append((case4_20,0,1))

case4_16.path[5].append((case4_8,1,0))
case4_16.path[3].append((case4_6,3,0))
case4_16.path[3].append((case4_0,2,0))
case4_16.path[1].append((case4_1,2,1))
case4_16.path[1].append((case4_4,3,0))

case4_17.path[4].append((case4_9,1,2))
case4_17.path[3].append((case4_7,1,2))
case4_17.path[3].append((case4_1,2,1))
case4_17.path[2].append((case4_0,2,0))
case4_17.path[2].append((case4_5,1,2))

case4_18.path[2].append((case4_19,0,0))
case4_18.path[2].append((case4_16,2,0))
case4_18.path[6].append((case4_1,0,1))
case4_18.path[4].append((case4_17,0,0))
case4_18.path[3].append((case4_17,2,0))
# case4_18.path[3].append((case4_24))

case4_19.path[1].append((case4_18,0,1))
case4_19.path[1].append((case4_17,2,1))
# case4_19.path[2].append((case4_24))
case4_19.path[6].append((case4_0,0,1))
case4_19.path[5].append((case4_16,0,1))
case4_19.path[3].append((case4_16,2,1))

case4_20.path[1].append((case4_22,0,1))
case4_20.path[1].append((case4_0,2,1))
case4_20.path[2].append((case4_16,2,1))

case4_21.path[2].append((case4_23,0,0))
case4_21.path[2].append((case4_1,2,0))
case4_21.path[1].append((case4_17,2,0))

case4_22.path[2].append((case4_20,0,0))
case4_22.path[3].append((case4_0,2,0))

case4_23.path[1].append((case4_21,0,1))
case4_23.path[3].append((case4_1,2,1))

# case4_24.path[5].append((case4_1,0,0))
# 
# case4_25.path[1].append((case4_1,0,0))
# 
# case4_26.path[2].append((case4_0,0,0))

tetrimino_name=["I(sky blue)","L(Orange)","J(blue)","T(purple)","Z(red)","N(green)","O(yellow)"]
def swapfrom(arr,index):
    arr2=arr.copy()
    
    temp=arr2[index]
    arr2[index]=arr2[index+1]
    arr2[index+1]=temp
    return arr2

def swapwith(arr,index,hold):
    arr2=arr.copy()
    
    arr2[index]=hold
    return arr2

#qu=[6, 2, 3, 5, 6, 3, 4, 4, 3, 0, 3, 6, 5, 5, 2, 5, 2, 3, 5, 1]    
#qu=[5, 2, 3, 2, 1, 4, 0, 2, 0, 2, 1, 0, 0, 1, 5, 3, 4, 2, 5, 2]
#qu=[0, 6, 0, 1, 5, 3, 1, 2, 1, 6, 6, 2, 6, 4, 2, 4, 1, 2, 3, 0]
def get_piece_queue():
    q=[]
    for i in range(50):
        q.append(random.randint(0,6))
    return q


def findpath(countstart,piece_queue):
    

    count=countstart
    hold=None
    currpos=case4_8
        
    pathlist=queue.Queue()
    currpath=(Path(None,currpos,piece_queue,None,False,0,(0,0)))
    pathlist.put(currpath)
    node_count=0
    case_count=0
    loop_count=0
    success=True
    while(count<25):
        
        
        currpath=pathlist.get()
        currpos=currpath.dest
        p_queue=currpath.tetrisqueue
        
        this_tetrimino=p_queue[count]
        hold=currpath.hold
#         if currpath.ishold:
#             if this_tetrimino!=next_tetrimino:
#                 for t in currpos.path[next_tetrimino]:
#                     pathlist.put(Path(currpath,t,swapfrom(p_queue,count),next_tetrimino,False))
#                     case_count+=1
#                 for t in currpos.path[this_tetrimino]:
#                         pathlist.put(Path(currpath,t,p_queue,this_tetrimino,True,count))
#                         case_count+=1
#             else:
#                 for t in currpos.path[this_tetrimino]:
#                         pathlist.put(Path(currpath,t,p_queue,this_tetrimino,False,count))
#                         case_count+=1
#         else:
#             if this_tetrimino!=next_tetrimino:
#                 for t in currpos.path[next_tetrimino]:
#                     pathlist.put(Path(currpath,t,swapfrom(p_queue,count),next_tetrimino,True))
#                     case_count+=1
#             for t in currpos.path[this_tetrimino]:
#                 pathlist.put(Path(currpath,t,p_queue,this_tetrimino,False,count))
#                 case_count+=1

        for t in currpos.path[this_tetrimino]:
            pathlist.put(Path(currpath,t[0],p_queue,this_tetrimino,False,hold,(t[1],t[2])))
            case_count+=1
            
        if this_tetrimino!=hold:
            for t in currpos.path[hold]:
                pathlist.put(Path(currpath,t[0],swapwith(p_queue,count,hold),hold,True,p_queue[count],(t[1],t[2])))
                case_count+=1
        
#         for t in currpos.path[this_tetrimino]:
#             if currpath.ishold:                   #이전 것과 hold 여부가 다를 경우에만 queue swap
#                 pathlist.put(Path(currpath,t,swapfrom(p_queue,count),next_tetrimino,False,count))
#             else:
#                 pathlist.put(Path(currpath,t,p_queue,this_tetrimino,False,count))
#             case_count+=1
#         if this_tetrimino!=next_tetrimino:
#             for t in currpos.path[next_tetrimino]:
#                 if currpath.ishold:
#                     pathlist.put(Path(currpath,t,p_queue,this_tetrimino,True,count))
#                 else:
#                     pathlist.put(Path(currpath,t,swapfrom(p_queue,count),next_tetrimino,True,count))
#                 case_count+=1
        
        loop_count+=1
        
        
        if count==0:
            count+=1
            node_count=case_count
            case_count=0
            loop_count=0
            
        elif loop_count>=node_count:
            count+=1
            node_count=case_count
            if case_count==0:
                print("combo impossible, combo stopped at ",count,"combo")
                return False
            case_count=0
            loop_count=0
            
    
        #currpos=pathlist.get()
        #piece_queue=queuelist.get()
    
    if success:
        predecessor=pathlist.get()
        pathList=[]
        while(predecessor.parent!=None):
            pathList.append((predecessor.dest,predecessor.tetrimino,predecessor.ishold,predecessor.action,predecessor.hold))
            predecessor=predecessor.parent
        
        #pathList=pathList.reverse()
        pathList.reverse()
#         for i in range(len(pathList)):
#             if pathList[i][2]:
#                 print((i+1),".  case:",pathList[i][0].id,", used tetrimino:",tetrimino_name[pathList[i][1]],", used hold")
#             else:
#                 print((i+1),".  case:",pathList[i][0].id,", used tetrimino:",tetrimino_name[pathList[i][1]])
#             print(pathList[i][4])
#             print(pathList[i][3])
        
        return pathList
    


    
    