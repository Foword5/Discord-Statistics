from scripts.functions import getUserInfoById

import pandas as pd
import os

def messagesPerServer(dataPath:str):
    """
    Get the number of messages sent in every discord server.

    Parameters :
        dataPath (string) : the path to the file containing all the messages, created by the function in dataCleanUp.py
    
    Return :
        A dataframe containing the list of every discord server and the number of messages sent in it
    """
    if not os.path.exists(dataPath):
        return None

    messages = pd.read_csv(dataPath, dtype = str, index_col=0)
    messages["Timestamp"] = pd.to_datetime(messages["Timestamp"]) # Changing data type from string to timestamp
    messages["Type"] = messages["Type"].astype(int)

    messagesPerSever = (
        messages
        [messages["Guild"].notna()] # We take only messages comming from a discord server
        .groupby(["Guild","GuildName"]) # grouping the data by server
        .count() # counting the messages
        .rename(columns = {"ID" : 'Count'}) # renaming the Id column to a more suitable name
        ["Count"] # keeping the column we want
        .reset_index()
    )
    
    return messagesPerSever


def messagesPerUser(dataPath:str, packagePath:str):
    """
    Get the number of messages sent to every user in private conversation.

    Parameters :
        dataPath (string) : the path to the file containing all the messages, created by the function in dataCleanUp.py
        packagePath (string) : the path to the package
    
    Return :
        A dataframe containing the list of every users to whom a message was sent and the number of messages sent in it
    """
    if not os.path.exists(dataPath):
        return None

    messages = pd.read_csv(dataPath, dtype = str, index_col=0)
    messages["Timestamp"] = pd.to_datetime(messages["Timestamp"]) # Changing data type from string to timestamp
    messages["Type"] = messages["Type"].astype(int)

    messagesPerUser = (
        messages
        .copy()
        [messages["Recipient"].notna()] # We take only messages comming from private channel
        .groupby(["Recipient"]) # grouping the data by user
        .count() # counting the messages
        .rename(columns = {"ID" : 'Count'}) # renaming the Id column to a more suitable name
        ["Count"] # keeping the column we want
        .reset_index()
    )

    recipientNames = [None] * len(messagesPerUser["Recipient"]) # We create a list for the recipient names
    for i in range(len(messagesPerUser["Recipient"])): # we iterate to either add the name or the id if there is no info on the user
        userInfo = getUserInfoById(messagesPerUser["Recipient"][i],packagePath) # we get the information on the user
        if type(userInfo) != str: # if the info is a string, it means there is no name, only an ID
            recipientNames[i] = userInfo["username"]
        else :
            recipientNames[i] = userInfo

    messagesPerUser["RecipientName"] = recipientNames # We add the RecipientName column

    return messagesPerUser

def mostContentSent(dataPath:str):
    """
    Count every message's content

    Parameters :
        dataPath (string) : the path to the file containing all the messages, created by the function in dataCleanUp.py
    
    Return :
        The dataframe contaning the different contents and the count of them
    """
    if not os.path.exists(dataPath):
        return None

    messages = pd.read_csv(dataPath, dtype = str, index_col=0)
    messages["Timestamp"] = pd.to_datetime(messages["Timestamp"]) # Changing data type from string to timestamp
    messages["Type"] = messages["Type"].astype(int)
    messages["Contents"] = messages["Contents"].str.lower()

    contentCount = (
        messages
        [messages["Contents"].notna()] # We take only messages that have content (so message that aren't only an attachment)
        .groupby("Contents") # grouping the data by content
        .count() # counting the messages
        .rename(columns = {"ID" : 'Count'}) # renaming the Id column to a more suitable name
        ["Count"] # keeping the column we want
        .reset_index()
    )

    return contentCount

def mostWordSent(dataPath:str):
    """
    Get the count of every word in every messages

    Parameters :
        dataPath (string) : the path to the file containing all the messages, created by the function in dataCleanUp.py

    Return :
        A dataframe with the words and their count
    """
    if not os.path.exists(dataPath):
        return None

    messages = pd.read_csv(dataPath, dtype = str, index_col=0)
    messages["Timestamp"] = pd.to_datetime(messages["Timestamp"]) # Changing data type from string to timestamp
    messages["Type"] = messages["Type"].astype(int)
    messages["Contents"] = messages["Contents"].str.lower()
    messages = messages[messages["Contents"].notna()]


    wordCount = messages.Contents.str.split(expand=True).stack().value_counts().reset_index()

    wordCount.columns = ['Word', 'Count'] 
    
    return wordCount

def messageSize(dataPath:str):
    """
    Count the number of messages sent per size

    Parameters :
        dataPath (String) : the path to the file containing all the messages, created by the function in dataCleanUp.py
    
    Return :
        A dataframe containing the different length with their count
    """
    if not os.path.exists(dataPath):
        return None

    messages = pd.read_csv(dataPath, dtype = str, index_col=0)
    messages["Length"] = messages["Contents"].str.len() # getting the length of the message
    
    messages = (
        messages
        .groupby("Length") # regroup the messages by length
        .count()
        .rename(columns = {"ID" : 'Count'}) # renaming the Id column to a more suitable name
        ["Count"] # keeping the column we want
        .reset_index()

    )
    total = sum(messages["Count"]) # we take the total of messages sent
    messages = messages[messages.Count > total*0.001].reset_index().drop("index", axis=1) # we only keep the length that have more than 0.05% of messages

    return messages

def messagesPerChannel(dataPath:str):
    """
    Counting every channel's messages

    Parameters :
        dataPath (String) : the path to the file containing all the messages, created by the function in dataCleanUp.py
    
    Return :
        the dataframe containing every channel and their count of messages
    """
    if not os.path.exists(dataPath):
        return None

    messages = pd.read_csv(dataPath, dtype = str, index_col=0)

    # returnDF = pd.DataFrame(columns=["Channel","Type","Recipient","ChannelName","GuildName","GroupName","ThreadName"])

    messagesType1 = (
        messages
        [messages["Type"] == "1"] # keeping only the type we want
        .groupby(["Channel","Recipient"])
        .count()
        .rename(columns = {"ID" : 'Count'}) # renaming the Id column to a more suitable name
        ["Count"]
        .reset_index()
    )
    messagesType1["Type"] = 1 # Readding the type column

    messagesType02 = (
        pd.concat([messages[messages.Type == "0"],messages[messages.Type == "2"]]) # keeping only the type we want
        .groupby(["Channel","ChannelName","GuildName"])
        .count()
        .rename(columns = {"ID" : 'Count'}) # renaming the Id column to a more suitable name
        ["Count"]
        .reset_index()
    )
    messagesType02["Type"] = 0 # Readding the type column

    messagesType3 = (
        messages
        [messages.Type == "3"] # keeping only the type we want
        .groupby(["Channel","GroupName"])
        .count()
        .rename(columns = {"ID" : 'Count'}) # renaming the Id column to a more suitable name
        ["Count"]
        .reset_index()
    )
    messagesType3["Type"] = 3 # Readding the type column

    messagesType11 = (
        messages
        [messages.Type == "11"] # keeping only the type we want
        .groupby(["Channel","ThreadName","GuildName"])
        .count()
        .rename(columns = {"ID" : 'Count'}) # renaming the Id column to a more suitable name
        ["Count"]
        .reset_index()
    )
    messagesType11["Type"] = 11 # Readding the type column

    returnDF = pd.concat([messagesType1,messagesType02,messagesType3,messagesType11]) # fusing all the dataframes

    print(returnDF)