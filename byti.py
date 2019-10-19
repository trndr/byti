#!/usr/bin/env python3
from tkinter import *
import tkinter.font
import os, sys
import datetime
import math

#TODO Brundir

class Sheep:
    def __init__(self):
        self.sheep=[]
    def add(self,sheep):
        self.sheep.append(sheep)
    def load_from_file(self,filename):
        self.sheep=[]
        with open(filename) as f:
            lines=f.readlines()
            for line in lines:
                if line != "":
                    number,weight,group=line.split(";")
                    self.add({"number":int(number.strip()),"weight":float(weight.strip()),"group":group.strip()})
    def save_to_file(self,filename):
        with open(filename,"w") as f:
            for sheep in self.sheep:
                f.write("{0:4d};{1:10.2f};{2:s}\n".format(sheep["number"], sheep["weight"], sheep["group"]))
    def get_sheep(self,index):
        return self.sheep[index]
    def update_sheep(self,index,properties):
        self.sheep[index]=properties
    def get_highies_number(self):
        return max(map(lambda x:x["number"],self.sheep))
    def get_count(self):
        return len(list(filter(lambda x: x["group"] in ["V","G","AE"],self.sheep)))
    def get_mean_weight(self):
        interesting=list(filter(lambda x: x["group"] in ["V","G","AE"],self.sheep))
        if len(interesting)>0:
            return float(sum(list(map(lambda x:x["weight"], interesting))))/len(interesting)
        else:
            return 0
    def get_full_count(self):
        return(len(self.sheep))
    def get_full_mean_weight(self):
        if self.get_full_count()>0:
            return sum(map(lambda x:x["weight"],self.sheep))/get_full_count()
        else:
            return 0
    def equivalent_weight(self, weight, typeFrom, typeTo):
        if (typeFrom=="AE"):
            if (typeTo=="G"):
                return(weight)
            else:
                return(weight)
        if (typeFrom=="G"):
            if (typeTo=="V"):
                return(weight)
            else:
                return(weight)
        if (typeFrom=="V"):
            if (typeTo=="G"):
                return(weight)
            else:
                return(weight)
    def find_closest_to(self, weight, group):
        i=0
        differenceLast=abs(weight-group[i]["weight"])
        while (i<len(group)-1):
            difference=abs(weight-group[i+1]["weight"])
            if difference>differenceLast:
                return(i)
            differenceLast=difference
            i+=1
        return(len(group)-1)
    def get_parts(self,number_of_parts,berintsmork=False):
        groups_to_divide=[[],[],[]]
        groups_to_divide[0]=list(filter(lambda x:x["group"]=="AE",self.sheep))
        groups_to_divide[1]=list(filter(lambda x:x["group"]=="G",self.sheep))
        groups_to_divide[2]=list(filter(lambda x:x["group"]=="V",self.sheep))
        parts=[]
        ignored=list(filter(lambda x:x["group"]=="IB",self.sheep))
        brundir=list(filter(lambda x:x["group"]=="BR",self.sheep))
        #print(groups_to_divide,brundir,ignored)
        for i in range(number_of_parts):
            parts.append(Part("Partur nummar "+str(i+1)))

        partBerintmork=Part("Berintsmørk")
        if berintsmork:
            for group in groups_to_divide:
                group.sort(key=lambda element: element["weight"])
            for i in range(12):
                closest=self.find_closest_to(self.get_mean_weight(), groups_to_divide[2])
                partBerintmork.add(groups_to_divide[2].pop(closest))

        groups_to_divide.sort(key=len)
        for group in groups_to_divide:
            group.sort(key=lambda element: element["weight"])
#            if len(group)>0:
#                print(group[0]["group"]+str(sum(map(lambda x:x["weight"], group))/len(group)))

        NotFirstGo=False
        for group in groups_to_divide:
            if len(group)>0:
                groupType=group[0]["group"]
            averageWeight=-1
            numberOfSplits=math.ceil(len(group)/number_of_parts)
            for split in range(numberOfSplits):
                parts.sort(key=lambda part:part.calculationWeight)
                if(split%2==0):
                    parts.reverse()
                group.reverse()
                for i in range(number_of_parts):
                    try:
                        parts[i].add(group.pop())
                    except IndexError as e:
                        if averageWeight==-1:
                            averageWeight=sum(list(map(lambda x:x.calculationWeight,parts[:i])))/float(i)
                        missingWeight=averageWeight-parts[i].calculationWeight
                        equivalentWeight=self.equivalent_weight(missingWeight, groupType, groups_to_divide[2][0]["group"])
                        closest=self.find_closest_to(equivalentWeight, groups_to_divide[2])
                        calWeight=self.equivalent_weight(groups_to_divide[2][closest]["weight"], groups_to_divide[2][0]["group"],group)
                        parts[i].add(groups_to_divide[2].pop(closest), calWeight)
        if berintsmork:
            parts.append(partBerintmork)
        return parts,brundir,ignored


class Application(Frame):
    def loadFromFile(self, fileName):
        try:
            self.known_sheep.load_from_file(fileName)

        except Exception as e:
            print(e)
            return(0)
        self.remakeListBox()
        return(1)

    def saveToFile(self, fileName):
        self.known_sheep.save_to_file(fileName)
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
            self.known_sheep.add(sheep)
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


    def listSelect(self, event):
        w=event.widget
        try:
            self.currentlySelected=int(w.curselection()[0])
        except:
            pass
    def correct(self):
        if self.currentlySelected>=0:
            correction=Correction(self.root, self.known_sheep.get_sheep(self.currentlySelected))
            self.root.wait_window(correction.top)
            responce=correction.getResponce()
            if responce[0]:
                #print(responce)
                self.known_sheep.update_sheep(self.currentlySelected,responce[1])
                self.remakeListBox()
#        else:
#            print(self.currentlySelected)

    def createScrollWidget(self):
        self.scrollFrameOuter = Frame(self)
        self.scrollFrame = Frame(self.scrollFrameOuter)
        self.scrollBar = Scrollbar(self.scrollFrame)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.scrollFrame, yscrollcommand=self.scrollBar.set, font=self.customFont)
        self.listbox.bind("<<ListboxSelect>>", self.listSelect)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollBar.config(command=self.listbox.yview)
        self.scrollFrame.pack(anchor=N, expand=True, fill=BOTH)
        self.divideButton = Button(self.scrollFrameOuter, command=self.startDivide, text="Být")
        self.divideButton.pack(anchor=S)
        self.scrollFrameOuter.pack({"side" : "left"}, expand=True, fill=BOTH)
    def remakeListBox(self):
        self.listbox.delete(0, END)
        self.number.set(0)
        backupFile = open("viga.bac", "w")
        for sheep in self.known_sheep.sheep:
            self.listbox.insert(END, "{0:4d}{1:10.2f} {2:s}".format(sheep["number"], sheep["weight"], sheep["group"]))
            backupFile.write("{0:4d};{1:10.2f};{2:s}\n".format(sheep["number"], sheep["weight"], sheep["group"]))
        self.number.set(self.known_sheep.get_highies_number()+1)
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
        self.groups = Radiobutton(self.groupFrame, text="Ær", variable=self.group, value="AE").pack(anchor=W)
        self.groups = Radiobutton(self.groupFrame, text="Gimburlamb", variable=self.group, value="G").pack(anchor=W)
        self.groups = Radiobutton(self.groupFrame, text="Veðurlamb", variable=self.group, value="V").pack(anchor=W)
        self.groupFrame.pack(anchor=N)
        
        self.buttonFrame=Frame(self)
        self.addElementButton = Button(self.buttonFrame, text="Leg afturat")
        self.addElementButton["command"] = self.addElement

        self.addElementButton.pack({"side": "left"})
        self.correctionButton = Button(self.buttonFrame, text="Rætta")
        self.correctionButton["command"]=self.correct
        self.correctionButton.pack({"side":"left"})
        self.buttonFrame.pack(anchor=N)

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
        self.currentlySelected=-1
        self.createMenuWidget()
        self.customFont = tkinter.font.Font(family="Courier New", size=12)
        self.createScrollWidget()
        self.createNumberWidget()
        self.createWeightWidget()
        self.createWidgets()
        self.pack(expand=1, fill=BOTH)
        self.hasCloseOpen=False
        self.known_sheep=Sheep()
    
    def createMenuWidget(self):
        menubar=Menu(self.root)
        fileMenu = Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Opna", command=self.loadFromFileSelect)
        fileMenu.add_command(label="Goym", command=self.saveToFileSelect)
        fileMenu.add_separator()
        fileMenu.add_command(label="Lat aftur", command=self.checkIfItShouldSave)
        menubar.add_cascade(label="Skjal", menu=fileMenu)
        toolsMenu = Menu(menubar, tearoff=0)
        toolsMenu.add_command(label="Statstik", command=self.generateStatics)
        menubar.add_cascade(label="Amboð", menu=toolsMenu)

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
        return
    #TODO Fix
    def generateStatics(self):
        return
        groups=[]
        groups.append(list(map(lambda x:x["weight"],filter(lambda x:x["group"]=="V",sheeps))))
        groups.append(list(map(lambda x:x["weight"],filter(lambda x:x["group"]=="G",sheeps))))
        groups.append(list(map(lambda x:x["weight"],filter(lambda x:x["group"]=="AE",sheeps))))
        groups.append(list(map(lambda x:x["weight"],filter(lambda x:x["group"]=="BR",sheeps))))
        groups.append(list(map(lambda x:x["weight"],filter(lambda x:x["group"]=="IB",sheeps))))
        minimumWeight=99999
        maximumWeight=0
        for group in groups:
            if len(group)>0:
                groupMinimumWeight=min(group)
                groupMaximumWeight=max(group)
                if groupMinimumWeight<minimumWeight:
                    minimumWeight=groupMinimumWeight
                if groupMaximumWeight>maximumWeight:
                    maximumWeight=groupMaximumWeight
        bucketListLength=int(maximumWeight-minimumWeight)+1
        groupNames=["Veðurlomb", "Gimburlomb", "Ær", "Brundir", "Ikki í býti"]
        i=0
        for group in range(len(groups)):
            if (len(groups[group])<=0):
                continue
            bucketList=[0]*bucketListLength
            for sheep in groups[group]:
                bucketList[int(sheep-minimumWeight)]+=1
            #print(len(groups[group]))
            size=0.8
            c.drawString(0.6*cm, (27-i*size)*cm, groupNames[group])
            i+=1
            c.drawString(0.6*cm, (27-i*size)*cm, str(bucketList))
            i+=1
            if group!=3:
                #midalvekt
                c.drawString(0.6*cm, (27-i*size)*cm, str(sum(groups[group])/len(groups[group])))
            else:
                #midalvekt; alt við hornum
                c.drawString(0.6*cm, (27-i*size)*cm, str(sum((groups[0]+groups[group]))/(len(groups[0])+len(groups[group]))))
            i+=2
        c.showPage()
        c.save()


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
        Divider(self.root,self.known_sheep)
    
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
        if not(self.hasCloseOpen):
            self.hasCloseOpen=True
            popUp=PopUp(self.root, "Eru tigum vísur í at enda forritið?\nØll ógoymd data vera sletta", 1)
            self.root.wait_window(popUp.top)
            if not(popUp.getResponce()):
                self.hasCloseOpen=False
                return()

            os.remove("viga.bac")
            self.root.destroy()
            #quit()
            sys.exit()

class Part:
    def __init__(self, name):
        self.sheepList=[]
        self.calculationWeight=0
        self.realWeight=0
        self.partName=name
    def add(self, sheep, weight=None):
        self.sheepList.append(sheep)
        if weight==None:
            self.calculationWeight+=sheep["weight"]
        else:
            self.calculationWeight+=weight
        self.realWeight+=sheep["weight"]
    def setPartName(self, name):
        self.partName=name
    def getSheep(self):
        return(self.sheepList)
    def getStats(self):
        return(len(list(filter(lambda x:x["group"]=="AE",self.sheepList)))
              ,len(list(filter(lambda x:x["group"]=="G",self.sheepList)))
              ,len(list(filter(lambda x:x["group"]=="V",self.sheepList)))
              ,self.realWeight)
    def getPrittySheep(self):
        sheepList=[self.partName+" sortera","eftir vekt"]
        sheepList.append(" Nr      Vekt ")
        self.sheepList.sort(key=lambda x:-x["weight"])
        sheepList+=list(map(lambda x:"{0:4d}{1:10.0f} {2:s}".format(x["number"], x["weight"], x["group"]), self.sheepList))
        self.sheepList.sort(key=lambda x:x["number"])
        sheepList.append("")
        sheepList.append(self.partName+" sortera")
        sheepList.append("eftir nummar")
        sheepList.append(" Nr      Vekt ")
        sheepList+=list(map(lambda x:"{0:4d}{1:10.0f} {2:s}".format(x["number"], x["weight"], x["group"]), self.sheepList))

        sheepList.append("")
        sheepList.append("Total vekt "+str(int(self.realWeight)))
        return(sheepList)
    def getPartName(self):
        return(self.partName)
    
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

    def __init__(self, parent,known_sheep):
        top = self.top = Toplevel(parent)
        self.top.transient(parent)
        self.parent=(parent)
        self.known_sheep=known_sheep
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
        berintsmorkFrame=Frame(top)
        self.berintsmorkRadio = Radiobutton(berintsmorkFrame, text="Nei", variable=self.berintsmork, value=0).pack({"side":"left"})
        self.berintsmorkRadio = Radiobutton(berintsmorkFrame, text="Ja", variable=self.berintsmork, value=1).pack({"side":"right"})
        berintsmorkFrame.pack(anchor=N)
        divideButton = Button(top, command=self.divide, text="být")
        divideButton.pack(anchor=S)
        self.top.grab_set()
        self.top.protocol("WM_DELETE_WINDOW", self.cancel)
    def cancel(self, event=None):
        self.parent.focus_set()
        self.top.destroy()
          
    def divide(self):
        if self.partsVarInput.get()!="":
            parts=int(self.partsVarInput.get())

            totalSheep=self.known_sheep.get_count()
            if (totalSheep%parts==0 or (self.berintsmork.get()==1 and (totalSheep-12)%parts==0)):
                partsList,brundir,ignored=self.known_sheep.get_parts(parts,self.berintsmork.get()==1)
                htmlPrinter=HTMLPrinter()

                for i in range(len(partsList)):
                    popUp=htmlPrinter.add_part(partsList[i].getPrittySheep())
                brundirPrint=list(map(lambda x:"{0:4d}{1:10.0f} {2:s}".format(x["number"], x["weight"], x["group"]), brundir))
                for i in range(int((len(brundir)+1)/2)):
                    currentPrintList=brundirPrint[i*2:i*2+2]
#                    for j in range(17):
#                        currentPrintList.insert(1,"")
                    block_space=7
                    if len(currentPrintList)==2:
                        currentPrintList=["Brundur"]+[currentPrintList[0]]+[""]*block_space+["Brundur"]+[currentPrintList[1]]+[""]*block_space
                    else:
                        currentPrintList=["Brundur"]+[currentPrintList[0]]+[""]*(block_space*2+2)
                    popUp=htmlPrinter.add_part(currentPrintList)
                for i in range(len(brundirPrint)-1,0,-1):
                    brundirPrint.insert(i,"")
                popUp=htmlPrinter.add_part(["Brundir"]+brundirPrint)

                ignoredPrint=list(map(lambda x:"{0:4d}{1:10.0f} {2:s}".format(x["number"], x["weight"], x["group"]), ignored))
#                for i in range(len(brundirPrint)-1,0,-1):
#                    brundirPrint.insert(i,"")
                popUp=htmlPrinter.add_part(ignoredPrint)
                with open(str(datetime.datetime.utcnow())[:-7].replace(":","-")+".html","w") as f:
                    f.write(htmlPrinter.get_html())

                fileStream = open("byti.txt", 'w')
                for part in partsList:
                    for sheep in part.sheepList:
                        fileStream.write("{0:4d};{1:10.2f};{2:s};{3:s}\n".format(sheep["number"], sheep["weight"], sheep["group"], part.partName))
                fileStream.close()

                self.outPutText=""
                if (self.berintsmork.get()==1):
                    self.outPutText+="Býti er liðugt, tikin vóru "+str((totalSheep-12)/parts)+"\nMiðalvektin var "+str(self.known_sheep.get_mean_weight())
                else:
                    self.outPutText+="Býti er liðugt, tikin vóru "+str(totalSheep/parts)+"\nMiðalvektin var "+str(self.known_sheep.get_mean_weight())
                self.outPutText+="\n"
                for i in partsList:
                    stats=i.getStats()
                    self.outPutText+="{0:s} fekk {1:4d} Ær {2:4d} Gimburlomb {3:4d} Veðurlomb total vekt {4:6f}\n".format(i.getPartName(), stats[0], stats[1], stats[2], stats[3])
                popUp=PopUp(self.top, self.outPutText, 0)
                self.top.wait_window(popUp.top)
            else:
                if (self.berintsmork.get()==1):
                    popUp=PopUp(self.top, str(parts)+" gongur ikki upp í "+str(totalSheep)+" -12 (berintsmørk)"+"\n"+str((totalSheep-12)%parts), 0)
                else:
                    popUp=PopUp(self.top, str(parts)+" gongur ikki upp í "+str(totalSheep), 0)
                self.top.wait_window(popUp.top)

class FileBrowser:
    def getFilePath(self):
        return(self.pathString)
    def getCurrentDirectory(self):
        return(self.currentDirectory)
    def getResponce(self):
        return(self.responce)
    def __init__(self, parent, path):
        self.top = Toplevel(parent)
        self.top.transient(parent)
        self.parent=(parent)
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
        self.cancelButton=Button(self.fileFrame, command=self.cancel, text="Angra")
        self.cancelButton.pack(side="left")
        self.okButton=Button(self.fileFrame, command=self.chooseItem, text="Vátta")
        self.okButton.pack(side="left")
        self.fileFrame.pack(anchor=N)
        self.responce=False
        self.pathString=""
        self.currentDirectory = path
        self.openDirectory(self.currentDirectory)

        self.top.grab_set()
        self.top.protocol("WM_DELETE_WINDOW", self.cancel)

    def cancel(self, event=None):
        self.parent.focus_set()
        self.top.destroy()
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
                self.cancel()

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

class HTMLPrinter:
    def __init__(self):
        self.svgs=[]
    def add_part(self,part):
        text="""<svg viewBox="0 0 250 {}" xmlns="http://www.w3.org/2000/svg" font-family="monospace" font-size="20" xml:space="preserve" style="height: 100%;width: 100%;">\n""".format(29+18*len(part))
        for line in range(len(part)):
            text+="<text x=\"{}\" y=\"{}\">{}</text>".format(0,20+18*line,part[line])
        text+="</svg>"
        self.svgs.append(text)
    def get_html(self):
        return """<html><body>"""+"".join(self.svgs)+"</body></html>"

class Correction:
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
    
    def __init__(self, parent, selected):
        self.top = Toplevel(parent)
        self.top.transient(parent)
        self.parent=(parent)
        self.responce=(False, 0)
        self.CorrectionFrame = Frame(self.top)
        self.number=selected["number"]
        self.numberLabel = Label(self.CorrectionFrame, text="Nummar: "+str(selected["number"]))
        self.numberLabel.pack({"side":"left"})
        self.CorrectionFrame.pack(fill=X)

        self.weightFrame = Frame(self.top)
        self.weightText = Message(self.weightFrame, text="Vekt:")
        self.weightText.pack({"side" : "left"})
        vcmd = (self.weightFrame.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.weight = Entry(self.weightFrame, width=6, validate = 'key', validatecommand = vcmd)
        self.weight.pack({"side" : "top"})
        self.weightFrame.pack(fill=X)
        self.weight.insert(0,str(int(selected["weight"])))
        self.group = StringVar()
        self.groupFrame = Frame(self.top)
        self.groups = Radiobutton(self.groupFrame, text="Ær", variable=self.group, value="AE").pack(anchor=W)
        self.groups = Radiobutton(self.groupFrame, text="Gimburlamb", variable=self.group, value="G").pack(anchor=W)
        self.groups = Radiobutton(self.groupFrame, text="Veðurlamb", variable=self.group, value="V").pack(anchor=W)
        self.groups = Radiobutton(self.groupFrame, text="Brundur", variable=self.group, value="BR").pack(anchor=W)
        self.groups = Radiobutton(self.groupFrame, text="Ikki í býti", variable=self.group, value="IB").pack(anchor=W)
        self.group.set(selected["group"])
        self.groupFrame.pack()
        self.buttonFrame=Frame(self.top)
        self.cancelButton=Button(self.buttonFrame, command=self.top.destroy, text="Angra")
        self.cancelButton.pack(side="left")
        self.okButton=Button(self.buttonFrame, command=self.acceptResponce, text="Vátta")
        self.okButton.pack(side="left")
        self.buttonFrame.pack()
        self.top.grab_set()
        self.top.protocol("WM_DELETE_WINDOW", self.cancel)
        self.top.focus_set()

    def cancel(self, event=None):
        self.parent.focus_set()
        self.top.destroy()
    def getResponce(self):
        return(self.responce)
    def acceptResponce(self):
        self.responce=(True,{"number" : self.number, "weight" : float(self.weight.get()), "group" : self.group.get()})
        self.cancel()
        

class PopUp:
    
    def __init__(self, parent, message, typeOfPopUp):
        self.top = Toplevel(parent)
        self.top.transient(parent)
        self.parent=(parent)
        self.responce=False
        self.PopUpFrame = Frame(self.top)

        self.messageLabel = Label(self.PopUpFrame, text=message)
        self.messageLabel.pack()
        self.buttonFrame=Frame(self.top)
        if (typeOfPopUp==1):
            self.cancelButton=Button(self.buttonFrame, command=self.cancel, text="Angra")
            self.cancelButton.pack(side="left")
        self.okButton=Button(self.buttonFrame, command=self.acceptResponce, text="Vátta")
        self.okButton.pack(side="left")
        self.PopUpFrame.pack()
        self.buttonFrame.pack()
        self.top.grab_set()
        self.top.protocol("WM_DELETE_WINDOW", self.cancel)

    def cancel(self, event=None):
        self.parent.focus_set()
        self.top.destroy()
        
    def getResponce(self):
        return(self.responce)
    def acceptResponce(self):
        self.responce=True
        self.cancel()
if __name__=="__main__":
    app=Application().start()
