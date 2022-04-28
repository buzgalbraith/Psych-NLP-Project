"""
Authored By: Buz Galbraith

"""

import pandas as pd
import numpy as np
import json
from PlaceAndShootGym import *

class StateTraceParser:
    def __init__(self, path):
        """ 1. data is just the json dictionary
            2. position_time is a dictionary with key values for each time step related to the bals position. 
            3. velocity_time dictionary with time keys and velcoity values 
            4.object_position_time dictionary with time keys and object position values
            5.note_times dictionary with time keys and binary variable for if a note is posted
            6.reset_times dictionary with time keys and binary variable for if a reset is made
            7.lastStepNum the final time step 
            8. walls a nested dict with keys X and Y and sub keys max and min representing the game boundry
            9. df time indexed aggreagate dictioanry . 
            10. wall_hits subset of df where the ball hits walls. 
            11. not_wall_hits subset of df where teh ball does not hit the wall 9is the complement of wall hits)
            12. obs_vector a 2d vector such that [reset_number][obs_number]
        """
        self.data = json.load(open(path))
        self.obj_tags = self.data["foundObjectsTags"]
        self.colision_tags=self.data["foundCollidersTags"]
        self.dim = len(self.obj_tags)
        self.lastStepNum = self.data["lastStepNum"]
        self.walls = {"X": {"Max": self.data["boxMaxX"],
                            "Min": self.data["boxMinX"]},
                      "Y": {"Max": self.data["boxMaxY"],
                            "Min": self.data["boxMinY"]}}
        self.make_df()

        self.wall_hits = self.df[[self.row_check(
            i) for i in range(len(self.df["ball_x"]))]]
        self.not_wall_hits = self.df[[self.row_check(
            i) == False for i in range(len(self.df["ball_x"]))]]
        self.above_bucket = self.df[self.df["ball_y"] >= self.df["bucket_y"]]
        self.above_corner = self.df[self.df["ball_y"] >= self.df["corner_y"]]
        self.above_triangle = self.df[self.df["ball_y"]
                                      >= self.df["triangle_y"]]
        self.above_gear = self.df[self.df["ball_y"] >= self.df["gear_y"]]
        self.above_crate = self.df[self.df["ball_y"] >= self.df["crate_y"]]
        
        self.obs_vector=[]
        temp=[]
        cols = ['bucket_x','bucket_y','corner_x','corner_y','crate_x','crate_y','gear_x','gear_y','triangle_x','triangle_y'\
                        ,'ball_x','ball_y', 'velocity_x','velocity_y','collisons','reset']
        for i in range(self.lastStepNum):
            temp.append(Obs(self.df[cols].iloc[i]))
            if(self.df["reset"][i]==1.0 or i==self.lastStepNum-1):
                self.obs_vector.append(temp)
                temp=[]

    def make_df(self):
        def makeDict(posVec):
            dct = {}
            for i in range(self.dim):
                dct.update({f"{self.obj_tags[i]}_x": posVec[i]["x"],
                            f"{self.obj_tags[i]}_y": posVec[i]["y"]})
            return dct
        reshaped = [makeDict(self.data["objectPositions"][i:i+self.dim]) for i
                    in range(0, len(self.data["objectPositions"]), self.dim)]
        objPos = pd.DataFrame(reshaped)
        ballPos = pd.DataFrame(self.data["ballPositions"])[["x", "y"]]
        ballPos.columns = ["ball_x", "ball_y"]
        self.df = pd.concat((ballPos, objPos), axis=1)
        if len(self.data["velocitiesCT"])>0:
            self.df.loc[self.data["velocitiesCT"], ["velocity_x", "velocity_y"]] = list(zip(pd.DataFrame(self.data["velocities"])["x"], pd.DataFrame(self.data["velocities"])["y"]))
        else:
            self.df[["velocity_x", "velocity_y"]] = 0.0
        self.df.loc[self.data["resetCT"], "reset"] = 1
        self.df.loc[self.data["notesCT"], "note_taken"] = 1
        self.df.fillna(0, inplace=True)
        self.df["collisons"]=np.zeros([self.lastStepNum])
        for i in range(len(self.data["ballCollisions"])):
            self.df["collisons"][self.data["ballCollisionsCT"][i]]=self.data["ballCollisions"][i]
        

    def row_check(self, x): 
        return (self.df["ball_x"][x] <= self.walls["X"]["Min"]) or \
                (self.df["ball_x"][x] >= self.walls["X"]["Max"]) or \
                (self.df["ball_y"][x] <= self.walls["Y"]["Min"]) or \
                (self.df["ball_y"][x] >= self.walls["Y"]["Max"])

    def ballInBucket(self, timestep):
        MIN_X_DELTA = -0.1927506923675537
        MAX_X_DELTA = 0.2523689270019531
        MIN_Y_DELTA = -0.24334418773651123
        MAX_Y_DELTA = 0.6142134666442871

        x_delta = self.df.loc[timestep, "ball_x"] - self.df.loc[timestep, "bucket_x"]
        y_delta = self.df.loc[timestep, "ball_y"] - self.df.loc[timestep, "bucket_y"]

        return (MAX_X_DELTA>=x_delta>=MIN_X_DELTA) and (MAX_Y_DELTA>=y_delta>=MIN_Y_DELTA)


