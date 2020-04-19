import datetime
from tkinter import *
from tkinter import ttk, filedialog

LETTERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
           'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p',
           'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
           'y', 'x', 'c', 'v', 'b', 'n', 'm',
           'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P',
           'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
           'Y', 'X', 'C', 'V', 'B', 'N', 'M', ' ', '\n', '\t', '°', '^', '!', '"', '§', '$', '%', '&', '/', '(', ')', 
           '=', '?', '`', ' ', 'ß', '´', '+', '<', ',', '.', '-', '_', 'ü', 
           'Ü', 'ö', 'Ö', 'ä', 'Ä', '*', '#', '\'', ':', ';', '>', '@', '²', 
           '³', '~', 'µ', '|', '€', '\\', '{', '[', '}', ']', 'á', 
           'à', 'é', 'è', 'í', 'ì', 'ó', 'ò', 'ú', 'ù', 'Á', 'À', 'É', 'È', 'Í', 'Ì', 'Ó', 'Ò', 'Ú', 'Ù']

class StartingFrame(Frame):
    def __init__(self, window, location):
        super().__init__(window)
        self.pack(side = location, expand=True, fill=BOTH)

class Header(Frame):
    def __init__(self, window):
        super().__init__(window, height=50, width = 700)
        self.stBtn = StatisticsButton(self, "Show Statistics")
        self.pack(side=TOP)
        self.pack_propagate(0)        

class StatisticsButton(Button):
    def __init__(self, window, textS):
        super().__init__(window, text=textS)
        self.pack(side=TOP, pady=10)
        self.labelInfo = "Hello another window!"
        self.bind('<Button-1>', self.showStatistics)        
        self.active = False

    def showStatistics(self, event):
        self.active = True
        self.window = Tk()
        self.window.title("Statistics")
        self.window.geometry("300x200")
        self.window.resizable(FALSE, FALSE)        
        
        self.l = Label()
        self.s = Label()

        self.update()

        self.window.pack_propagate(0)
        self.window.mainloop()

    def update(self):
        file = open("./statistics.txt", "r")
        lines = file.readlines()

        accuracy = round(float(lines[0]))
        speed = round(float(lines[1]))

        self.l.destroy()
        self.s.destroy()        

        self.l = Label(self.window, text="Accuracy: " + str(accuracy))
        self.s = Label(self.window, text="Speed: " + str(speed))

        self.l.pack()
        self.s.pack()

class MainFrame(Frame):
    def __init__(self, window):
        super().__init__(window, height=550, width = 700, background="red")
        self.pack(side=TOP)
        self.pack_propagate(0)

class selectTextFile(Button):
    def __init__(self, window):
        super().__init__(window, text="Click to select file")
        self.pack(side=TOP, pady=10)        
        self.bind('<Button-1>', self.selectFile)
        self.filename = ""
    
    def selectFile(self, event):
        self.filename =  filedialog.askopenfilename(initialdir = "./texts", title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
class TextEntry(Text):
    def __init__(self, window):
        super().__init__(window, height=500, background="white", wrap=WORD)
        self.pack(side=TOP, pady=30)

class Window(Tk):    
    def __init__(self):
        super().__init__()
        self.geometry("700x600")
        self.resizable(FALSE, FALSE)
        self.title("Typing trainer")
        self.menu()

    def menu(self, s="Welcome! Press any key to start..."):
        self.header = Header(self)
        self.frame = StartingFrame(self, TOP)
        self.label = Label(self.frame, text=s, width="200")
        self.label.pack(padx=10, pady=20)
        self.frame.bind('<Key>', self.startGame)
        self.frame.focus_set()              
        self.btn = selectTextFile(self.frame)        

    def startGame(self, event):
        self.header.destroy()
        self.frame.destroy()
        self.header = Header(self)

        self.mainFrame = MainFrame(self)                
        
        self.types = 0
        self.correct = 0
        self.typed = 0
        self.textEntry = TextEntry(self.mainFrame)        
        self.textEntry.focus_set()

        self.loadText()
        
        self.textEntry.insert('1.0', self.lines)
        self.textEntry.mark_set("insert", "%d.%d" % (1, 0))        
        self.textEntry.see('1. 0')

        self.textEntry.tag_configure("ACCEPT", foreground="green")
        self.textEntry.tag_configure("FAILURE", foreground="red")

        # Set bindings
        self.textEntry.bind('<Key>', self.overrideInput)        
        self.textEntry.bind('<KeyRelease>', self.handleType)
        self.textEntry.bind('<Return>', self.handleEnter)

        # Set variables
        self.forbiddenEntry = False
        self.ind = 0

        self.start = datetime.datetime.now()

    def loadText(self):           
        if (self.btn.filename == ""):
            filename = filedialog.askopenfilename(initialdir = "./texts", title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))     
        else:
            filename = self.btn.filename
        file = open(filename, "r")
        self.lines = file.read()
        for line in self.lines:
            line = line.strip()
        file.close()

    def overrideInput(self, event):
        return "break"

    def handleType(self, event):
        key = event.char
        self.types += 1
        self.typed += 1;

        if (self.typed >= 5):
            self.typed = 0
            self.writeStatistic()

        if (self.ind == len(self.lines)):
            self.endGame()

        if (key not in LETTERS):
            return "break"            
        else:            
            if (key == self.lines[self.ind] or key == self.lines[self.ind] + self.lines[(self.ind+1)%len(self.lines)]):
                self.moveCursor()
                self.ind += 1
                return "break"
            else:       
                self.highlight(False)
                return "break"    

    def handleEnter(self, event):
        key = '\n'              
        self.types += 1

        if (self.ind == len(self.lines)):
            self.endGame()

        if (self.typed >= 5):
            self.typed = 0
            self.writeStatistic()

        if (key not in LETTERS):     
            return "break"
        else:
            if (key == self.lines[self.ind] or key == self.lines[self.ind] + self.lines[(self.ind+1)%len(self.lines)]):
                self.moveCursor(up=True)
                print(key)
                self.ind += 1
                return "break"
            else:                
                self.highlight(False)
                return "break"

    def moveCursor(self, up=False):
        self.correct += 1

        cursor_pos = self.textEntry.index(INSERT)
        sp = str(cursor_pos).split('.')
    
        y = int(sp[0])
        x = int(sp[1])
        if (not up):            
            self.textEntry.mark_set("insert", "%d.%d" % (y, x+1))
        else:
            self.textEntry.mark_set("insert", "%d.%d" % (y+1, 0))
        
        self.highlight()

    def highlight(self, good=True):
        if good:
            self.textEntry.tag_remove("FAILURE", "1.0", self.textEntry.index(INSERT))
            self.textEntry.tag_add("ACCEPT", '1.0', self.textEntry.index(INSERT))
            self.mainFrame.configure(bg="green")
        else:
            cursor_pos = self.textEntry.index(INSERT)
            sp = str(cursor_pos).split('.')
        
            y = int(sp[0])
            x = int(sp[1])
                        
            self.textEntry.tag_add("FAILURE", "%d.%d" % (y, x), "%d.%d" % (y, x+1) )  
            self.mainFrame.configure(bg="red")

    def endGame(self):
        if (self.header.stBtn.active):
            self.header.stBtn.window.destroy()
        self.header.destroy()
        self.mainFrame.destroy()
        self.menu("Great job! If you want to do it again, press any key...")

    def writeStatistic(self):
        file = open("./statistics.txt", "w")
        file.writelines( str(self.correct / self.types * 100) + "\n" )
        file.writelines( str(5 / ( (datetime.datetime.now() - self.start).total_seconds()) * 60) + "\n")
        self.start = datetime.datetime.now()
        file.close()

        if (self.header.stBtn.active):
            self.header.stBtn.update()
root = Window()

root.mainloop()