"""
Authored By: Buz Galbraith

"""
import json
import pandas as pd

import json
import pandas as pd

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
        """
        self.data = json.load(open(path))
        self.tags = self.data["foundObjectsTags"]
        self.dim = len(self.tags)
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

    def make_df(self):
        def makeDict(posVec):
            dct = {}
            for i in range(self.dim):
                dct.update({f"{self.tags[i]}_x": posVec[i]["x"],
                            f"{self.tags[i]}_y": posVec[i]["y"]})
            return dct
        reshaped = [makeDict(self.data["objectPositions"][i:i+self.dim]) for i
                    in range(0, len(self.data["objectPositions"]), self.dim)]
        objPos = pd.DataFrame(reshaped)
        ballPos = pd.DataFrame(self.data["ballPositions"])[["x", "y"]]
        ballPos.columns = ["ball_x", "ball_y"]
        self.df = pd.concat((ballPos, objPos), axis=1)
        self.df.loc[self.data["velocitiesCT"], ["velocity_x", "velocity_y"]] = list(zip(pd.DataFrame(self.data["velocities"])["x"], pd.DataFrame(self.data["velocities"])["y"]))
        self.df.fillna(0, inplace=True)
        self.df.loc[self.data["resetCT"], "reset"] = 1
        self.df.loc[self.data["notesCT"], "note_taken"] = 1

    def row_check(self, x): 
        return (self.df["ball_x"][x] <= self.walls["X"]["Min"]) or \
                (self.df["ball_x"][x] >= self.walls["X"]["Max"]) or \
                (self.df["ball_y"][x] <= self.walls["Y"]["Min"]) or \
                (self.df["ball_y"][x] >= self.walls["Y"]["Max"])


