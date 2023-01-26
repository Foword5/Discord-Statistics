import pandas as pd
import os
import json

from scripts.functions import getUserInfo,printProgressBar

def readMessages(path:str, prefixes:list):
    """
    Read all the messages from the path and combine them into one dataframe
    
    Parameters :
        path (string) : the path to the package
        prefixes (list of string) : prefixes to tell which message to disregard

    Return :
        The dataframe containing all the messages
    """
    userID = getUserInfo(path)["id"] # We get the user's id
    path = os.path.join(path,"messages") # We change the path to access the messages directly

    if(not os.path.exists(path)): return None # We check if the path to the data exists

    messagesData = pd.DataFrame(columns=["ID","Timestamp","Contents","Attachments","Channel","Type","Unknown","Recipient","ChannelName","Guild","GuildName","GroupName","ThreadName"]) # We create a new empty dataframe, we will append each channel info in it
    messagesData["Unknown"] = messagesData["Unknown"].astype(bool)

    nbrOfChannel = len(os.listdir(path)) # Number of channel present in the directory

    iteration = 0
    printProgressBar(0, nbrOfChannel, prefix = 'Reading Data :', suffix = 'Complete', length = 50) # Creating the progress bar
    for channel in os.listdir(path): # We get all the files in the folder, each representing a channel
        channelPath = os.path.join(path,channel) # We create the path to the channel folder
        if(os.path.exists(channelPath) and os.path.isdir(channelPath) and os.path.exists(os.path.join(channelPath,"messages.csv"))) : # We make sure that it is a foler that exists and contain the csv file
            channelData = pd.read_csv(os.path.join(channelPath,"messages.csv"),dtype = str) # We read the data from the csv file contained in the folder
            
            channelData["Timestamp"] = pd.to_datetime(channelData["Timestamp"]) # Changing data type from string to timestamp
            channelData["Channel"] = channel.replace("c","") # We add a column with the channel id 

            with open(os.path.join(path,channel,"channel.json"), 'r') as channelInfoFile: # we read the channel info 
                channelInfo = json.load(channelInfoFile) 

                channelData["Type"] = channelInfo["type"] # We add a column for the channel type
                channelData["Unknown"] = False

                # Depending on the type we save different informations about the channel
                if channelInfo["type"] == 0 or channelInfo["type"] == 2 :
                    if "name" in channelInfo :
                        channelData["ChannelName"] = channelInfo["name"] 
                        channelData["Guild"] = channelInfo["guild"]["id"] 
                        channelData["GuildName"] = channelInfo["guild"]["name"]
                    else :
                        channelData["Unknown"] = True
                elif channelInfo["type"] == 1 :
                    if "recipients" in channelInfo :
                        channelData["Recipient"] = channelInfo["recipients"][0] if channelInfo["recipients"][0] != userID else channelInfo["recipients"][1]
                    else :
                        channelData["Unknown"] = True
                elif channelInfo["type"] == 3 :
                    if "name" in channelInfo:
                        channelData["GroupName"] = channelInfo["name"]
                    else :
                        channelData["Unknown"] = True
                elif channelInfo["type"] == 11 :
                    if "name" in channelInfo :
                        channelData["ThreadName"] = channelInfo["name"] 
                        channelData["Guild"] = channelInfo["guild"]["id"] 
                        channelData["GuildName"] = channelInfo["guild"]["name"]
                    else :
                        channelData["Unknown"] = True

            messagesData = pd.concat([messagesData,channelData]) # We add the dataframe for the channel's messages to the overall messages

        iteration += 1
        printProgressBar(iteration, nbrOfChannel, prefix = 'Reading Data :', suffix = 'Complete', length = 50) # moving the progress bar

    messagesData = messagesData.reset_index().drop("index", axis=1)
    messagesData = messagesData[~messagesData["Contents"].str.startswith(tuple(prefixes)).fillna(False)] # removing the messages starting with the forbiden prefixes

    return messagesData # return the dataframe
