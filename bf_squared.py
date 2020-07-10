
import numpy


matrixshape=(1,8,8) #z,x,y
matrixdatabase=numpy.zeros(matrixshape,dtype=int)
layercount=2 #z amount (use this if you want 3d)

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
         "self.dir=[0,0] \nself.pos[2]+=1",
         "self.dir=[0,0] \nself.pos[1]+=1",
         "self.dir=[0,0] \nself.pos[2]-=1",
         "self.dir=[0,0] \nself.pos[1]-=1",
         "dir=pos_if(self.variables, self.pos) \nif dir!= False and any(dir):\n self.pos[1]+=2*dir[0] \n self.pos[2]+=2*dir[1] ",
         "self.variables=int(matrixdatabase[self.returnpos()])",
         # Tile twelve takes all the variables from it's linked partners,
         # and then puts them into an array, and sets that as it's own
         # variables list. 
         "self.variables=[] \nfor i in range(len(self.linked)): \n   self.variables=numpy.append(self.variables,actorlist[self.linked[i]].variables)",

         # tiles 13-25 give orders to all the linked actors
         "for i in range(len(self.linked)): \n actorlist[self.linked[i]].orders=0",
         "for i in range(len(self.linked)): \n actorlist[self.linked[i]].orders=1",
         "for i in range(len(self.linked)): \n actorlist[self.linked[i]].orders=2",
         "for i in range(len(self.linked)): \n actorlist[self.linked[i]].orders=3",
         "for i in range(len(self.linked)): \n actorlist[self.linked[i]].orders=4",
         "for i in range(len(self.linked)): \n actorlist[self.linked[i]].orders=5",
         "for i in range(len(self.linked)): \n actorlist[self.linked[i]].orders=6",
         "for i in range(len(self.linked)): \n actorlist[self.linked[i]].orders=7",
         "for i in range(len(self.linked)): \n actorlist[self.linked[i]].orders=8",
         "for i in range(len(self.linked)): \n actorlist[self.linked[i]].orders=9",
         "for i in range(len(self.linked)): \n actorlist[self.linked[i]].orders=10",
         "for i in range(len(self.linked)): \n actorlist[self.linked[i]].orders=11",
         "for i in range(len(self.linked)): \n actorlist[self.linked[i]].orders=12",




         ] 

for i in range(layercount): #this part appends arrays of matrixshape 
    matrixdatabase=numpy.append(matrixdatabase,numpy.zeros(matrixshape, dtype=int),axis=0)

def pos_if(variable1, pos1):
    # this checks all actors and if they are close to pos1,
    # it checks if any of that actor's variables equal variable1.

    for i in range(len(actorlist)):
        if actorlist[i].pos != pos1:

            if abs(actorlist[i].pos[1]-pos1[1])+abs(actorlist[i].pos[2]-pos1[2])<=1:

                if actorlist[i].variables==variable1:

                    return [pos1[2]-actorlist[i].pos[2],pos1[1]-actorlist[i].pos[1]]

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
            exec(program[int(matrixdatabase[self.returnpos()])])

        else:
            #print(program[self.orders])
            exec(program[self.orders])

            self.orders=0
        # the actor slides if there is no code against it. 
        self.pos[1]+=self.dir[0]
        self.pos[2]+=self.dir[1]


# This makes a fun path.
# tile zero does nothing,
# tiles 1-4 changes the direction of the actor
# tile 5 sets the direction to [0,0]
# tiles 6-9 set direction to zero, but still shifts the actor. 
# tile 10 is the "if equal" tile
# tile eleven gets the actor to read what tile the actor is standing on
# tile twelve accumulates the data from it's linked partners
# the tiles 13-26 give orders to the actor's linked partners Ex:(tile 13 tells
# the partner to act as if it's on tile 0) 
matrixdatabase[0,0,0]=1
matrixdatabase[0,1,0]=14
matrixdatabase[0,3,0]=24
matrixdatabase[1,2,0]=12
matrixdatabase[0,4,0]=12
matrixdatabase[0,5,0]=10
matrixdatabase[0,7,2]=18
# So this program is set up to use 3 actors.
# the main actor starts at [0,0,0], it's linked counterpart starts at [1,0,0]
# the last actor is at [0,5,1] to act as an argument later.
#
# The program starts with [0,0,0] and tile 1, telling actor 0 to move to the
# right.
# Then, at [0,1,0], there is tile 14, telling the actor to command it's
# linked counterpart to move right as well.
# Then, as actor 1 (actor 0's counterpart) walks over tile 12, actor 0 goes
# over tile 24, which tell's it's counterpart to read it's tile. Thus,
# actor 1 stores tile 12 as it's variable.
# Then, actor 0 walks over tile twelve, which tells it to take the variable
# from it's counterpart.
# After that, actor 0 walks onto [0,5,0]. which is tile 10, an "if statement"
# Just below that tile, resides actor 2, who has the variable 12 stored.
# because of the if tile, actor 0 "hops" over actor 2.



##  MAIN LOOP
##
##
##
##  MAIN LOOP BELOW


#setting up all the actors
a=actor([0,0,0],[0,0],True)
a.linked=[1]
b=actor([1,0,0],[0,0],False)

c=actor([0,5,1],[0,0],False)
c.variables=12

actorlist=[a,b,c]
print(program[24])
for i in range(8):
    print("iter "+str(i)+":")
    for i in range(len(actorlist)):
        actorlist[i].run()
        print("Agent "+str(i)+" Pos: " +str(actorlist[i].pos))
        print("Agent "+str(i)+" variables: " +str(actorlist[i].variables))
        print("-=-")
    print()




