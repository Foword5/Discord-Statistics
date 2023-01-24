from scripts.functions import *

import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
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
        data (pandas.Dataframe) : the dataframe of the messages per server created using the function "messagesPerServer"
    
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
        data (pandas.Dataframe) : the dataframe of the messages per user created using the function "messagesPerUser"
    
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
    """
    Create a barPlot of the length of messages by the number of messages

    Parameters :
        data (pandas.Dataframe) : the dataframe of the messages per length, created by the function "messageSize"
    
    Return :
        The barPlot
    """
    plt.clf()

    plt.bar(data["Length"],data["Count"]) # Create the plot
    plt.xticks(range(0,len(data["Count"]),5)) # add the x ticks
    plt.gcf().set_size_inches(10, 4) # change the graph size

    max = data.sort_values("Count",ascending=False).reset_index()["Length"][0] # getting the max value
    textSummary = (
        "Mean : " + str(round(sum(data["Length"]*data["Count"])/sum(data["Count"]),2)) + "\n" + # computing the mean
        "Median : " + str(weighted_median(data["Length"],data["Count"])) + "\n" + # computing the median
        "Max : " + str(int(max)) + " (" + str(data["Count"][max]) + ")" 
    )

    # setting the x and y coordinates for the box
    x = data["Length"].max() * 0.85 
    y = data["Count"].max() * 0.8

    # adding the text box on the graph
    plt.text(x=x,y=y,s=textSummary,fontsize = 10, bbox = dict(facecolor = 'lightblue', alpha = 1))

    # adding the labels
    plt.xlabel("Length of the message") 
    plt.ylabel("Number of messages")

    return plt

def messagesPerChannelGraph(data:pd.DataFrame,packagePath:str):
    """
    Create a barplot for the most popular channels

    Parameters :
        data (pandas.Dataframe) : the dataframe of the messages per server created using the function "messagesPerChannel"
        packagePath (string) : the path to the package containing the user's data

    Return :
        The barPlot
    """
    plt.clf()

    data = data.sort_values("Count", ascending=False)[:10].reset_index().drop("index", axis=1) # sorting and keeping only the top
    data["Name"] = None # adding the name column
    data["Color"] = None # adding the Color column

    # setting the name and color to different values depending on the type of channel
    for i in data.index :
        match data["Type"][i]:
            case 0 :
                data.loc[(i,"Name")] = data["ChannelName"][i] + "\n(" + data["GuildName"][i] + ")"
                data.loc[(i,"Color")] = "blue"
            case 1:
                userInfo = getUserInfoById(data["Recipient"][i],packagePath) # we get the information on the user
                if type(userInfo) != str: # if the info is a string, it means there is no name, only an ID
                    data.loc[(i,"Name")] = userInfo["username"]
                else :
                    data.loc[(i,"Name")] = userInfo
                data.loc[(i,"Color")] = "red"
            case 3:
                data.loc[(i,"Name")] = data["GroupName"][i]
                data.loc[(i,"Color")] = "yellow"
            case _:
                data.loc[(i,"Name")] = data["ThreadName"][i] + "\n(" + data["GuildName"][i] + ")"
                data.loc[(i,"Color")] = "green"

    plt.bar(data["Name"],data["Count"], color=data["Color"]) # Create the plot
    
    for i in data.index :
        plt.text(s=data["Count"][i], x=i , y=data["Count"][i], ha = 'center')



    legendColor=[ # to create the legend
        mpatches.Patch(color="blue", label="Sever"),
        mpatches.Patch(color="red", label="Private message"),
        mpatches.Patch(color="yellow", label="Group"),
    ]

    plt.gcf().set_size_inches(14, 4) # change the graph size
    plt.legend(handles=legendColor, bbox_to_anchor=(1, 1), fancybox=True, shadow=True, ncol=3) # creating the legend
    plt.xticks(rotation=30, ha='right')
    plt.xlabel("Channel") 
    plt.ylabel("Number of messages")

    return plt

def messagePerDayGraph(data:pd.DataFrame):
    """
    Create a plot to represent the evolution of the number of messages sent everyday

    Parameters :
        data (pandas.Dataframe) : the dataframe of the messages per server created using the function "messsagePerDay"

    Return :
        The barPlot
    """
    plt.clf()

    plt.plot(data["Date"],data["Count"])
    
    window = 30
    movingAvg = movingAverage(data["Count"],window)

    plt.plot(data["Date"][int(window/2):len(movingAvg)+int(window/2)],movingAvg, color = "red")
    
    plt.gcf().set_size_inches(10, 4) # change the graph size

    max = data.sort_values("Count", ascending=False).reset_index()["index"][0]

    textSummary = (
        "Max : " + str(data["Count"][max]) + " (" + str(data["Date"][max]) + ") \n" +
        "Mean : " + str(round((sum(data["Count"])/len(data["Count"])),2)) + "\n" +
        "Median : " +  str(data["Count"].median())
    )

    # adding the text box on the graph
    plt.text(x=data["Date"].max(),y=data["Count"][max],s=textSummary,fontsize = 10, bbox = dict(facecolor = 'lightblue', alpha = 1))

    plt.xticks(rotation=30, ha='right')
    plt.xlabel("Years") 
    plt.ylabel("Number of messages")

    return plt