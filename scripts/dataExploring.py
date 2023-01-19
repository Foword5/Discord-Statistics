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
        [messages["Recipient"].notna()] # We take only messages comming from private channel
        .groupby(["Recipient"]) # grouping the data by user
        .count() # counting the messages
        .rename(columns = {"ID" : 'Count'}) # renaming the Id column to a more suitable name
        ["Count"] # keeping the column we want
        .reset_index()
    )

    messagesPerUser["RecipientName"] = messagesPerUser["Recipient"]
    for i in range(len(messagesPerUser["Recipient"])):
        userInfo = getUserInfoById(messagesPerUser["Recipient"][i],packagePath)
        if type(userInfo) != str:
            messagesPerUser["RecipientName"][i] = userInfo["username"]

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