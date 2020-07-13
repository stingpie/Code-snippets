

import time
import pygame
from pygame import freetype
import numpy


matrixshape=(1,10,10) #z,x,y
matrixdatabase=numpy.zeros(matrixshape,dtype=int)
layercount=2 #z amount (use this if you want 3d)

# stuff for controlling input.

cursorpos=[0,0,0]
cursortile=0
# gives names to the tiles you select. 
tilenames=["erase",
           "slide right",
           "slide up",
           "slide left",
           "slide down",
           "stop sliding",
           "shift right",
           "shift up",
           "shift left",
           "shift down",
           "if any equal",
           "get tile",
           "aggregate data",
           "add one",
           "subtract one",
           "add by variable",
           "subtract by variable",
           "toggle activity",
           "link actor",
           "remove link",
           "make actor"
           ]

tilesymbol=["",
            "→",
            "↑",
            "←",
            "↓",
            "X",
            "˃",
            "˄",
            "˂",
            "˅",
            "≈",
            "Ꙭ",
            "ↈ",
            "+",
            "-",
            "∑",
            "σ",
            "℮",
            "ꚙ",
            "ꙍ",
            "Ꙫ"
            ]


# program contains all the info about what specific tiles instruct the actor
# what to do.
# for example, program[0]="" because if an actor is on tile zero, it's behaivior
# isn't supposed to change
program=["",
         "self.dir=[1,0]",
         "self.dir=[0,1]",
         "self.dir=[-1,0]",
         "self.dir=[0,-1]",
         "self.dir=[0,0]",
         "self.dir=[0,0] \nself.pos[1]+=1",
         "self.dir=[0,0] \nself.pos[2]+=1",
         "self.dir=[0,0] \nself.pos[1]-=1",
         "self.dir=[0,0] \nself.pos[2]-=1",
         "dir=pos_if(self.variables, self.pos) \nif dir!= False and any(dir):\n self.pos[1]+=2*dir[0] \n self.pos[2]+=2*dir[1] ",
         "self.variables=int(matrixdatabase[self.returnpos()])",
         # Tile twelve takes all the variables from it's linked partners,
         # and then puts them into an array, and sets that as it's own
         # variables list. 
         "self.variables=[] \nfor i in range(len(self.linked)): \n   self.variables=numpy.append(self.variables,actorlist[self.linked[i]].variables)",
         #these next few edit the layer. 
         "matrixdatabase[self.returnpos()]+=1",
         "matrixdatabase[self.returnpos()]-=1",
         "matrixdatabase[self.returnpos()]+=self.variables[0]",
         "matrixdatabase[self.returnpos()]-=self.variables[0]",
         #makes the actor active/inactive
         "self.active = not self.active",
         #adds an actor with the index variable[0]
         "self.linked=numpy.append(self.linked,self.variables[0])",
         #Removes the linked actors of index variables[0]
         "self.linked=numpy.append(self.linked[:self.variables[0]],self.linked[self.variables[0]+1:])", 
         #this creates a new actor using six variables from self.variables[0:5]
         "actorlist=numpy.append(actorlist,actor(self.variables[0:2],self.variables[3:4],bool(self.variables[5])))",

         ] 

for i in range(layercount-1): #this part appends arrays of matrixshape 
    matrixdatabase=numpy.append(matrixdatabase,numpy.zeros(matrixshape, dtype=int),axis=0)

def pos_if(variable1, pos1): 
    # this checks all actors and if they are close to pos1,
    # it checks if any of that actor's variables equal variable1.

    for i in range(len(actorlist)):
        if actorlist[i].pos != pos1:
            if actorlist[i].pos[0]==pos1[0]:
                if abs(actorlist[i].pos[1]-pos1[1])+abs(actorlist[i].pos[2]-pos1[2])<=1:

                    if actorlist[i].variables==variable1:

                        return [actorlist[i].pos[1]-pos1[1] , actorlist[i].pos[2]-pos1[2]]

    return False

class actor(object):

    def __init__(self,pos,dir,active):
        #position should be in the form (z,x,y)
        self.pos=pos
        # direction should just be (x,y) but I may add z.
        self.dir=dir
        # the variables hold all the info from it's own layer, and
        # it's linked counterpart/s. 
        self.variables=[]
        # this holds the information about it's linked counterparts.
        # it should hold the counterpart's index
        self.linked=[]
        # In case it's ever neccessary for some actor to know another actor's
        # index, put it here. 
        self.index=0
        # "active" defines whether or not this actor recieves orders from
        # the matrix, or from another actor. 
        self.active=active
        # Orders is the tile number of the order it's partner want's it to do. 
        self.orders=0

    def returnpos(self):

        return (int(self.pos[0]),int(self.pos[1]),int(self.pos[2]))

    def run(self):
        if self.active:
            # executes the code from the specific tile that the actor
            # stands on
            tile=int(matrixdatabase[self.returnpos()]) 
            if tile <= len(program):
                exec(program[tile])
##                print(program[tile])
##                print()
            else:
                # if the tile has a value larger than the length of "program"
                # Assume it's trying to give an order to it's linked partners.
                # len(program) * which_linked_partner + tile_order
                if self.linked[0]>=0:
                    linked_actor=int(tile/len(program))-1
                    linked_order=tile%len(program)
                    actorlist[self.linked[linked_actor]].orders=linked_order
##                print(program[linked_order])
##                print()
                            
        else:
##            print(program[self.orders])
##            print(self.pos)
##            print(matrixdatabase[self.pos[0],self.pos[1],self.pos[2],])
            exec(program[self.orders])
##            print(program[self.orders])
##            print()
            self.orders=0
        # the actor slides if there is no code against it. 
        self.pos[1]+=self.dir[0]
        self.pos[2]+=self.dir[1]


def color_palette(col):
    square=pygame.Color(0,0,0)
    square.hsva=(2*len(program)*int(col/len(program)),bool(col)*100,50+1.5*(col%len(program)),100)
    return square



def draw():

    pygame.draw.rect(window,(80,120,80),(0,0,canvaswidth,canvasheight))

    sq=int(canvasheight/((matrixshape[2])*layercount+2))
    for z in range(layercount):
        for x in range(matrixshape[1]):
            for y in range(matrixshape[2]):
                squarepos=(x*sq+sq,(canvasheight-y*sq-2*sq)-z*sq*matrixshape[2]-z*sq)
                pygame.draw.rect(window,color_palette(matrixdatabase[z,x,y]),(squarepos[0],squarepos[1],sq,sq))

                if viewmode==1:
                    default.render_to(window,(squarepos),tilesymbol[matrixdatabase[z,x,y]%len(program)])
                if viewmode==2:
                    default.render_to(window,(squarepos),chr(matrixdatabase[z,x,y]+32))
                if viewmode==3:
                    default.render_to(window,(squarepos),str(matrixdatabase[z,x,y]))
                

                    
    radius=int(sq/2)
    for i in range(len(actorlist)):
        
        actorpos1=actorlist[i].pos[1]*sq+sq+radius
        actorpos2=(canvasheight-actorlist[i].pos[2]*sq-2*sq)-actorlist[i].pos[0]*sq*matrixshape[2]+radius -actorlist[i].pos[0]*sq
        pygame.draw.circle(window,(20,20,20),(actorpos1,actorpos2),radius)
        if isinstance(actorlist[i].variables,int):
            pygame.draw.circle(window,(color_palette(actorlist[i].variables)),(actorpos1,actorpos2),int(radius/2))
        elif len(actorlist[i].variables)>0:
            pygame.draw.circle(window,(color_palette(actorlist[i].variables[0])),(actorpos1,actorpos2),int(radius/2))
    
    cursorscreenpos=[0,0]
    cursorscreenpos[0]=cursorpos[1]*sq+sq
    cursorscreenpos[1]=(canvasheight-cursorpos[2]*sq-2*sq)-cursorpos[0]*sq*matrixshape[2] -cursorpos[0]*sq
    pygame.draw.rect(window,(255,255,254),(cursorscreenpos[0],cursorscreenpos[1],sq,sq),1)

    default.render_to(window,(int(canvaswidth/2),int(canvasheight/64)),str(int(cursortile/len(program)))+"x "+tilenames[cursortile%len(program)],fgcolor=(255,255,255))
    if actorplace:
        default.render_to(window,(int(canvaswidth/2),int(canvasheight/64)+fontsize),"actor placer",fgcolor=(255,255,255))
        default.render_to(window,(int(canvaswidth/2),int(canvasheight/64)+2*fontsize),"linked actor index: "+str(possiblelink),fgcolor=(255,255,255))    
    default.render_to(window,(int(canvaswidth/2),int(canvasheight/2)),"controls:",fgcolor=(255,255,255))
    default.render_to(window,(int(canvaswidth/2),int(canvasheight/2)+fontsize),"arrow keys: move cursor",fgcolor=(255,255,255))
    default.render_to(window,(int(canvaswidth/2),int(canvasheight/2)+fontsize*2),"q&e: increment / decrement",fgcolor=(255,255,255))
    default.render_to(window,(int(canvaswidth/2),int(canvasheight/2)+fontsize*3),"w: place",fgcolor=(255,255,255))
    default.render_to(window,(int(canvaswidth/2),int(canvasheight/2)+fontsize*4),"r: actor mode",fgcolor=(255,255,255))
    
    pygame.display.update()
    pygame.event.pump()
    
canvaswidth = 800
canvasheight = 600
pygame.display.init()
window= pygame.display.set_mode((canvaswidth, canvasheight) )



##  MAIN LOOP
##
##
##
##  MAIN LOOP BELOW


#setting up all the actors

actorlist=[]

pygame.freetype.init()
fontsize=int(canvasheight/((matrixshape[2])*layercount+2))-4
default=pygame.freetype.SysFont("Segoe UI",fontsize)
viewmode=0


up_pressed=0
right_pressed=0
down_pressed=0
left_pressed=0
space_pressed=0
e_pressed=0
q_pressed=0
w_pressed=0
r_pressed=0

possiblelink=0
playing=False
actorplace=False

while True:
    ## Input handling
    pygame.event.pump()
    key=pygame.key.get_pressed()
    
    if key[pygame.K_RIGHT] and right_pressed<=0:
        if cursorpos[1]+1<matrixshape[1]:
            cursorpos[1]+=1
        right_pressed=1
        
    if key[pygame.K_UP] and up_pressed<=0:
        if cursorpos[0]!=layercount-1 or cursorpos[2]!=matrixshape[2]-1:
            if cursorpos[0]+1<layercount and cursorpos[2]==matrixshape[2]-1:
                cursorpos[0]+=1
                cursorpos[2]=0
            else:
                cursorpos[2]+=1
        up_pressed=1
        
    if key[pygame.K_LEFT] and left_pressed<=0:
        if cursorpos[1]-1>=0:
            cursorpos[1]-=1
        left_pressed=1
            
    if key[pygame.K_DOWN] and down_pressed<=0:
        if cursorpos[0]!=0 or cursorpos[2]!=0:
            if cursorpos[0]-1>=0 and cursorpos[2]==0:
                cursorpos[0]-=1
                cursorpos[2]=matrixshape[2]-1
            else:
                cursorpos[2]-=1
        down_pressed=1

    if key[pygame.K_SPACE] and space_pressed<=0:
        playing= not playing
        space_pressed=1

    if key[pygame.K_q] and q_pressed<=0:
        cursortile-=1
        possiblelink-=1
        q_pressed=1
        
    if key[pygame.K_e] and e_pressed<=0:
        cursortile+=1
        possiblelink+=1
        e_pressed=1
    if key[pygame.K_w] and w_pressed<=0:
        if not actorplace:
            matrixdatabase[cursorpos[0],cursorpos[1],cursorpos[2]]=cursortile
        else:
            actorlist=numpy.append(actorlist,actor([cursorpos[0],cursorpos[1],cursorpos[2]],[0,0],True))
            actorlist[-1:][0].linked=[possiblelink]

        w_pressed=1
    if key[pygame.K_r] and r_pressed<=0:
        actorplace=not actorplace
        r_pressed=1

        

    if key[pygame.K_0]:
        viewmode=0
    if key[pygame.K_1]:
        viewmode=1
    if key[pygame.K_2]:
        viewmode=2
    if key[pygame.K_3]:
        viewmode=3
    if cursorpos[0]<0 or cursorpos[0]>layercount-1 or cursorpos[1]<0 or cursorpos[1]>=matrixshape[1] or cursorpos[2]<0 or cursorpos[2]>=matrixshape[2]:
        cursorpos=[0,0,0]
    
    space_pressed-=0.3
    right_pressed-=0.3
    up_pressed-=0.3
    left_pressed-=0.3
    down_pressed-=0.3
    e_pressed-=0.3
    q_pressed-=0.3
    w_pressed-=0.3
    r_pressed-=0.3
    #done with input handling

    
    draw()
    time.sleep(0.03)
##    print("iter "+str(i)+":")
    if playing:
        for i in range(len(actorlist)):
            actorlist[i].run()
    ##        print("Agent "+str(i)+" Pos: " +str(actorlist[i].pos))
    ##        print("Agent "+str(i)+" variables: " +str(actorlist[i].variables)
