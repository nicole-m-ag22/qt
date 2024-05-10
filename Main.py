from PyQt6 import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import json
import pickle

#global variables
vec1, vec2, lineColor = [], [], []
lastSave = 0
color = "Black"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Niki paint")
        self.setFixedSize(400, 300)
        self.show()
        self.__leftMouseButtonDown = False

        #vec1 and vec2 of the current line
        self.__vec1 = QPoint()
        self.__vec2 = QPoint()

        self.__path = None
        self.menuBar().setNativeMenuBar(False)

        fileMenu = self.menuBar().addMenu("File")
        newAction = QAction("New", self)
        newAction.triggered.connect(self.onNew)
        fileMenu.addAction(newAction)

        openAction = QAction("Open", self)
        openAction.triggered.connect(self.onOpen)
        fileMenu.addAction(openAction)

        saveAction = QAction("Save", self)
        saveAction.triggered.connect(self.onSave)
        fileMenu.addAction(saveAction)

        saveAsAction = QAction("Save as", self)
        saveAsAction.triggered.connect(self.onSaveAs)
        fileMenu.addAction(saveAsAction)

        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.onExit)
        exitAction.setShortcut("Alt+X")
        fileMenu.addAction(exitAction)

        colorMenu = self.menuBar().addMenu("Color")
        redAction = QAction("Red", self)
        redAction.triggered.connect(self.onRed)
        colorMenu.addAction(redAction)

        greenAction = QAction("Green", self)
        greenAction.triggered.connect(self.onGreen)
        colorMenu.addAction(greenAction)

        blueAction = QAction("Blue", self)
        blueAction.triggered.connect(self.onBlue)
        colorMenu.addAction(blueAction)

        blackAction = QAction("Black", self)
        blackAction.triggered.connect(self.onBlack)
        colorMenu.addAction(blackAction)


    def onNew(self):
        global vec1, vec2, lineColor, lastSave
        vec1, vec2, lineColor, lastSave = [], [], [], 0


    def onOpen(self):
        (path, _) = QFileDialog.getOpenFileName \
            (self, "Open File", self.__path, \
             "Draw files (*.drw)")
        if path:
            self.__path = path

            #opens the file on the path
            with open(self.__path, "rb") as f:
                saveArray = pickle.load(f)    #converts the json on the file back into an array/list
                f.close()
            global vec1, vec2, lineColor, lastSave
            vec1 = saveArray[0]
            vec2 = saveArray[1]
            lineColor = saveArray[2]
            lastSave = len(vec1)
            QMessageBox.about(self, "Path", "Opened")

    def onSave(self):
        global vec1, vec2, lineColor, lastSave
        if self.__path:
            saveArray = [vec1, vec2, lineColor]
            #opens/creates the file on the path
            with open(self.__path, "wb") as f:
                pickle.dump(saveArray, f)     #converts the data from the drawing into json
                f.close()
            lastSave = len(vec1)
            QMessageBox.about(self, "Path", "Saved")
        else:
            QMessageBox.about(self, "Error", "Please create a save file first")

    def onSaveAs(self):
        global vec1, vec2, lineColor, lastSave
        (path, _) = QFileDialog.getSaveFileName \
            (self, "Save File", self.__path, \
            "Draw files (*.drw)")
        if path:
            self.__path = path
            saveArray = [vec1, vec2, lineColor]
            #opens/creates the file on the path
            with open(self.__path, "wb") as f:
                pickle.dump(saveArray, f)     #converts the data from the drawing into json
                f.close()
            lastSave = len(vec1)
            QMessageBox.about(self, "Path", "Saved")

    def onExit(self):
        if QMessageBox.question(self, "Quit", "Do you want to quit") == \
                QMessageBox.StandardButton.Yes:
            application.exit(0) # The application quits.

    def closeEvent(self, event):
        global vec1, lastSave
        if QMessageBox.question \
                (self, "Quit", "Do you want to quit") == \
                QMessageBox.StandardButton.Yes:
            if lastSave != len(vec1):
                if QMessageBox.question \
                        (self, "Unsaved work", "do you want to save") == \
                        QMessageBox.StandardButton.Yes:
                    self.onSaveAs()
                else:
                    event.accept()
            else:
                # The window closes, and the application quits.
                event.accept()
        else:
            # Nothing happens.
            event.ignore()

    def onRed(self):
        global color
        color = "Red"

    def onGreen(self):
        global color
        color = "Green"

    def onBlue(self):
        global color
        color = "Blue"

    def onBlack(self):
        global color
        color = "Black"

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.__leftMouseButtonDown = True
            self.__vec1 = event.pos()
            self.__vec2 = event.pos()
            # The call to update forces a repainf of the window.
            # It indirecly calls the paintEvent method.
        self.update()

    def mouseMoveEvent(self, event):
        if self.__leftMouseButtonDown:
            self.__vec2 = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        global vec1, vec2, lineColor, color
        if self.__leftMouseButtonDown:
            self.__leftMouseButtonDown = False
        
        vec1.append(self.__vec1)
        vec2.append(self.__vec2)
        lineColor.append(color)

    def paintEvent(self, _):
        global vec1, vec2, lineColor, lastSave, title, color
        qPainter = QPainter(self)
        qPen = QPen(QColor(color))
        qPen.setStyle(Qt.PenStyle.DashLine)
        qPainter.setPen(qPen)

        qPainter.drawLine(QLine(self.__vec1, self.__vec2))
        
        for i in range(len(vec1)):
            qPen = QPen(QColor(lineColor[i]))
            qPen.setStyle(Qt.PenStyle.DashLine)
            qPainter.setPen(qPen)

            qPainter.drawLine(vec1[i], \
            vec2[i])

        if lastSave != len(vec1):
            self.setWindowTitle("niki paint*")
        else:
            self.setWindowTitle("niki paint")

    

application = QApplication([])
mainWindow = MainWindow()
application.exec()

