from scripts.dataCleanUp import *
from scripts.dataExploring import *
from scripts.dataGraph import *
from scripts.functions import *
from config import *

from fpdf import FPDF

import os
import sys

if not os.path.exists(PACKAGE_PATH):
    sys.exit(
    "############################################################################################ \n" +
    "#                                                                                          # \n" +
    "#                                Package folder not found !                                # \n" +
    "#         Once you downloaded the data from discord, put them on the root folder           # \n" +
    "#                                under the name \"package\"                                  # \n" +
    "#                                                                                          # \n" +
    "############################################################################################ \n"
    )

# the file containing the messages dataframe, in the newData folder
messagesFile = "message.csv"

# creating the messages file if it doesn't exist
messagesPath = os.path.join(NEW_DATA_FOLDER,messagesFile)
if not os.path.exists(NEW_DATA_FOLDER):
    os.mkdir(NEW_DATA_FOLDER)
readMessages(PACKAGE_PATH,REMOVED_PREFIX).to_csv(messagesPath)

###########################################################################
#                                                                         #
#                             Building the PDF                            #
#                                                                         #
###########################################################################

printProgressBar(0, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # creating the main progress bar
pdf = FPDF(unit="mm",format=(450,360))
pdf.add_page()
pdf.set_font(FONT, size = 15)
pdf.set_fill_color(230,230,230)

#######################################################################
#                        Messages sent per sever                      #
#######################################################################

pdf.set_xy(10,10)
pdf.cell(100,100, fill=True) # we draw the cell
pdf.set_xy(10,10)

dataMessagePerServer = messagesPerServer(messagesPath).sort_values("Count",ascending=False) # getting the proper data
printProgressBar(1, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar
plotMessagePerServer = messagesPerServerGraph(dataMessagePerServer) # getting the graph to print
printProgressBar(2, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar

pdf.set_font(FONT, size = 20)
pdf.cell(100,10,txt="Messages sent per server", align="C", ln=1) # title

imgPath = os.path.join(NEW_DATA_FOLDER,"imageGraph1.png") # we create the path for the new image
plotMessagePerServer.savefig(imgPath,transparent=True,bbox_inches='tight') # we save the plot as a png file

pdf.image(imgPath,15,20,0,35) # we add the image to the pdf

dataToPrint = dataMessagePerServer[:][0:10].reset_index().drop("index", axis=1) # we prepare the data we're going to print under the pie chart
printString = ""

for i in range(len(dataToPrint)): # in case there isn't 10 different server we iterate the length of the data
    printString += str(i+1) + ". " + dataToPrint["GuildName"][i][0:35] + " - " + str(dataToPrint["Count"][i]) + "\n"

printString = printString.encode('latin-1', 'replace').decode('latin-1')

pdf.set_xy(20,55)
pdf.set_font(FONT, size = 12)
pdf.multi_cell(90,5,txt=printString, align="L") # we add the text to the pdf
printProgressBar(3, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar

#######################################################################
#                            Messages size                            #
#######################################################################

pdf.set_xy(120,10)
pdf.cell(200,100, fill=True) # we draw the cell
pdf.set_xy(120,10)

pdf.set_font(FONT, size = 20)
pdf.cell(200,10,txt="Length of the messages sent", align="C", ln=1) # title
pdf.set_font(FONT, size = 12)

dataMessageLength = messageSize(messagesPath)
printProgressBar(4, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar
plotMessageLength = messageSizeGraph(dataMessageLength)
printProgressBar(5, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar

imgPath = os.path.join(NEW_DATA_FOLDER,"imageGraph3.png") # we create the path for the new image
plotMessageLength.savefig(imgPath,transparent=True,bbox_inches='tight') # we save the plot as a png file

pdf.image(imgPath,120,20,200,0) # we add the image to the pdf
printProgressBar(6, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar

#######################################################################
#                        Messages sent per user                       #
#######################################################################

pdf.set_xy(330,10)
pdf.cell(100,100, fill=True) # we draw the cell
pdf.set_xy(330,10)

dataMessagePerUser = messagesPerUser(messagesPath, PACKAGE_PATH).sort_values("Count",ascending=False) # getting the proper data
printProgressBar(7, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar
plotMessagePerUser = messagesPerUserGraph(dataMessagePerUser) # getting the graph to print
printProgressBar(8, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar

pdf.set_font(FONT, size = 20)
pdf.cell(100,10,txt="Messages sent per user", align="C", ln=1) # we add the title

imgPath = os.path.join(NEW_DATA_FOLDER,"imageGraph2.png") # we create the path for the image
plotMessagePerUser.savefig(imgPath,transparent=True,bbox_inches='tight') # we save the plot as a png file

pdf.image(imgPath,335,20,0,35) # we add the image to the pdf

dataToPrint = dataMessagePerUser[:][0:10].reset_index().drop("index", axis=1) # we prepare the data we're going to print under the pie chart
printString = ""

for i in range(len(dataToPrint)): # in case there isn't 10 different server we iterate the length of the data
    printString += str(i+1) + ". " + dataToPrint["RecipientName"][i][0:35] + " - " + str(dataToPrint["Count"][i]) + "\n"

printString = printString.encode('latin-1', 'replace').decode('latin-1')

pdf.set_xy(340,55)
pdf.set_font(FONT, size = 12)
pdf.multi_cell(90,5,txt=printString, align="L") #  we add the text to the pdf
printProgressBar(9, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar

#######################################################################
#                         Most Sent messages                          #
#######################################################################

pdf.set_xy(10,120)
pdf.cell(100,210, fill=True) # we draw the cell# we draw the cell
pdf.set_xy(10,120)

pdf.set_font(FONT, size = 20)
pdf.cell(100,10,txt="Most sent messsages", align="C", ln=1) # we add the title
pdf.set_font(FONT, size = 12)

dataMostSendMessages = mostContentSent(messagesPath).sort_values("Count",ascending=False).reset_index()[:38]
printProgressBar(10, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar
printString = ""

for i in range(len(dataMostSendMessages)):
    content = dataMostSendMessages["Contents"][i]
    if len(content) > 35 :
        printString += str(i+1) + ". " + content[:32] + "... (" + str(dataMostSendMessages["Count"][i]) + ") \n"
    else :
        printString += str(i+1) + ". " + content + " (" + str(dataMostSendMessages["Count"][i]) + ") \n"

printString = printString.encode('latin-1', 'replace').decode('latin-1')

pdf.set_xy(20,130)
pdf.multi_cell(90,5,txt=printString, align="L") #  we add the text to the pdf
printProgressBar(11, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar

#######################################################################
#                           Most used word                            #
#######################################################################

pdf.set_xy(330,120)
pdf.cell(100,210, fill=True) # we draw the cell
pdf.set_xy(330,120)

pdf.set_font(FONT, size = 20)
pdf.cell(100,10,txt="Most used word", align="C", ln=1) # we add the title
pdf.set_font(FONT, size = 12)

dataMostUsedWord = mostWordSent(messagesPath).sort_values("Count",ascending=False).reset_index()[:38]
printProgressBar(12, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar
printString = ""

for i in range(len(dataMostUsedWord)):
    word = dataMostUsedWord["Word"][i]
    if len(content) > 35 :
        printString += str(i+1) + ". " + word[:32] + "... (" + str(dataMostUsedWord["Count"][i]) + ") \n"
    else :
        printString += str(i+1) + ". " + word + " (" + str(dataMostUsedWord["Count"][i]) + ") \n"

printString = printString.encode('latin-1', 'replace').decode('latin-1')

pdf.set_xy(340,130)
pdf.multi_cell(90,5,txt=printString, align="L") #  we add the text to the pdf
printProgressBar(13, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar

#######################################################################
#                          Favorite channel                           #
#######################################################################

pdf.set_xy(120,120)
pdf.cell(200,100, fill=True) # we draw the cell
pdf.set_xy(120,120)

pdf.set_font(FONT, size = 20)
pdf.cell(200,10,txt="Most popular channels", align="C", ln=1) # we add the title
pdf.set_font(FONT, size = 12)

dataFavChannel = messagesPerChannel(messagesPath)
printProgressBar(14, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar
plotFavChannel = messagesPerChannelGraph(dataFavChannel, PACKAGE_PATH)
printProgressBar(15, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar

imgPath = os.path.join(NEW_DATA_FOLDER,"imageGraph4.png") # we create the path for the image
plotFavChannel.savefig(imgPath,transparent=True,bbox_inches='tight') # we save the plot as a png file

pdf.image(imgPath,120,130,200,0) # we add the image to the pdf
printProgressBar(16, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar

#######################################################################
#                        Messages sent per day                        #
#######################################################################

pdf.set_xy(120,230) 
pdf.cell(200, 100, fill=True) # we draw the cell
pdf.set_xy(120,230)

pdf.set_font(FONT, size = 20)
pdf.cell(200,10,txt="Messages per day", align="C", ln=1) # we add the title
pdf.set_font(FONT, size = 12)

dataMessagesPerDay = messsagePerDay(messagesPath)
printProgressBar(17, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar
plotMessagesPerDay = messagePerDayGraph(dataMessagesPerDay)
printProgressBar(18, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar

imgPath = os.path.join(NEW_DATA_FOLDER,"imageGraph5.png") # we create the path for the image
plotMessagesPerDay.savefig(imgPath,transparent=True,bbox_inches='tight') # we save the plot as a png file

pdf.image(imgPath,120,240,200,0) # we add the image to the pdf
printProgressBar(19, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar

pdf.output("Result.pdf")
printProgressBar(20, 20, prefix = 'Creating the PDF :', suffix = 'Complete', length = 50) # updating the progressbar
print(
    "\n" +
    "############################################################################################ \n" +
    "#                                                                                          # \n" +
    "#                                  You're PDF is ready !                                   # \n" +
    "#                    The pdf as been created under the name \"Result.pdf\"                   # \n" +
    "#                                                                                          # \n" +
    "############################################################################################ \n"
)