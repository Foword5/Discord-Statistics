from scripts.dataCleanUp import readMessages
from scripts.dataExploring import mostWordSent
from config import *

import os


# the file containing the messages dataframe, in the newData folder
messageFile = "message.csv"

messagePath = os.path.join(NEWDATAPATH,messageFile)
if not os.path.exists(messagePath):
    readMessages(PACKAGEPATH).to_csv(messagePath)


print(
    mostWordSent(messagePath)
)