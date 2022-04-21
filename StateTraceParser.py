"""
Authored by: Buz Galbraith

"""
import json
import pandas as pd 
class json_pareser:
    
    def set_ball_postion_time(self):
        i=0
        self.ball_postion_time={}
        for j in range(self.data["lastStepNum"]):
            self.ball_postion_time[j]=self.data['ballPositions'][i]
            if(j==self.data['ballPositionsCT'][i] and i<(len(self.data['ballPositions'])-1)):
                i=i+1
        self.ball_postion_time[self.data['ballPositionsCT'][-1]]=self.data['ballPositions'][-1]
        
    def set_velocity_time(self):
        i=0
        self.velocity_time={}
        for j in range(self.data["lastStepNum"]):
            self.velocity_time[j]=self.data['velocities'][i]
            if(j==self.data['velocitiesCT'][i] and i<(len(self.data['velocities'])-1)):
                i=i+1
        self.velocity_time[self.data['velocitiesCT'][-1]]=self.data['velocities'][-1]
    
    make_slice= lambda self,x:self.data["objectPositions"][(x)*int(len(self.data["objectPositions"])/len(self.data["foundObjectsTags"])):(x+1)*int(len(self.data["objectPositions"])/len(self.data["foundObjectsTags"]))]
    
    def set_object_postion_time(self):
        self.object_postion_time={}
        for i in range(len(self.data["foundObjectsTags"])):
            slice=self.make_slice(i)
            j=0
            self.object_postion_time[self.data["foundObjectsTags"][i]]={}
            for l in range(self.data["lastStepNum"]):
                self.object_postion_time[self.data["foundObjectsTags"][i]][l]=slice[j]
                if(l==self.data['objectPositionsCT'][j] and j<(len(slice)-1)):
                    j=j+1
                self.object_postion_time[self.data["foundObjectsTags"][i]][len(slice)-1]=slice[-1]

    def note_posted(self):
        self.note_times={}
        for i in range(self.data["lastStepNum"]):
            self.note_times[i]=0
            if(i in self.data["notesCT"]):
                self.note_times[i]=1
    def resets_posted(self):
        self.reset_times={}
        for i in range(self.data["lastStepNum"]):
            self.reset_times[i]=0
            if(i in self.data["resetCT"]):
                self.reset_times[i]=1

    def make_df(self):
        a=pd.Series([self.object_postion_time["corner"][x]["x"] for x in range(len(self.object_postion_time["corner"]))])
        b=pd.Series([self.ball_postion_time[x][y] for x in range(len(self.ball_postion_time))] for y in self.ball_postion_time[1].keys())
        c=pd.Series([self.velocity_time[x][y] for x in range(len(self.velocity_time))] for y in self.velocity_time[1].keys())
        d=pd.Series([self.object_postion_time["bucket"][x]["x"] for x in range(len(self.object_postion_time["bucket"]))])
        e=pd.Series([self.object_postion_time["triangle"][x]["x"] for x in range(len(self.object_postion_time["triangle"]))])
        f=pd.Series([self.object_postion_time["gear"][x]["x"] for x in range(len(self.object_postion_time["gear"]))])
        g=pd.Series([self.object_postion_time["crate"][x]["x"] for x in range(len(self.object_postion_time["crate"]))])
        h=pd.Series(self.reset_times[i] for i in range(len(self.reset_times)))
        i=pd.Series(self.note_times[i] for i in range(len(self.note_times)))
        temp={'Ball X':b[0], "Ball Y":b[1], "Velocity X":c[0],"Velocity Y":c[1],
         "Corner X":a[0], "Corner Y": a[1], "Bucket X":d[0],"Bucket Y":d[1],
         "Triangle X":e[0],"Triangle Y":e[1],"Gear X":f[0],"Gear Y":f[1],
         "Crate X":g[0],"Crate Y":g[1], "Reset":h, "Note Made":i
            } 
        self.df=pd.DataFrame(data=temp, index=self.ball_postion_time.keys())
    row_check= lambda self,x:(self.df["Ball X"][x]<=self.walls["X"]["Min"]) or (self.df["Ball X"][x]>=self.walls["X"]["Max"]) or (self.df["Ball Y"][x]<=self.walls["Y"]["Min"]) or (self.df["Ball Y"][x]>=self.walls["Y"]["Max"])
    



    def __init__(self,path):
        """ 1. data is just the json dictionary
            2. postion_time is a dictionary with key values for each time step related to the bals postion. 
            3. velocity_time dictionary with time keys and velcoity values 
            4.object_postion_time dictionary with time keys and object postion values
            5.note_times dictionary with time keys and binary variable for if a note is posted
            6.reset_times dictionary with time keys and binary variable for if a reset is made
            7.lastStepNum the final time step 
            8. walls a nested dict with keys X and Y and sub keys max and min representing the game boundry
            9. df time indexed aggreagate dictioanry . 
            10. wall_hits subset of df where the ball hits walls. 
            11. not_wall_hits subset of df where teh ball does not hit the wall 9is the complement of wall hits)
            """
        self.data=json.load(open(path))    
        self.set_ball_postion_time()
        self.set_velocity_time()
        self.set_object_postion_time()
        self.note_posted()
        self.resets_posted()
        self.lastStepNum=self.data["lastStepNum"]
        self.walls={"X":{"Max":self.data["boxMaxX"],"Min":self.data["boxMinX"]},"Y":{"Max":self.data["boxMaxY"],"Min":self.data["boxMinY"]}}
        self.make_df()
        self.wall_hits=self.df[[self.row_check(i) for i in range(len(self.df["Ball X"]))]]
        self.not_wall_hits=self.df[[self.row_check(i)==False for i in range(len(self.df["Ball X"]))]]
