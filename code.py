import sys
from api import *
from time import sleep
import numpy as np
import math

#######    YOUR CODE FROM HERE #######################
grid =[]

class Node:
    def __init__(self,value,point):
        self.value = value  #0 for blocked,1 for unblocked
        self.point = point
        self.parent = None
        self.move=None
        self.H = 0
        self.G = 0
        
neigh=[[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]]

def isValid(pt):
    return pt[0]>=0 and pt[1]>=0 and pt[0]<200 and pt[1]<200

def neighbours(point):  #returns valid neighbours
    global grid,neigh
    x,y = point.point
    links=[]
    for i in range(len(neigh)):
        newX=x+neigh[i][0]
        newY=y+neigh[i][1]
        if not isValid((newX,newY)):
            continue
        links.append((i+1,grid[newX][newY]))
    return links
        
def diagonal(point,point2):
    return max(abs(point.point[0] - point2.point[0]),abs(point.point[1]-point2.point[1]))

def aStar(start, goal):
    #The open and closed sets
    openset = set()
    closedset = set()
    #Current point is the starting point
    current = start
    #Add the starting point to the open set
    openset.add(current)
    #While the open set is not empty
    while openset:
        #Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o:o.G + o.H)
        #Remove the item from the open set
        openset.remove(current)
        #Add it to the closed set
        closedset.add(current)
        #If it is the item we want, retrace the path and return it
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
                if(current.point==start.point):
                    path.append(current)
                    return path[::-1]
        #Loop through the node's children/siblings which are valid and not blocked
        for move,node in neighbours(current):
            #If it is already in the closed set, skip it
            if node in closedset:
                continue
            #if cell is blocked
            if node.value==0:
                continue
            #Otherwise if it is already in the open set
            if node in openset:
                #Check if we beat the G score
                if node.value==1:
                    new_g = current.G + 1 #onl
                if node.value==2:
                    new_g = current.G + 2 #on2
                if node.G > new_g:
                    #If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
                    node.move=move
            else:
                #If it isn't in the open set, calculate the G and H score for the node
                if node.value==1:
                    node.G = current.G + 1
                if node.value==2:
                    node.G = current.G + 2
                node.H = diagonal(node, goal)
                #Set the parent to our current item
                node.parent = current
                node.move=move
                #Add it to the set
                openset.add(node)
    #Throw an exception if there is no path
    raise ValueError('No Path Found')

'''
PS: You need not write codes for all levels. You must
at least complete the function corresponding to the level
you're attempting at the moment.
'''
    
def level1(botId):
    global grid
    moveType = 5
    botsPose = get_botPose_list()
    obstaclePose = get_obstacles_list()
    greenZone = get_greenZone_list()
    redZone = get_redZone_list()
    originalGreenZone = get_original_greenZone_list()
    for i in range(200):
        grid.append([])
        for j in range(200):
            grid[i].append(Node(1,(i,j)))
    for pt in obstaclePose:
        for i in range(pt[0][0],pt[2][0]+1):
            for j in range(pt[0][1],pt[2][1]+1):
                grid[i][j]=Node(0,(i,j))
    start=grid[botsPose[0][0]][botsPose[0][1]]
    goal=grid[greenZone[0][0][0]][greenZone[0][0][1]]
    path=aStar(start, goal)
    print(len(path))
    print("final pos:",greenZone[0][0])
    pos=get_botPose_list()
    print("initial pos:",pos[0])
    sleep(0.05)
    for i in range(1,len(path)):
        successful_move, mission_complete = send_command(botId,path[i].move)
        pos=get_botPose_list()
        if successful_move:
            print("YES")
        else:
            print("NO")
        if mission_complete:
            print("MISSION COMPLETE")
        pos=get_botPose_list()
        print(pos[0])

def level2(botId):
    global grid
    global z
    moveType = 5
    botsPose = get_botPose_list()
    obstaclePose = get_obstacles_list()
    greenZone = get_greenZone_list()
    redZone = get_redZone_list()
    originalGreenZone = get_original_greenZone_list()
    print(type(greenZone))
    for i in range(200):
        grid.append([])
        for j in range(200):
            grid[i].append(Node(1,(i,j)))
    for pt in obstaclePose:
        for i in range(pt[0][0],pt[2][0]+1):
            for j in range(pt[0][1],pt[2][1]+1):
                grid[i][j]=Node(0,(i,j))
    
    z=0
    a=0
    
    
    for i in range(len(greenZone)):
        min=1000
        
        for j in range(len(greenZone)):
            for a in range(0,4):
                distance = math.sqrt( ((botsPose[0][0]-greenZone[j][a][0])**2)+(botsPose[0][1]-greenZone[j][a][1])**2)
                if(min>distance):
                    min=distance
                    z=j
                    y=a
            print("targets left:")
            print(greenZone[j][0])
        botsPose = get_botPose_list()
        start=grid[botsPose[0][0]][botsPose[0][1]]
        goal=grid[greenZone[z][y][0]][greenZone[z][y][1]]
        path=aStar(start, goal)
                
        
    
            
        print(len(path))
        print("final pos:",greenZone[z][y])
        pos=get_botPose_list()
        print("initial pos:",pos[0])
        sleep(0.05)
        
        
        
        for k in range(1,len(path)):
            successful_move, mission_complete = send_command(0,path[k].move)
            pos=get_botPose_list()
            if successful_move:
                print("YES")
            else:
                print("NO")
            if mission_complete:
                print("MISSION COMPLETE")
            pos=get_botPose_list()
            print(pos[0])
        greenZone = get_greenZone_list()
                

            


def level3(botId):
    global grid
    global z
    global y
    moveType = 5
    botsPose = get_botPose_list()
    obstaclePose = get_obstacles_list()
    greenZone = get_greenZone_list()
    redZone = get_redZone_list()
    originalGreenZone = get_original_greenZone_list()
    for i in range(200):
        grid.append([])
        for j in range(200):
            grid[i].append(Node(1,(i,j)))
    for pt in obstaclePose:
        for i in range(pt[0][0],pt[2][0]+1):
            for j in range(pt[0][1],pt[2][1]+1):
                grid[i][j]=Node(0,(i,j))
    
    z=0
   
    for i in range(len(greenZone)):
        min1=1000
        min2=1000
        
        for j in range(len(greenZone)):
            for a in range(0,4):
                distance1 = math.sqrt( ((botsPose[0][0]-greenZone[j][a][0])**2)+(botsPose[0][1]-greenZone[j][a][1])**2)
                distance2 = math.sqrt( ((botsPose[1][0]-greenZone[j][a][0])**2)+(botsPose[1][1]-greenZone[j][a][1])**2)
                if(min1>distance1):
                    min1=distance1
                    z=j
                    p=a
                if(min2>distance2):
                    min2=distance2
                    y=j
                    q=a
                print("targets left:")
                print(greenZone[j][0])
        if(min1<min2):
            botsPose = get_botPose_list()
            start=grid[botsPose[0][0]][botsPose[0][1]]
            goal=grid[greenZone[z][p][0]][greenZone[z][p][1]]
            path=aStar(start, goal)
            t=0
        else:
            botsPose = get_botPose_list()
            start=grid[botsPose[1][0]][botsPose[1][1]]
            goal=grid[greenZone[y][q][0]][greenZone[y][q][1]]
            path=aStar(start, goal)
            t=1
        
            
      
    
    
            
        print(len(path))
        if t==0:
            print("final pos:",greenZone[z][p])
        else:
            print("final pos:",greenZone[y][q])
        
        pos=get_botPose_list()
        print("initial pos:",pos[t])
        sleep(0.05)
        for k in range(1,len(path)):
            successful_move, mission_complete = send_command(t,path[k].move)
            pos=get_botPose_list()
            if successful_move:
                print("YES")
            else:
                print("NO")
            if mission_complete:
                print("MISSION COMPLETE")
            pos=get_botPose_list()
            print(pos[t])
        if t==0:
            greenZone.pop(z)
        else:
            greenZone.pop(y)
            
            
def level4(botId):
    global grid
    global z
    global y
    moveType = 5
    botsPose = get_botPose_list()
    obstaclePose = get_obstacles_list()
    greenZone = get_greenZone_list()
    redZone = get_redZone_list()
    originalGreenZone = get_original_greenZone_list()
    for i in range(200):
        grid.append([])
        for j in range(200):
            grid[i].append(Node(1,(i,j)))
    for pt in obstaclePose:
        for i in range(pt[0][0],pt[2][0]+1):
            for j in range(pt[0][1],pt[2][1]+1):
                grid[i][j]=Node(0,(i,j))
    
    z=0
   
    for i in range(len(greenZone)):
        min=1000
        for j in range(len(greenZone)):
            for k in range(len(botsPose)):
                for a in range(0,4):
                    distance = math.sqrt( ((botsPose[k][0]-greenZone[j][a][0])**2)+(botsPose[k][1]-greenZone[j][a][1])**2)
                    if(min>distance):
                        min=distance
                        z=j
                        botno=k
                        y=a
        print("targets left:")
        print(greenZone[j][0])
            
        botsPose = get_botPose_list()
        start=grid[botsPose[botno][0]][botsPose[botno][1]]
        goal=grid[greenZone[z][y][0]][greenZone[z][y][1]]
        path=aStar(start, goal)
            
      
    
    
            
        print(len(path))
        print("final pos:",greenZone[z][y])
        pos=get_botPose_list()
        print("initial pos:",pos[botno])
        sleep(0.05)
        for k in range(1,len(path)):
            successful_move, mission_complete = send_command(botno,path[k].move)
            pos=get_botPose_list()
            if successful_move:
                print("YES")
            else:
                print("NO")
            if mission_complete:
                print("MISSION COMPLETE")
            pos=get_botPose_list()
            print(pos[botno])
        greenZone.pop(z)

def level5(botId):
    global grid
    global z
    global y
    moveType = 5
    botsPose = get_botPose_list()
    obstaclePose = get_obstacles_list()
    greenZone = get_greenZone_list()
    redZone = get_redZone_list()
    originalGreenZone = get_original_greenZone_list()
    for i in range(200):
        grid.append([])
        for j in range(200):
            grid[i].append(Node(1,(i,j)))
    for pt in obstaclePose:
        for i in range(pt[0][0],pt[2][0]+1):
            for j in range(pt[0][1],pt[2][1]+1):
                grid[i][j]=Node(0,(i,j))
    for r in redZone:
        for i in range(r[0][0],r[2][0]+1):
            for j in range(r[0][1],r[2][1]+1):
                grid[i][j]=Node(0,(i,j))
                
     
    z=0
    
    for i in range(len(greenZone)):
        min1=1000
        min2=1000
        
        for j in range(len(greenZone)):
            for a in range(0,4):
                distance1 = math.sqrt( ((botsPose[0][0]-greenZone[j][a][0])**2)+(botsPose[0][1]-greenZone[j][a][1])**2)
                distance2 = math.sqrt( ((botsPose[1][0]-greenZone[j][a][0])**2)+(botsPose[1][1]-greenZone[j][a][1])**2)
                if(min1>distance1):
                    min1=distance1
                    z=j
                    p=a
                if(min2>distance2):
                    min2=distance2
                    y=j
                    q=a
                print("targets left:")
                print(greenZone[j][0])
        if(min1<min2):
            botsPose = get_botPose_list()
            start=grid[botsPose[0][0]][botsPose[0][1]]
            goal=grid[greenZone[z][p][0]][greenZone[z][p][1]]
            path=aStar(start, goal)
            t=0
        else:
            botsPose = get_botPose_list()
            start=grid[botsPose[1][0]][botsPose[1][1]]
            goal=grid[greenZone[y][q][0]][greenZone[y][q][1]]
            path=aStar(start, goal)
            t=1
        
            
      
    
    
            
        print(len(path))
        if t==0:
            print("final pos:",greenZone[z][p])
        else:
            print("final pos:",greenZone[y][q])
        
        pos=get_botPose_list()
        print("initial pos:",pos[t])
        sleep(0.05)
        for k in range(1,len(path)):
            successful_move, mission_complete = send_command(t,path[k].move)
            pos=get_botPose_list()
            if successful_move:
                print("YES")
            else:
                print("NO")
            if mission_complete:
                print("MISSION COMPLETE")
            pos=get_botPose_list()
            print(pos[t])
        if t==0:
            greenZone.pop(z)
        else:
            greenZone.pop(y)
            
def level6(botId):
    global grid
    global z
    global y
    moveType = 5
    botsPose = get_botPose_list()
    obstaclePose = get_obstacles_list()
    greenZone = get_greenZone_list()
    redZone = get_redZone_list()
    originalGreenZone = get_original_greenZone_list()
    for i in range(200):
        grid.append([])
        for j in range(200):
            grid[i].append(Node(2,(i,j)))
    for pt in obstaclePose:
        for i in range(pt[0][0],pt[2][0]+1):
            for j in range(pt[0][1],pt[2][1]+1):
                grid[i][j]=Node(0,(i,j))
    for r in redZone:
        for i in range(r[0][0],r[2][0]+1):
            for j in range(r[0][1],r[2][1]+1):
                grid[i][j]=Node(2,(i,j))
    
    z=0
    
    for i in range(len(greenZone)):
        min=1000
        for j in range(len(greenZone)):
            for k in range(len(botsPose)):
                for a in range(0,4):
                    distance = math.sqrt( ((botsPose[k][0]-greenZone[j][a][0])**2)+(botsPose[k][1]-greenZone[j][a][1])**2)
                    if(min>distance):
                        min=distance
                        z=j
                        botno=k
                        y=a
        print("targets left:")
        print(greenZone[j][0])
            
        botsPose = get_botPose_list()
        start=grid[botsPose[botno][0]][botsPose[botno][1]]
        goal=grid[greenZone[z][y][0]][greenZone[z][y][1]]
        path=aStar(start, goal)
            
      
    
    
            
        print(len(path))
        print("final pos:",greenZone[z][y])
        pos=get_botPose_list()
        print("initial pos:",pos[botno])
        sleep(0.05)
        for k in range(1,len(path)):
            successful_move, mission_complete = send_command(botno,path[k].move)
            pos=get_botPose_list()
            if successful_move:
                print("YES")
            else:
                print("NO")
            if mission_complete:
                print("MISSION COMPLETE")
            pos=get_botPose_list()
            print(pos[botno])
        greenZone.pop(z)



#######    DON'T EDIT ANYTHING BELOW  #######################

if  __name__=="__main__":
    botId = int(sys.argv[1])
    level = get_level()
    if level == 1:
        level1(botId)
    elif level == 2:
        level2(botId)
    elif level == 3:
        level3(botId)
    elif level == 4:
        level4(botId)
    elif level == 5:
        level5(botId)
    elif level == 6:
        level6(botId)
    else:
        print("Wrong level! Please restart and select correct level")

