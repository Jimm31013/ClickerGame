"""
Quirky lil clicker game using Tk. Just felt like messing around with it.
Author: Jimmy Parkins
Date: 2025-03-04
"""
#Imports
from tkinter import *
from tkinter import ttk
import json
import os

#######################MAIN SCREEN ESTABLISHMENT######################################
root = Tk()

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

root.geometry(f"{screenWidth}x{screenHeight}")
root.title("Jimmy's Button Clicker")
######################################################################################

####################### GLOBAL VARIABLE DECLARATION#################################### 
number = 0
autoClickerCount = 0
autoClickerPrice = 10  
autoClickerUpgradePrice = 100
autoClickerUpgradeCount = 1
autoClickerTimer = 0xffff
clickerUpgradeCount = 1
clickerUpgradePrice = 1000
FINALGOAL = 10000
progressToFinish = (number / FINALGOAL) * 100
FINALGOALHIT = FALSE

gameDirectory = os.path.dirname(__file__)
saveFilePath = os.path.join(gameDirectory, "saveGame.json")

########################################################################################

# Loads savegame information from json file. bet youre pretty glad this is here eh?
def loadGame():
    global number, autoClickerCount, autoClickerPrice, autoClickerUpgradePrice, autoClickerUpgradeCount, autoClickerTimer, clickerUpgradeCount, clickerUpgradePrice
    try:
        with open(saveFilePath, "r") as saveFile:
            gameSave = json.load(saveFile)
            number = gameSave["number"]
            autoClickerCount = gameSave["autoClickerCount"]
            autoClickerPrice = gameSave["autoClickerPrice"]
            autoClickerUpgradePrice = gameSave["autoClickerUpgradePrice"]
            autoClickerUpgradeCount = gameSave["autoClickerUpgradeCount"]
            autoClickerTimer = gameSave["autoClickerTimer"]
            clickerUpgradeCount = gameSave["clickerUpgradeCount"]
            clickerUpgradePrice = gameSave["clickerUpgradePrice"]
    except FileNotFoundError or KeyError:
        pass
    updateInfo()

# Saves current game data to hidden mystery totally secure json file that cannot be modified or cracked at all
def saveGame():
    gameSave = {
        "number": number,
        "autoClickerCount": autoClickerCount,
        "autoClickerPrice": autoClickerPrice,
        "autoClickerUpgradePrice": autoClickerUpgradePrice,
        "autoClickerUpgradeCount": autoClickerUpgradeCount,
        "autoClickerTimer": autoClickerTimer,
        "clickerUpgradeCount": clickerUpgradeCount,
        "clickerUpgradePrice": clickerUpgradePrice
    }
    with open(saveFilePath, "w") as saveFile:
        json.dump(gameSave, saveFile)
    
# Wipes all the game data clean in the hidden mystery totally secure json file
def resetGame():
    newGame= {
        "number" : 0,
        "autoClickerCount": 0,
        "autoClickerPrice": 10,
        "autoClickerUpgradePrice": 100,
        "autoClickerUpgradeCount": 1,
        "autoClickerTimer": 0xffff,
        "clickerUpgradeCount": 1,
        "clickerUpgradePrice": 1000

    }
    with open(saveFilePath, "w") as saveFile:
        json.dump(newGame, saveFile)
    
    root.quit()

# Handles the user wishing to reset to play this game.. again? Why they would want to do that? I dont know. But its here if they want it.
def resetButton():
    resetScreen = Tk()
    resetScreen.geometry(f"{screenWidth}x{screenHeight}")
    resetScreen.title("ARE YOU SURE?")

    yesButton = Button(resetScreen,text="Yes I'm sure", padx=50, pady=50, bg="grey", font=("Arial, 22"), command=resetGame)
    noButton = Button(resetScreen, text= "No, go back",padx=50, pady=50, bg="grey", font=("Arial, 22"), command=resetScreen.destroy)
    resetDesc = Label(resetScreen, text="ARE YOU SURE YOU WANT TO RESTART? Im too lazy to code a backup so you really cant go back", font=("Arial, 20"), fg="red", pady=20)

    resetDesc.pack()
    noButton.pack()
    yesButton.pack()

def exitButton():
    saveGame()
    root.quit()

# The keystone of the entire game.... the click button. 
def ClickMainButton():
    global number, clickerUpgradeCount
    number += clickerUpgradeCount

    updateInfo()
    

# Handles buying the autoclicker. Innapropriately named, but so was James and we just pretend thats not my name
def autoClick():
    global autoClickerCount, number, autoClickerPrice
    if number < autoClickerPrice:
        AutoClickerLabel["text"] = "YOU DO NOT HAVE ENOUGH TO BUY AUTOCLICKER"

    else:
        autoClickerCount += 1
        number -= autoClickerPrice
        autoClickerPrice += 2 ** autoClickerCount
        updateInfo()

# Updates all the info on screen, all at once! (very innefficient?)
def updateInfo():
    global number, autoClickerCount, clickerUpgradeCount, FINALGOALHIT
    AutoClickerLabel["text"] = ""
    ShowInfo["text"] = "You Currently have  " + str(number) + " bits."
    AutoClickerPriceLabel["text"] = f"Cost: {autoClickerPrice} bits | Current: {autoClickerCount}"  
    AutoClickerUpgradePriceLabel["text"] = f"Cost: {autoClickerUpgradePrice} bits | Current: {autoClickerUpgradeCount}"  
    ClickerUpgradePriceLabel["text"] = f"Cost: {clickerUpgradePrice} bits | Current: {clickerUpgradeCount}"
    progressToFinish = (number / FINALGOAL) * 100
    ProgressBar["value"] = progressToFinish
    ProgressBarLabel["text"] = f"PROGRESS TO FINISH: {progressToFinish:.2f}%"
    
    # Fancy lil label change depending on availabilty for purchase
    if number < autoClickerUpgradePrice:
        AutoClickerUpgrade.config(bg="grey")
    else:
        AutoClickerUpgrade.config(bg="green")
    if number < autoClickerPrice:
        AutoClickerPurchase.config(bg="grey")
    else:
        AutoClickerPurchase.config(bg="green")

    if number < clickerUpgradePrice:
        ClickUpgrade.config(bg="grey")
    else:
        ClickUpgrade.config(bg="green")

    if progressToFinish >= 100:
        FINALGOALHIT = True

    if FINALGOALHIT:
        number = 0
        autoClickerCount = 0
        clickerUpgradeCount = 0
        AutoClickerLabel["text"] = "CONGRATULATIONS! YOU FINISHED!!! GO OUTSIDE!!! (or reset?)"


        
    

# Handles the autoclicker loop
def autoLoop():
    global number, autoClickerCount, autoClickerUpgradeCount
    number += autoClickerCount * autoClickerUpgradeCount
    updateInfo()
    root.after(1000, autoLoop)

# Handles the autoclicker upgrade
def autoClickUpgrade():
    global number, autoClickerUpgradePrice, autoClickerUpgradeCount
    if number < autoClickerUpgradePrice:
        AutoClickerLabel["text"] = "YOU DO NOT HAVE ENOUGH TO UPGRADE AUTOCLICKER"

    else:
        autoClickerUpgradeCount += 1
        number -= autoClickerUpgradePrice
        autoClickerUpgradePrice += 3 ** autoClickerUpgradeCount
        updateInfo()

# Handles upgrading the clicker button    
def clickerUpgrade():
    global number, clickerUpgradeCount, clickerUpgradePrice
    if number < clickerUpgradePrice:
        AutoClickerLabel["text"] = "YOU DO NOT HAVE ENOUGH TO UPGRADE CLICKER"
    else:
        clickerUpgradeCount += 1
        number -= clickerUpgradePrice
        clickerUpgradePrice = (clickerUpgradeCount ** 2) * 10 + clickerUpgradePrice
        updateInfo()  

# Establishes all UI Objects
ClickingButton = Button(root,text="Click Me!", padx=50, pady=50, bg="gold", font=("Arial, 22"), command=ClickMainButton)
ShowInfo = Label(root, text="Welcome to the Bit clicker! Click to start!", font=("Arial, 20"), fg="purple", pady=20)
AutoClickerLabel = Label(root, text="",font=("Arial, 20"), fg="purple",pady=10)
AutoClickerPurchase = Button(root, text="Buy autoclicker", padx=50,pady=10, bg="green", font=("Arial, 12"),command=autoClick)
AutoClickerUpgrade = Button(root, text="Upgrade autoclicker", padx=50,pady=10, bg="green", font=("Arial, 12"),command=autoClickUpgrade)
ClickUpgrade = Button(root, text="Upgrade Clicker Button", padx=50, pady=10, bg="grey", font=("Arial, 12"),command=clickerUpgrade)
AutoClickerPriceLabel = Label(root,text=f"Cost: {autoClickerPrice} bits | Current: {autoClickerCount}", font="Arial, 12", fg="blue")
AutoClickerUpgradePriceLabel = Label(root,text=f"Cost: {autoClickerUpgradePrice} bits | Current: {autoClickerUpgradeCount}", font="Arial, 12", fg="blue")
ClickerUpgradePriceLabel = Label(root,text=f"Cost: {clickerUpgradePrice} bits | Current: {clickerUpgradeCount}", font="Arial, 12", fg="blue")
ProgressBar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
ProgressBarLabel = Label(root, text=f"PROGRESS TO FINISH: %{progressToFinish:.2f}%", font= "Arial, 12", fg="black" )

# Exit button also saves game. Pretty neat.
ExitButton = Button(root, text="Exit", padx=10,pady=10, bg="red", font=("Arial, 10"),command=exitButton)
ResetButton = Button(root, text="Reset Game", padx=10,pady=10, bg="red", font=("Arial, 10"),command=resetButton)

# Packs all the buttons and labels, dont touch this. Pain in the ass
ShowInfo.pack(side=TOP)
AutoClickerLabel.pack(side=TOP)
ClickingButton.pack(side=TOP)
AutoClickerPurchase.pack(side=TOP, anchor=W)
AutoClickerPriceLabel.pack(side=TOP, anchor=W)  
AutoClickerUpgrade.pack(side=TOP, anchor=W)
AutoClickerUpgradePriceLabel.pack(side=TOP, anchor=W)  
ClickUpgrade.pack(side=TOP, anchor=W)
ClickerUpgradePriceLabel.pack(side=TOP, anchor=W) 
ProgressBarLabel.pack(side=TOP)
ProgressBar.pack(side=TOP)
ExitButton.pack(side=BOTTOM, anchor=E)
ResetButton.pack(side=BOTTOM, anchor=E)

# Load game saveData if any
loadGame()

# Updates all info on the screen
updateInfo()

# Ensures the game is saved when user presses the x at teh top of the window
root.protocol("WM_DELETE_WINDOW", exitButton)

autoLoop()

# Return to mainloop start
root.mainloop()