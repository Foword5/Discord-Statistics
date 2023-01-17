from scripts.functions import *
from scripts.dataCleanUp import *


def messagesPerServer(dataPath):
    """
    Get the number of messages sent in every discord server.

    Parameters :
        dataPath (int) : the path to the file containing all the messages, created by the function in dataCleanUp.py
    
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


def messagesPerUser(dataPath):
    """
    Get the number of messages sent to every user in private conversation.

    Parameters :
        dataPath (int) : the path to the file containing all the messages, created by the function in dataCleanUp.py
    
    Return :
        A dataframe containing the list of every users to whom a message was sent and the number of messages sent in it
    """
    if not os.path.exists(dataPath):
        return None

    messages = pd.read_csv(dataPath, dtype = str, index_col=0)
    messages["Timestamp"] = pd.to_datetime(messages["Timestamp"]) # Changing data type from string to timestamp
    messages["Type"] = messages["Type"].astype(int)

    messagesPerSever = (
        messages
        [messages["Recipient"].notna()] # We take only messages comming from private channel
        .groupby(["Recipient"]) # grouping the data by user
        .count() # counting the messages
        .rename(columns = {"ID" : 'Count'}) # renaming the Id column to a more suitable name
        ["Count"] # keeping the column we want
        .reset_index()
    )
