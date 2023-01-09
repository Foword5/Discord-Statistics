import pandas as pd
import os
import json

from scripts.functions import *

def readMessages(path):
    """read all the messages from the path and combine them into one dataframe"""
    userID = getUserId(path) # We get the user's id
    path = os.path.join(path,"messages") # We change the path to access the messages directly

    if(not os.path.exists(path)): return None # We check if the path to the data exists

    messagesData = pd.DataFrame() # We create a new empty dataframe, we will append each channel info in it

    for channel in os.listdir(path): # We get all the files in the folder, each representing a channel
        channelPath = os.path.join(path,channel) # We create the path to the channel folder
        if(os.path.exists(channelPath) and os.path.isdir(channelPath) and os.path.exists(os.path.join(channelPath,"messages.csv"))) : # We make sure that it is a foler that exists and contain the csv file
            channelData = pd.read_csv(os.path.join(channelPath,"messages.csv"),dtype = str) # We read the data from the csv file contained in the folder
            
            channelData["Timestamp"] = pd.to_datetime(channelData["Timestamp"]) # Changing data type from string to timestamp
            channelData["Channel"] = channel.replace("c","") # We add a column with the channel id 

            with open(os.path.join(path,channel,"channel.json"), 'r') as channelInfoFile: # we read the channel info 
                channelInfo = json.load(channelInfoFile) 

                channelData["type"] = channelInfo["type"] # We add a column for the channel type

                # Depending on the type we save different informations about the channel
                if channelInfo["type"] == 0 or channelInfo["type"] == 2 :
                    if "name" in channelInfo :
                        channelData["channelName"] = channelInfo["name"] 
                        channelData["guild"] = channelInfo["guild"]["id"] 
                        channelData["guildName"] = channelInfo["guild"]["name"]
                    else :
                        channelData["channelName"], channelData["guild"], channelData["guildName"] = "unknownChannelName","unknownGuildID","unknownGuildName"
                elif channelInfo["type"] == 1 :
                    if "recipients" in channelInfo :
                        channelData["recipient"] = channelInfo["recipients"][0] if channelInfo["recipients"][0] != userID else channelInfo["recipients"][1]
                elif channelInfo["type"] == 3 :
                    channelData["groupName"] = channelInfo["name"] if "name" in channelInfo else "unknownGroupName"
                elif channelInfo["type"] == 11 :
                    if "name" in channelInfo :
                        channelData["threadName"] = channelInfo["name"] 
                        channelData["guild"] = channelInfo["guild"]["id"] 
                        channelData["guildName"] = channelInfo["guild"]["name"]
                    else :
                        channelData["threadName"], channelData["guild"], channelData["guildName"] = "unknownThreadName","unknownGuildID","unknownGuildName"

            messagesData = pd.concat([messagesData,channelData]) # We add the dataframe for the channel's messages to the overall messages
    
    return messagesData.reset_index().drop("index", axis=1) # return the dataframe



def readEmoji(path):
    """Read the emoji data of the user"""
    path = os.path.join(path,"account","user.json") # We change the path to access the user's info directly

    if(not os.path.exists(path)): return None # We check if the path to the data exists

    emojiData =[]

    with open(os.path.join(path), 'r') as userInfoFile: # we read the channel info 
        emojiJSONData = json.load(userInfoFile)["settings"]["frecency"]["emojiFrecency"]["emojis"]

        for emoji in emojiJSONData.keys():
            emojiData.append([emoji, emojiJSONData[emoji]["totalUses"]])
    
    return pd.DataFrame(emojiData, columns = ["name","totalUses"])