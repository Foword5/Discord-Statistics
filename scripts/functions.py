import os
import json
from fpdf import FPDF
from matplotlib import pyplot as plt

def getUserInfo(path:str):
    """
    Get the user's id, username, discriminator and avatar hash
    
    Parameters :
        path (string) : the path to the package
    
    Return :
        The user's information
    """
    if(not os.path.exists(path)): # We check if the path to the data exists
        return None
    
    with open(os.path.join(path,"account","user.json"), 'r') as userInfoFile: # read the json containing the user's info
        user = json.load(userInfoFile)
        return {
            "id" : user["id"],
            "username" : user["username"],
            "discriminator" : user["discriminator"],
            "avatar" : user["avatar_hash"]
        }

def getUserInfoById(id:str,path:str):
    """
    Get a user's information, only work on user with who the main user has a relationship with, else it will only return the given id

    Parameters :
        id (string) : the id of the user
        path (string) : the path to the package

    Return :
        The user's information
    """
    if(not os.path.exists(path)): # We check if the path to the data exists
        return None

    with open(os.path.join(path,"account","user.json"), 'r') as userInfoFile: # read the json containing the user's info
        for friend in json.load(userInfoFile)["relationships"]:
            if friend["id"] == id:
                return friend["user"]
        return id

def addGraphToPDF(pdf:FPDF,plot:plt,path:str,x:int,y:int,w:int=0,h:int=0):
    """
    Add a plot image to a pdf

    Parameters :
        pdf (FPDF) : the pdf
        plot (plt) : the plot
        path (string) : the path to the temporary data
        x (int) : x coordinate to place the plot
        y (int) : y coordinate to place the plot
        w (int) (default = 0) : the width of the plot (0 being the unmodified width)
        h (int) (default = 0) : the height of the plot (0 being the unmodified height)
    """
    if(not os.path.exists(path)): # We check if the path to the data exists
        return None

    imgPath = os.path.join(path,"tempImage.png") # we create the path for the image
    plot.savefig(imgPath,transparent=True,bbox_inches='tight') # we save the plot as a png file

    pdf.image(imgPath,x,y,w,h) # we add the image to the pdf
    os.remove(imgPath) # we delete the image file