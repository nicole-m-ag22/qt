from PyQt6 import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import pickle



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

        #save variables
        self.vec1 = []
        self.vec2 = []
        self.lineColor = []
        self.lastSave = 0
        self.color = "Black"

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
        self.vec1 = []
        self.vec2 = []
        self.lineColor = []
        self.lastSave = 0


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
            self.vec1 = saveArray[0]
            self.vec2 = saveArray[1]
            self.lineColor = saveArray[2]
            self.lastSave = len(self.vec1)
            QMessageBox.about(self, "Path", "Opened")

    def onSave(self):
        if self.__path:
            saveArray = [self.vec1, self.vec2, self.lineColor]
            #opens/creates the file on the path
            with open(self.__path, "wb") as f:
                pickle.dump(saveArray, f)     #converts the data from the drawing into json
                f.close()
            self.lastSave = len(self.vec1)
            QMessageBox.about(self, "Path", "Saved")
        else:
            QMessageBox.about(self, "Error", "Please create a save file first")

    def onSaveAs(self):
        (path, _) = QFileDialog.getSaveFileName \
            (self, "Save File", self.__path, \
            "Draw files (*.drw)")
        if path:
            self.__path = path
            saveArray = [self.vec1, self.vec2, self.lineColor]
            #opens/creates the file on the path
            with open(self.__path, "wb") as f:
                pickle.dump(saveArray, f)     #converts the data from the drawing into json
                f.close()
            self.lastSave = len(self.vec1)
            QMessageBox.about(self, "Path", "Saved")

    def onExit(self):
        if QMessageBox.question(self, "Quit", "Do you want to quit") == \
                QMessageBox.StandardButton.Yes:
            application.exit(0) # The application quits.

    def closeEvent(self, event):
        if QMessageBox.question \
                (self, "Quit", "Do you want to quit") == \
                QMessageBox.StandardButton.Yes:
            if self.lastSave != len(self.vec1):
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
        self.color = "Red"

    def onGreen(self):
        self.color = "Green"

    def onBlue(self):
        self.color = "Blue"

    def onBlack(self):
        self.color = "Black"

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
        if self.__leftMouseButtonDown:
            self.__leftMouseButtonDown = False
        
        self.vec1.append(self.__vec1)
        self.vec2.append(self.__vec2)
        self.lineColor.append(self.color)

    def paintEvent(self, _):
        qPainter = QPainter(self)
        qPen = QPen(QColor(self.color))
        qPen.setStyle(Qt.PenStyle.DashLine)
        qPainter.setPen(qPen)

        qPainter.drawLine(QLine(self.__vec1, self.__vec2))
        
        for i in range(len(self.vec1)):
            qPen = QPen(QColor(self.lineColor[i]))
            qPen.setStyle(Qt.PenStyle.DashLine)
            qPainter.setPen(qPen)

            qPainter.drawLine(self.vec1[i], \
            self.vec2[i])

        if self.lastSave != len(self.vec1):
            self.setWindowTitle("niki paint*")
        else:
            self.setWindowTitle("niki paint")

    

application = QApplication([])
mainWindow = MainWindow()
application.exec()

