# _*_ coding: UTF-8 _*_
##############################################################
## this module contains a class for generating racing tracks
##############################################################

#Input is a Tupel with Tupel of (x,y,z)
#They are the midpoints of the Street



def thickness(tupelOfTupel):
    '''
    '''
    varthickness = []
    #Generate the Vector for thickness of the road
    
    for i in range(len(tupelOfTupel)-1):
        if i == 0:
            varthickness.append(calcTheVector(tupelOfTupel[len(tupelOfTupel)-1],tupelOfTupel[i],tupelOfTupel[i+1]))
            continue
        varthickness.append(calcTheVector(tupelOfTupel[i-1],tupelOfTupel[i],tupelOfTupel[i+1]))
    varthickness.append(calcTheVector(tupelOfTupel[len(tupelOfTupel)-2],tupelOfTupel[len(tupelOfTupel)-1],tupelOfTupel[0]))
    
    #Normalizing the Vector
    for i in varthickness:
        pass
        ##TODO
        #normalizing(i)
    #Creating the Vertex
    ##TODO
    #Conect the Vertex
    ##TODO
    #?Show the Mesh
    ##TODO
    ##Debugprint
    print varthickness
    #return List
    return varthickness

def calcTheVector(pre, now, past):
    vector1 = (pre[0] - now[0], pre[1] - now[1])    ##BUG!!!!!!!!!!!!!!!! Wie rum???
    vector2 = (past[0] - now[0], past[1] - now[1])  ##BUG!!!!!!!!!!!!!!!!
    high = pre[2] - past[2]
    return ((vector1[1] + vector2[1])/2.0),((vector1[0] + vector2[0])/2.0), high


#Test
tuple = ((1.0,2.0,3.0),(3.0,4.0,5.0),(6.0,4.0,2.0),(8.0,3.0,6.0),(4.0,7.0,2.0))
tuple2 = ((-2.0, -3.0, 0.0),(1.0, -5.0, 0.0),(4.0, -4.0, 0.0),(6.0, 0.0, 0.0),(3.0, 4.0, 0.0),(-2.0, 6.0, 0.0),(-7.0, 3.0, 0.0),(-8.0, -2.0, 0.0))
tuple3 = ((10.0,10.0,0.0),(10.0,-10.0,0.0),(-10.0,-10.0,0.0),(-10.0,10.0,0.0))
thickness(tuple3)