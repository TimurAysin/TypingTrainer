import datetime
from tkinter import *
from tkinter import ttk, filedialog

LETTERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
           'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p',
           'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
           'y', 'x', 'c', 'v', 'b', 'n', 'm',
           'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P',
           'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
           'Y', 'X', 'C', 'V', 'B', 'N', 'M', ' ', '\n', '\t',
           '°', '^', '!', '"', '§', '$', '%', '&', '/', '(', ')',
           '=', '?', '`', ' ', 'ß', '´', '+', '<', ',', '.', '-', '_', 'ü',
           'Ü', 'ö', 'Ö', 'ä', 'Ä', '*', '#', '\'', ':', ';', '>', '@',
           '²', '³', '~', 'µ', '|', '€', '\\', '{', '[', '}', ']', 'á',
           'à', 'é', 'è', 'í', 'ì', 'ó', 'ò', 'ú', 'ù', 'Á', 'À', 'É',
           'È', 'Í', 'Ì', 'Ó', 'Ò', 'Ú', 'Ù']


class StartingFrame(Frame):
    def __init__(self, window, location):
        super().__init__(window)
        self.pack(side=location, expand=True, fill=BOTH)


class MenuHeader(Frame):
    def __init__(self, window):
        super().__init__(window, height=50, width=700)
        self.speedButton = StatisticsButton(self, "Show Info")
        self.pack(side=TOP)
        self.pack_propagate(0)


class GameHeader(Frame):
    def __init__(self, window):
        super().__init__(window, height=50, width=700)
        self.speedButton = SpeedButton(self, "Show Speed")
        self.pack(side=TOP)
        self.pack_propagate(0)


class SpeedButton(Button):
    def __init__(self, window, textS):
        super().__init__(window, text=textS)
        self.pack(side=TOP, pady=10)
        self.labelInfo = "Hello another window!"
        self.bind('<Button-1>', self.showInfo)
        self.active = False

    def showInfo(self, event):
        self.active = True
        self.window = Tk()
        self.window.title("Speed")
        self.window.geometry("300x200")
        self.window.resizable(FALSE, FALSE)

        self.l = Label()
        self.s = Label()

        self.window.pack_propagate(0)
        self.window.mainloop()

    def update(self, accuracy, speed):
        self.l.destroy()
        self.s.destroy()

        self.l = Label(self.window, text="Accuracy: " + accuracy + "%")
        self.s = Label(self.window, text="Speed: " + speed + "sym/minute")

        self.l.pack()
        self.s.pack()


class MainFrame(Frame):
    def __init__(self, window):
        super().__init__(window, height=550, width=700, background="red")
        self.pack(side=TOP)
        self.pack_propagate(0)


class SelectTextFile(Button):
    def __init__(self, window):
        super().__init__(window, text="Click to select file")
        self.pack(side=TOP, pady=10)
        self.bind('<Button-1>', self.selectFile)
        self.filename = ""

    def selectFile(self, event):
        self.filename = filedialog.askopenfilename(
            initialdir="./texts", title="Select file",
            filetypes=(("txt files", "*.txt"), ("all files", "*.*")))


class TextEntry(Text):
    def __init__(self, window):
        super().__init__(window, height=500, background="white", wrap=WORD)
        self.pack(side=TOP, pady=30)


class StatisticsButton(Button):
    def __init__(self, window, textS):
        super().__init__(window, text=textS)
        self.pack(side=TOP, pady=10)
        self.labelInfo = "Hello another window!"
        self.bind('<Button-1>', self.showInfo)
        self.statisticsFile = "./statistics.txt"
        self.lines = ""

    def showInfo(self, event):
        self.root = Tk()
        self.root.title("Statistics")
        self.root.resizable(FALSE, FALSE)

        container = ttk.Frame(self.root)
        canvas = Canvas(container, width=200)
        scrollbar = ttk.Scrollbar(
            container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.readFile()

        self.l = Label(scrollable_frame, text=self.lines)
        self.l.grid(row=0, column=0, columnspan=100)

        self.l.pack(fill="both", expand=True)
        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.root.mainloop()

    def readFile(self):
        file = open(self.statisticsFile, "r")
        line = file.readline()

        ind = 1

        while line:
            s = ""
            s += "Game: " + str(ind) + "\n"
            s += "Accuracy: " + line.split(",")[0].strip() + "%\n"
            s += "Speed: " + line.split(",")[1].strip() + "sym/minute\n\n"
            self.lines += s
            ind += 1
            line = file.readline()


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("700x600")
        self.resizable(FALSE, FALSE)
        self.title("Typing trainer")
        self.menu()
        self.statisticsFile = "./statistics.txt"

    def menu(self, s="Welcome! Press any key to start..."):
        self.header = MenuHeader(self)
        self.frame = StartingFrame(self, TOP)
        self.label = Label(self.frame, text=s, width="200")
        self.label.pack(padx=10, pady=20)
        self.frame.bind('<Key>', self.startGame)
        self.frame.focus_set()
        self.btn = SelectTextFile(self.frame)

    def startGame(self, event):
        self.header.destroy()
        self.frame.destroy()
        self.header = GameHeader(self)
        self.updateTimeInSeconds = 2

        self.mainFrame = MainFrame(self)

        self.types = 0
        self.correct = 0
        self.textEntry = TextEntry(self.mainFrame)

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
        self.textEntry.bind('<Button-1>', self.handleMouseInput)
        self.textEntry.bind('<ButtonRelease-1>', self.handleMouseInput)
        self.textEntry.bind('<B1-Motion>', self.handleMouseInput)
        self.textEntry.bind('<Double-Button-1>', self.handleMouseInput)

        # Set variables
        self.forbiddenEntry = False
        self.ind = 0
        self.timer = datetime.datetime.now()
        self.start = datetime.datetime.now()
        self.accuracy = 0
        self.speed = 0

        self.textEntry.focus_set()

    def handleMouseInput(self, *args):
        self.textEntry.focus_set()
        return "break"

    def loadText(self):
        if self.btn.filename == "":
            filename = filedialog.askopenfilename(
                initialdir="./texts", title="Select file",
                filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
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

        now = datetime.datetime.now()

        if (now - self.timer).total_seconds() >= self.updateTimeInSeconds:
            self.updateStatistics()

        if self.ind >= len(self.lines):
            self.endGame()
            return "break"

        sym = self.lines[self.ind]
        nextSym = self.lines[self.ind] + \
                  self.lines[(self.ind + 1) % len(self.lines)]

        if key not in LETTERS:
            return "break"
        else:
            if key == sym or key == nextSym:
                self.moveCursor()
                self.ind += 1
                return "break"
            else:
                self.highlight(False)
                return "break"

    def handleEnter(self, event):
        key = '\n'
        self.types += 1

        if self.ind >= len(self.lines):
            self.endGame()
            return "break"

        now = datetime.datetime.now()

        if (now - self.timer).total_seconds() >= self.updateTimeInSeconds:
            self.updateStatistics()

        sym = self.lines[self.ind]
        nextSym = self.lines[self.ind] + \
                  self.lines[(self.ind + 1) % len(self.lines)]

        if key not in LETTERS:
            return "break"
        else:
            if key == sym or key == nextSym:
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
        if not up:
            self.textEntry.mark_set("insert", "%d.%d" % (y, x + 1))
        else:
            self.textEntry.mark_set("insert", "%d.%d" % (y + 1, 0))

        self.highlight()

    def highlight(self, good=True):
        if good:
            self.textEntry.tag_remove(
                "FAILURE", "1.0", self.textEntry.index(INSERT))
            self.textEntry.tag_add(
                "ACCEPT", '1.0', self.textEntry.index(INSERT))
            self.mainFrame.configure(bg="green")
        else:
            cursor_pos = self.textEntry.index(INSERT)
            sp = str(cursor_pos).split('.')

            y = int(sp[0])
            x = int(sp[1])

            self.textEntry.tag_add("FAILURE", "%d.%d" %
                                   (y, x), "%d.%d" % (y, x + 1))
            self.mainFrame.configure(bg="red")

    def endGame(self):
        self.writeStatistics()
        if self.header.speedButton.active:
            self.header.speedButton.window.destroy()
        self.header.destroy()
        self.mainFrame.destroy()
        self.menu("Great job! If you want to do it again, press any key...")

    def writeStatistics(self):
        file = open(self.statisticsFile, "a+")
        self.speed = round(
            self.types * 60 /
            ((datetime.datetime.now() - self.start).total_seconds()))
        self.accuracy = round(self.correct / self.types * 100)
        file.write(str(self.accuracy) + "," + str(self.speed) + "\n")
        file.close()

        if self.header.speedButton.active:
            self.header.speedButton.update(str(self.accuracy), str(self.speed))

    def updateStatistics(self):
        if (self.header.speedButton.active):
            self.speed = round(
                self.types * 60 /
                ((datetime.datetime.now() - self.start).total_seconds()))
            self.accuracy = round(self.correct / self.types * 100)
            self.header.speedButton.update(str(self.accuracy), str(self.speed))
            self.timer = datetime.datetime.now()


root = Window()

root.mainloop()
