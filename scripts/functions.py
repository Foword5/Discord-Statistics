import os
import json
import pandas as pd
from matplotlib import pyplot as plt

def getUserInfo(path:str):
    """
    Get the user's id, username, discriminator and avatar hash
    
    Parameters :
        path (string) : the path to the package
    
    Return :
        The user's information
    """
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
    """
    Get a user's information, only work on user with who the main user has a relationship with, else it will only return the given id

    Parameters :
        id (string) : the id of the user
        path (string) : the path to the package

    Return :
        The user's information
    """
    if(not os.path.exists(path)): # We check if the path to the data exists
        return None

    with open(os.path.join(path,"account","user.json"), 'r') as userInfoFile: # read the json containing the user's info
        for friend in json.load(userInfoFile)["relationships"]:
            if friend["id"] == id:
                return friend["user"]
        return id

def weighted_median(values:pd.Series,weights:pd.Series):
    """
    Compute the weighted median using the values and the weight

    Parameters :
        values (pandas.Series) the values
        weights (pandas.Series) the weights

    Return :
        the weighted median
    """
    middleWeight = int(sum(weights)/2)
    position = 0
    i = 0
    while i < len(values) and position < middleWeight :
        position += weights[i]
        i += 1
    return values[i]-0.5