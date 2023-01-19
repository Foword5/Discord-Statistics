import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

def percentPrinted(val:int):
    """
    Get a string to print the percentage on the pie chart.
    
    Parameter :
        val (int) : the percentage
    
    Return :
        The rounded up percentage with the "%" sign or nothing if the percentage is less than 5%
    """
    returnedValue = np.round(val, 1)  # calculate the percentage of the value
    return str(returnedValue) + "%" if returnedValue > 5 else ""  # if the percentage is less than 10, we don't print the percentage
        
def messagesPerServerGraph(data:pd.DataFrame):
    """
    Create a pie chart of the messages sent per discord server

    Parameters :
        data (panda.Dataframe) : the dataframe of the messages per server created using the function "messagesPerServer"
    
    Return :
        The pie chart
    """
    plt.clf()
    dataPieChart = data.copy() # we copy the dataframe to not modify the original
    total = sum(dataPieChart["Count"]) # We get the total number of messages
    dataPieChart.loc[dataPieChart["Count"] < total*0.04, 'Guild'] = 'Other' # to not have to many servers on the pie chart, we group every server that has less than 1% in one group, "other"
    dataPieChart.loc[dataPieChart["Count"] < total*0.04, 'GuildName'] = 'Other' # once again but for the name
    dataPieChart = dataPieChart.groupby(["Guild","GuildName"]).sum("Count").reset_index() # to regroup the 1% and less servers

    plt.pie(dataPieChart["Count"],labels=dataPieChart["GuildName"],autopct=percentPrinted, textprops={'fontsize': 20}) # we create the pie chart

    return plt

def messagesPerUserGraph(data:pd.DataFrame):
    """
    Create a pie chart of the messages sent per discord users

    Parameters :
        data (panda.Dataframe) : the dataframe of the messages per user created using the function "messagesPerUser"
    
    Return :
        The pie chart
    """
    plt.clf()
    dataPieChart = data.copy() # we copy the dataframe to not modify the original
    total = sum(dataPieChart["Count"]) # We get the total number of messages
    dataPieChart.loc[dataPieChart["Count"] < total*0.04, 'Recipient'] = 'Other' # to not have to many servers on the pie chart, we group every server that has less than 1% in one group, "other"
    dataPieChart.loc[dataPieChart["Count"] < total*0.04, 'RecipientName'] = 'Other' # once again but for the name
    dataPieChart = dataPieChart.groupby(["Recipient","RecipientName"]).sum("Count").reset_index() # to regroup the 1% and less servers


    plt.pie(dataPieChart["Count"],labels=dataPieChart["RecipientName"],autopct=percentPrinted, textprops={'fontsize': 20}) # we create the pie chart

    return plt

def messageSizeGraph(data:pd.DataFrame):
    plt.clf()

    plt.bar(data["Length"],data["Count"])
    plt.xticks(range(0,len(data["Count"]),5))
    plt.gcf().set_size_inches(10, 4)

    plt.xlabel("Length of the message")
    plt.ylabel("Number of messages")

    return plt