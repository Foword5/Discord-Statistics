import pandas as pd
from matplotlib import pyplot as plt

def messagesPerServerGraph(data:pd.DataFrame):
    
    dataPieChart = data.copy()
    dataPieChart.loc[dataPieChart["Count"] < 100, 'Guild'] = 'Other'
    dataPieChart = dataPieChart.groupby(["Guild"]).sum("Count")

    plt.pie(dataPieChart["Count"])
    
    return plt