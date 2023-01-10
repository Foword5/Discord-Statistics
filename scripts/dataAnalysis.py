from scripts.functions import *
from scripts.dataCleanUp import *



def messagesPerServer(dataPath):
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