import json

class json_pareser:
    def set_postion_time(self):
        i=0
        self.postion_time={}
        for j in range(self.data["lastStepNum"]):
            self.postion_time[j]=self.data['ballPositions'][i]
            if(j==self.data['ballPositionsCT'][i] and i<(len(self.data['ballPositions'])-1)):
                i=i+1
        self.postion_time[self.data['ballPositionsCT'][-1]]=self.data['ballPositions'][-1]
        
    def set_velocity_time(self):
        i=0
        self.velocity_time={}
        for j in range(self.data["lastStepNum"]):
            self.velocity_time[j]=self.data['velocities'][i]
            if(j==self.data['velocitiesCT'][i] and i<(len(self.data['velocities'])-1)):
                i=i+1
        self.velocity_time[self.data['velocitiesCT'][-1]]=self.data['velocities'][-1]
    def set_object_postion_time(self):
        i=0
        self.objectPositions_time={}
        for j in range(self.data["lastStepNum"]):
            self.objectPositions_time[j]=self.data['objectPositions'][i]
            if(j==self.data['objectPositionsCT'][i] and i<(len(self.data['objectPositions'])-1)):
                i=i+1
        self.objectPositions_time[self.data['objectPositionsCT'][-1]]=self.data['objectPositions'][-1]
    def set_notes_time(self):
        i=0
        self.notes_time={}
        if(len(self.data["notes"])!=0):
            for j in range(self.data["lastStepNum"]):
                self.notes_time[j]=self.data['notes'][i]
                if(j==self.data['notesCT'][i] and i<(len(self.data['notes'])-1)):
                    i=i+1
            self.notes_time[self.data['notesCT'][-1]]=self.data['notes'][-1]

    def __init__(self,path):
        """ 1. data is just the json dictionary
            2. postion_time is a dictionary with key values for each time step related to the bals postion. 
            3. velocity_time dictionary with time keys and velcoity values 
            4.object_postion_time dictionary with time keys and object postion values  
            5.velocity_time dictionary with time keys and velcoity values 

            """
        self.data=json.load(open(path))    
        self.set_postion_time()
        self.set_velocity_time()
        self.set_object_postion_time()
        self.set_notes_time()

