import os
import json

def getUserId(path):
    """Get the user's ID"""
    if(not os.path.exists(path)): # We check if the path to the data exists
        return None
    
    with open(os.path.join(path,"account","user.json"), 'r') as userInfoFile: # read the json containing the user's info
        return json.load(userInfoFile)["id"]