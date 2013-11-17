from tkinter import *
import tkinter.font
import numpy, os
from datetime import date

sheeps=[]
class Application(Frame):
  def loadFromFile(self, fileName):
    try:
      fileStream = open(fileName, "r")
      global sheeps
      sheeps=[]
      for line in fileStream:
        splitedLine = line.split(";")
        sheeps.append({"number":int(splitedLine[0].strip(" ")), "weight":float(splitedLine[1].strip(" ")), "group": splitedLine[2][:-1]})
      
      fileStream.close()

    except:
      return(0)
    self.remakeListBox()
    return(1)

  def saveToFile(self, fileName):
    fileStream = open(fileName, 'w')
    for sheep in sheeps:
      fileStream.write("{0:4d};{1:10.2f};{2:s}\n".format(sheep["number"], sheep["weight"], sheep["group"]))
    fileStream.close()
    return(True)

  def addElement(self, event="some"):

    if self.group.get()!="" and self.weight.get()!="":
      sheep={"number" : self.number.get(), "weight" : float(self.weight.get()), "group" : self.group.get()}
      backupFile = open("viga.bac", "a")
      backupFile.write("{0:4d};{1:10.2f};{2:s}\n".format(sheep["number"], sheep["weight"], sheep["group"]))
      backupFile.close()
      self.listbox.insert(END, "{0:4d}{1:10.2f} {2:s}".format(sheep["number"], sheep["weight"], sheep["group"]))
      self.weight.delete(0, END)
      self.number.set(self.number.get()+1)
      sheeps.append(sheep)
      self.listbox.see(END)

  def validate(self, action, index, value_if_allowed,
    prior_value, text, validation_type, trigger_type, widget_name):
    if text in '0123456789.-+':
      try:
        float(value_if_allowed)
        return True
      except ValueError:
        if len(value_if_allowed)==0:
          return True
        else:
          return False
    else:
      if len(text)>1:
        return True
      else:
        return False

  def createScrollWidget(self):
    self.scrollFrameOuter = Frame(self)
    self.scrollFrame = Frame(self.scrollFrameOuter)
    self.scrollBar = Scrollbar(self.scrollFrame)
    self.scrollBar.pack(side=RIGHT, fill=Y)
    self.listbox = Listbox(self.scrollFrame, yscrollcommand=self.scrollBar.set, font=self.customFont)
    self.listbox.pack(side=LEFT, fill=BOTH)
    self.scrollBar.config(command=self.listbox.yview)
    self.scrollFrame.pack(anchor=N)
    self.divideButton = Button(self.scrollFrameOuter, command=self.startDivide, text="Být")
    self.divideButton.pack(anchor=S)
    self.scrollFrameOuter.pack({"side" : "left"})

  def remakeListBox(self):
    self.listbox.delete(0, END)
    backupFile = open("viga.bac", "w")
    for sheep in sheeps:
      self.listbox.insert(END, "{0:4d}{1:10.2f} {2:s}".format(sheep["number"], sheep["weight"], sheep["group"]))
      backupFile.write("{0:4d};{1:10.2f};{2:s}\n".format(sheep["number"], sheep["weight"], sheep["group"]))
      self.number.set(self.number.get()+1)
    backupFile.close()

  def createWeightWidget(self):
    self.root.bind("<Return>", self.addElement)
    self.root.bind("<KP_Enter>", self.addElement)
    self.weightFrame = Frame(self)
    self.weightText = Message(self.weightFrame, text="Vekt:")
    self.weightText.pack({"side" : "left"})
    vcmd = (self.weightFrame.register(self.validate),
        '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    self.weight = Entry(self.weightFrame, width=6, validate = 'key', validatecommand = vcmd)
    self.weight.pack({"side" : "top"})
    self.weightFrame.pack(fill=X)

  def createWidgets(self):
    self.group = StringVar()
    self.groupFrame = Frame(self)
    self.groups = Radiobutton(self.groupFrame, text="Ær", variable=self.group, value="Æ").pack(anchor=W)
    self.groups = Radiobutton(self.groupFrame, text="Gimburlamb", variable=self.group, value="G").pack(anchor=W)
    self.groups = Radiobutton(self.groupFrame, text="Veðurlamb", variable=self.group, value="V").pack(anchor=W)
    self.groupFrame.pack()
#    self.QUIT = Button(self)
#    self.QUIT["text"] = "QUIT"
#    self.QUIT["fg"]   = "red"
#    self.QUIT["command"] =  self.quit
#
#    self.QUIT.pack({"side": "left"})

    

    self.addElementButton = Button(self, text="Leg afturat")
    self.addElementButton["command"] = self.addElement

    self.addElementButton.pack({"side": "left"})

  def createNumberWidget(self):
    self.number = IntVar()
    self.number.set(1)
    self.numberFrame = Frame(self)
    self.numberText = Label(self.numberFrame, text="Nummar: ")
    self.numberText.pack({"side" : "left"})
    self.numberValue = Label(self.numberFrame, textvariable=self.number)
    self.numberValue.pack({"side" : "right"})
    self.numberFrame.pack(fill=X)

  def __init__(self, master=None):
    self.root = Tk()
    Frame.__init__(self, self.root)
    self.createMenuWidget()
    self.customFont = tkinter.font.Font(family="Courier New", size=12)
    self.createScrollWidget()
    self.createNumberWidget()
    self.createWeightWidget()
    self.createWidgets()
    self.pack()
  
  def createMenuWidget(self):
    menubar=Menu(self.root)
    fileMenu = Menu(menubar, tearoff=0)
    fileMenu.add_command(label="Opna", command=self.loadFromFileSelect)
    fileMenu.add_command(label="Goym", command=self.saveToFileSelect)
    fileMenu.add_separator()
    fileMenu.add_command(label="Lat aftur", command=self.checkIfItShouldSave)
    menubar.add_cascade(label="Skjal", menu=fileMenu)

    self.root.config(menu=menubar)

  def loadFromFileSelect(self):
    directory = os.getcwd()
    while(True):
      fb = FileBrowser(self.root, directory)
      self.root.wait_window(fb.top)
      if fb.getResponce():
        path=fb.getFilePath()
        pathSplit = path.split(".")
        if pathSplit[-1] != "mae":
          path = ".".join(pathSplit+["mae"])
        if self.loadFromFile(path):
          return
        else:
          directory=fb.getCurrentDirectory()
      else:
        return

    print(fb.getCurrentDir())

    return

  def saveToFileSelect(self):
    directory = os.getcwd()
    while(True):
      fb = FileBrowser(self.root, directory)
      self.root.wait_window(fb.top)
      if fb.getResponce():
        path=fb.getFilePath()
        pathSplit = path.split(".")
        if pathSplit[-1] != "mae":
          path = ".".join(pathSplit+["mae"])
        if self.saveToFile(path):
          return
        else:
          directory=fb.getCurrentDirectory()
      else:
        return
    return

  def startDivide(self):
    Divider(self.root)
  
  def start(self):
    try:
      backup = open('viga.bac', 'r')
      backup.close()

      popUp=PopUp(self.root, "Líkt er til at forritið ikki endaði rætt.\nSkal dataði frá seinast forritið koyrdi endurbyggjast?", 1)
      self.root.wait_window(popUp.top)

      if popUp.getResponce():
        self.loadFromFile("viga.bac")
      else:
        os.remove('viga.bac')
        backup = open('viga.bac', 'x')
        backup.close()
    except:
      backup = open('viga.bac', 'x')
      backup.close()
    self.root.protocol("WM_DELETE_WINDOW", self.checkIfItShouldSave)
    self.root.mainloop()
  def checkIfItShouldSave(self):
    popUp=PopUp(self.root, "Eru tigum vísur í at enda forritið?\nØll ógoymd data vera sletta", 1)
    self.root.wait_window(popUp.top)
    if not(popUp.getResponce()):
      return()

    os.remove("viga.bac")
    self.destroy()
    quit()

  
class Divider:
  def validate(self, action, index, value_if_allowed,
    prior_value, text, validation_type, trigger_type, widget_name):
    if text in '0123456789':
      try:
        int(value_if_allowed)
        return True
      except ValueError:
        if len(value_if_allowed)==0:
          return True
        else:
          return False
    else:
      return False

  def __init__(self, parent):
    top = self.top = Toplevel(parent)
    partsFrame = Frame(top)
    partsLabel = Label(partsFrame, text="Partar:")
    partsLabel.pack({"side" : "left"})

    vcmd = (top.register(self.validate),
        '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    self.partsVarInput = Entry(partsFrame, width=6, validate = 'key', validatecommand = vcmd)
    self.partsVarInput.pack({"side" : "left"})
    partsFrame.pack(anchor=N)
    berintsmorkLabel = Label(top, text="Skal Berintsmørk takast?")
    berintsmorkLabel.pack(anchor=N)
    self.berintsmork = IntVar()
#    self.berintsmork.set(0)
    berintsmorkFrame=Frame(top)
    self.berintsmorkRadio = Radiobutton(berintsmorkFrame, text="Nei", variable=self.berintsmork, value=0).pack({"side":"left"})
    self.berintsmorkRadio = Radiobutton(berintsmorkFrame, text="Ja", variable=self.berintsmork, value=1).pack({"side":"right"})
    berintsmorkFrame.pack(anchor=N)
    divideButton = Button(top, command=self.divide, text="být")
    divideButton.pack(anchor=S)
     

  def nestedSum(self, elementList):
    total=0
    for element in elementList:
      total+=element["weight"]
    return(total)

  def nestedStd(self, elementList):
    elements=[]
    for element in elementList:
      elements.append(element["weight"])
    return(numpy.std(elements))
    
  def divide(self):
    if self.partsVarInput.get()!="":
      parts=int(self.partsVarInput.get())
      if len(sheeps)%parts==0:
        groups=[[],[],[]]
        partsList=[None]*parts
        for sheep in sheeps:
          if sheep["group"]=="G":
            groups[1].append(sheep)
          else:
            if sheep["group"]=="V":
              groups[2].append(sheep)
            else: 
              if sheep["group"]=="Æ":
                groups[0].append(sheep)
              else:
                print(sheep)
                print("missing group")
                return
        if len(groups[0])%parts!=0:
          print("Ber ikki til at býta ædnar í " + str(parts))
          return
        if len(groups[1])%parts!=0:
          print("Ber ikki til at býta gimburlombini í " + str(parts))
          return
        if len(groups[2])%parts!=0:
          print("Ber ikki til at býta veðurlombini í " + str(parts))
          return
        groups.sort(key=len)
      NotFirstGo=False
      for group in groups:
        print(group)
        print(partsList)
        group.sort(key=lambda element: element["weight"])
        numberOfSplits=int(len(group)/parts)
        for split in range(numberOfSplits):
          if NotFirstGo:
            partsList.sort(key=self.nestedStd)
            if (numberOfSplits-split==1):
              partsList.reverse()
            partsList.sort(key=self.nestedSum)
            if split % 2 != 0:
              partsList.reverse()
              for i in range(parts):
                partsList[i].append(group.pop(0))
                print("poped: ")
                print(partsList[i][-1])
            else:
              for i in range(parts):
                partsList[i].append(group.pop())
                print("poped: ")
                print(partsList[i][-1])
          else:
            print("setting up")
            NotFirstGo=True
            for i in range(parts):
              partsList[i]=[group.pop()]
              print("poped: ")
              print(partsList[i][-1])

      print(groups)
      for i in partsList:
        print(i)
        print(self.nestedSum(i))

class FileBrowser:
  def getFilePath(self):
    return(self.pathString)
  def getCurrentDirectory(self):
    return(self.currentDirectory)
  def getResponce(self):
    return(self.responce)
  def __init__(self, parent, path):
    self.top = Toplevel(parent)
    self.browserFrame = Frame(self.top)
    self.scrollBar = Scrollbar(self.browserFrame)
    self.scrollBar.pack(side=RIGHT, fill=Y)
    self.fileListbox = Listbox(self.browserFrame, yscrollcommand=self.scrollBar.set)
    self.fileListbox.pack(side=LEFT, fill=BOTH)
    self.fileListbox.bind("<Double-Button-1>", self.chooseItem)
    self.fileListbox.bind("<<ListboxSelect>>", self.selectItem)
    self.scrollBar.config(command=self.fileListbox.yview)
    self.browserFrame.pack(anchor=N)
    self.fileFrame = Frame(self.top)
    self.fileNameStringVar = StringVar()
    self.fileNameBox = Entry(self.fileFrame, textvariable=self.fileNameStringVar)
    self.fileNameBox.pack(side="left")
    self.cancelButton=Button(self.fileFrame, command=self.top.destroy, text="Angra")
    self.cancelButton.pack(side="left")
    self.okButton=Button(self.fileFrame, command=self.chooseItem, text="Vátta")
    self.okButton.pack(side="left")
    self.fileFrame.pack(anchor=N)
    self.responce=False
    self.pathString=""
    self.currentDirectory = path
    self.openDirectory(self.currentDirectory)
  def chooseItem(self, event=None):
    if self.fileNameStringVar.get()=="..":
      self.openDirectory(os.path.dirname(self.currentDirectory))
    else:
      fullName = os.path.join(self.currentDirectory, self.fileNameStringVar.get())
      if fullName in self.directorys:
        self.openDirectory(fullName)
      else:
        self.responce=True
        self.pathString=fullName
        self.top.destroy()

  def selectItem(self, event=None):
    self.fileNameStringVar.set(self.fileListbox.get(int(self.fileListbox.curselection()[0])))

  def openDirectory(self, directory):
    self.fileNameStringVar.set("")
    self.currentDirectory = directory
    self.clearListBox()
    self.nodes = [os.path.join(directory, child) for child in os.listdir(directory)]
    self.directorys = list(filter(os.path.isdir, self.nodes))
    fileTypes = ["mae"]
    self.files = list(filter(lambda item: item.split(".")[-1] in fileTypes, list(set(self.nodes) - set(self.directorys))))
    self.addToListBox(self.directorys, self.files)
  def addToListBox(self, directorys, files):
    self.fileListbox.insert(END, "..")
    for directory in directorys:
      self.fileListbox.insert(END, os.path.basename(directory))
    for fileName in files:
      shortName = os.path.basename(fileName)
      self.fileListbox.insert(END, shortName)

  def clearListBox(self):
    self.fileListbox.delete(0, END)


class PopUp:
  
  def __init__(self, parent, message, typeOfPopUp):
    self.top = Toplevel(parent)
    self.responce=False
    self.PopUpFrame = Frame(self.top)
    self.messageLabel = Label(self.PopUpFrame, text=message)
    self.messageLabel.pack()
    self.buttonFrame=Frame(self.top)
    if (typeOfPopUp==1):
      self.cancelButton=Button(self.buttonFrame, command=self.top.destroy, text="Angra")
      self.cancelButton.pack(side="left")
    self.okButton=Button(self.buttonFrame, command=self.acceptResponce, text="Vátta")
    self.okButton.pack(side="left")
    self.PopUpFrame.pack()
    self.buttonFrame.pack()

    
  def getResponce(self):
    return(self.responce)
  def acceptResponce(self):
    self.responce=True
    self.top.destroy()




#root = Tk()
#fb=FileBrowser(root)
#fileBrowser = fb.openDirectory("/home/trndr/projects")
#root.mainloop()

Application().start()
print(sheeps)
