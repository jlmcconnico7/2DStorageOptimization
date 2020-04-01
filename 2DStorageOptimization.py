#

from tkinter import filedialog
from tkinter import *
import csv


class BoxPacker:
#this code creates a class titled BoxPacker

    def __init__(self, win):
        self.rootWind = win

        self.BoxesFileLabel = Label(win, text="Boxes File:")
        self.BoxesFileLabel.grid(row=0)
        #Creates Label titled "Boxes File:"
        
        self.FileNameEntry = Entry(win, width=75)
        self.FileNameEntry.insert(0,"...")
        self.FileNameEntry.config(state="readonly")
        self.FileNameEntry.grid(row=0, column=1, columnspan=2)
        #Creates Entry with "..." to display the file name selected by user
        
        self.SelectButton = Button(win, text="Select File", command=self.openFileClicked)
        self.SelectButton.grid(row=0, column=3, padx=2)
        #Creates Button titled "Select File" that calls openFileClicked
        #method when it is clicked. Allows user to select file.

        self.TruckDimsLabel = Label(win, text="Truck Dimensions")
        self.TruckDimsLabel.grid(row=1, column=1, sticky=W)
        #Creates Label titled "Truck Dimensions".
        
        self.WidthLabel = Label(win, text="Width:")
        self.WidthLabel.grid(row=2, column=0, sticky=E)
        #Creates Label titled "Width:".

        self.WidthEntry = Entry(win)
        self.WidthEntry.grid(row=2, column=1, sticky=W)
        #Creates Entry that allows user to enter their desired width.

        self.LengthLabel = Label(win, text="Length:")
        self.LengthLabel.grid(row=3, column=0, sticky=E)
        #Creates Label titled "Length:".

        self.LengthEntry = Entry(win)
        self.LengthEntry.grid(row=3, column=1, sticky=W)
        #Creates Entry that allows user to enter their desired length.

        self.PackAlgLabel = Label(win, text="Packing Algorithm")
        self.PackAlgLabel.grid(row=1, column=2)
        #Creates Label titled "Packing Algorithm".

        self.var = IntVar()
        #Helps relate radiobuttons with values

        rb1 = Radiobutton(win, text="Largest Box First", variable=self.var, value=1)
        rb1.grid(row=2, column=2)
        #Creates a radio button that allows user to select "Largest Box First".

        rb2 = Radiobutton(win, text="Smallest Box First", variable=self.var, value=2)
        rb2.grid(row=3, column=2)
        #Creates a radio button that allows user to select "Smallest Box First".

        self.saveButton = Button(win, text="Pack Boxes & Save Results", width=85, command=self.packNSaveClicked)
        self.saveButton.grid(row=4, columnspan=4, sticky=E+W)
        #Creates Button that allows user to pack the boxes and save the results.
        #It calls the packNSaveClicked method when the button is clicked.
    #This method creates a GUI. It organizes different labels, buttons, and
    #entry boxes in a grid inside the GUI window to obtain user input.

    def openFileClicked(self):
        self.fileName = filedialog.askopenfilename()
        self.FileNameEntry.config(state=NORMAL)
        self.FileNameEntry.delete(0,END)
        self.FileNameEntry.insert(0,str(self.fileName))
        if self.FileNameEntry.get() == "":
            self.FileNameEntry.insert(0, "...")
        self.FileNameEntry.config(state="readonly")
    #This method asks the user to select a file for input. The file is then
    #read and its name is inserted into the FileNameEntry box.

    def readBoxesFile(self):
        try:
            f = open(self.fileName)
            self.boxes = csv.reader(f)
            self.listOfData = []
            for line in self.boxes:
                if len(line) != 3:
                    raise ValueError
                else:
                    line[1] = int(line[1])
                    line[2] = int(line[2])
                    self.listOfData.append(line)
            f.close()
        except:
           raise ValueError
    #This method reads the user's selcted file as a CSV. It appends the
    #2nd and the 3rd parts of the file into the listOfData list.

    def isValidLocation(self, row, column, width, length):
        for R in range(row, row+length):
            for C in range(column, column+width):
                if R >= len(self.truck) or C >= len(self.truck[0]):
                    return False
                if self.truck[R][C] != "":
                    return False
        return True
    #This method determines if the length and width of a box can fit inside
    #the given values of the rows and columns. If a box is already present,
    #this method is capable of detecting that.

    def fillTruckLocation(self, row, column, boxInfo):
        for R in range(row, row+boxInfo[2]):
            for C in range(column, column+boxInfo[3]):
                self.truck[R][C] = boxInfo[1]
    #This method accepts a row and columns representing the location of the
    #upper left corner of the box. Each cell is filled with the Box ID of
    #the specific box filling the space.

    def packBox(self, dataList):
        for R in range(len(self.truck)):
            for C in range(len(self.truck[R])):
                if self.truck[R][C] == "":
                    a = self.isValidLocation(R, C, dataList[3], dataList[2])
                    if a == True:
                        b = self.fillTruckLocation(R, C, dataList)
                        return True
        return False
    #This method looks through the truck to find an empty cell. It goes row
    #by row and attempts to pack the corner of the box in a found empty cell.
    #The isValidLocation method is used to see which boxes can and cannot fit.

    def packTruck(self):
        self.cList = []
        for aList in self.listOfData:
            bList = []
            area = aList[1]*aList[2]
            bList.append(area)
            for item in aList:
                bList.append(item)
            self.cList.append(bList)
        if self.var.get()== 1:
            self.cList.sort(reverse = True)
        elif self.var.get() == 2:
            self.cList.sort()
        else:
            return None
        self.notPacked = []
        self.packed = []
        for item in self.cList:
            f = self.packBox(item)
            if f == False:
                self.notPacked.append(item[1])
            elif f == True:
                self.packed.append(item)
        return self.notPacked
    #This method uses the data from the CSV file to actually pack the truck.
    #The order is dependent on which radio button the user selects. It then
    #returns a list of boxes that were not able to be packed in the truck.

    def writeTruckToCSV(self):
        f = open("truckview.csv", "w", newline="")
        written = csv.writer(f)
        for item in self.truck:
            written.writerow(item)
        f.close()
    #This method creates a CSV file with a table view of boxes that were
    #packed into the truck. 

    def packNSaveClicked(self):
        try:
            self.W = int(self.WidthEntry.get())
            self.L = int(self.LengthEntry.get())
        except:
            messagebox.showwarning("Invalid Move", "You have not entered a valid number for width and length")
        self.truck = []
        for nums in range(0, self.L):
            widthList = []
            for num in range(0, self.W):
                widthList.append("")
            self.truck.append(widthList)
        try:
            c = self.readBoxesFile()
        except:
            messagebox.showwarning("Invalid File", "The CSV file you are trying to read is invalid!")
            return
        packingTruck = self.packTruck()
        writingTruck = self.writeTruckToCSV()
        percentPacked = float(len(self.packed)/len(self.cList))
        percentPacked = round((percentPacked * 100),1)
        a = 0
        b = 0
        for spaces in self.truck:
            for indentSpots in spaces:
                b += 1
                if indentSpots != "":
                    a += 1
        percentTruckFill = float(a/b)
        percentTruckFill = round((percentTruckFill * 100),1)
        
        self.PackingStatsLabel = Label(self.rootWind, text="Packing Statistics")
        self.PackingStatsLabel.grid(row=5, column=1, sticky=E)

        self.PercBoxPackLabel = Label(self.rootWind, text="Percent of Boxes Packed: "+str(percentPacked)+"%")
        self.PercBoxPackLabel.grid(row=6, sticky=W)

        self.PercTruckFillLabel = Label(self.rootWind, text="Percent of Truck Filled: "+str(percentTruckFill)+"%")
        self.PercTruckFillLabel.grid(row=7, sticky=W)

        self.BoxNotPackLabel = Label(self.rootWind, text="Boxes Not Packed:")
        self.BoxNotPackLabel.grid(row=6, column=2)

        rows = 6
        for item in self.notPacked:
            rows += 1
            Label(self.rootWind, text=str(item)).grid(row=int(rows), column=2, padx = 30)
    #This final method sets the truck to have the correct number of empty spaces,
    #read in the CSV file that contains info about the boxes, packs the boxes,
    #writes the truck's contents to "truckview.csv", and displays some statistics
    #to the user about the packed truck using widgets in the GUI.

win = Tk()
win.title('tk')
myApp = BoxPacker(win)
win.mainloop()

