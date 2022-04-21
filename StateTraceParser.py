"""
Authored by: Buz Galbraith

"""
import json

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
    
    def set_notes_time(self):
        i=0
        self.notes_time={}
        if(len(self.data["notes"])!=0):
            for j in range(self.data["lastStepNum"]):
                self.notes_time[j]=self.data['notes'][i]
                if(j==self.data['notesCT'][i] and i<(len(self.data['notes'])-1)):
                    i=i+1
            self.notes_time[self.data['notesCT'][-1]]=self.data['notes'][-1]
    def set_resets(self):
        self.reset_times={}
        for i in range(self.data["lastStepNum"]):
            self.reset_times[i]=0
            if(i in self.data["resetCT"]):
                self.reset_times[i]=1

    def __init__(self,path):
        """ 1. data is just the json dictionary
            2. postion_time is a dictionary with key values for each time step related to the bals postion. 
            3. velocity_time dictionary with time keys and velcoity values 
            4.object_postion_time dictionary with time keys and object postion values  
            5.velocity_time dictionary with time keys and velcoity values 

            """
        self.data=json.load(open(path))    
        self.set_ball_postion_time()
        self.set_velocity_time()
        self.set_object_postion_time()
        self.set_notes_time()
        self.set_resets()
        self.lastStepNum=self.data["lastStepNum"]
        self.boxMaxX=self.data["boxMaxX"]
        self.boxMaxY=self.data["boxMaxY"]
        self.boxMinY=self.data["boxMinY"]
        self.boxMinX=self.data["boxMinX"]
        

