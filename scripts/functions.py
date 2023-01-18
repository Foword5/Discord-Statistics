import os
import json

def getUserInfo(path:str):
    """Get the user's ID"""
    if(not os.path.exists(path)): # We check if the path to the data exists
        return None
    
    with open(os.path.join(path,"account","user.json"), 'r') as userInfoFile: # read the json containing the user's info
        user = json.load(userInfoFile)
        return {
            "id" : user["id"],
            "username" : user["username"],
            "discriminator" : user["discriminator"],
            "avatar" : user["avatar_hash"]
        }

def getUserInfoById(id:str,path:str):

    if(not os.path.exists(path)): # We check if the path to the data exists
        return None

    with open(os.path.join(path,"account","user.json"), 'r') as userInfoFile: # read the json containing the user's info
        for friend in json.load(userInfoFile)["relationships"]:
            if friend["id"] == id:
                return friend["user"]
        return id