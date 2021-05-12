
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime as dt
from datetime import timedelta
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QStatusBar
import json, os

class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        self.dtl=[]
        self.dtp=''

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(812, 711)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setFrameShape(QtWidgets.QFrame.HLine)
        self.listWidget.setWordWrap(True)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        font = QtGui.QFont()
        font.setFamily("Helvetica-Narrow")
        font.setPointSize(14)
        self.listWidget.setFont(font) 
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 812, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_chat_JSON = QtWidgets.QAction(MainWindow)
        self.actionOpen_chat_JSON.setObjectName("actionOpen_chat_JSON")
        self.menuMenu.addAction(self.actionOpen_chat_JSON)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.actionOpen_chat_JSON.triggered.connect(self.open_file)
        self.listWidget.clicked.connect(self.listItemclicked)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "InstaChatParser"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False) 
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Chat will appear here."))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionOpen_chat_JSON.setText(_translate("MainWindow", "Open chat JSON"))

    def open_file(self):
        dialog_txt = "Choose Chat JSON"
        filename = QtWidgets.QFileDialog.getOpenFileName(MainWindow, dialog_txt, os.path.expanduser('~'))
        #filename = ('D:/msg1.json', 'All Files (*)')
        print(filename)
        if filename != ('', ''):
            self.getdata(filename[0],self.dtl)
        
    def getdata(self,a,b):
        def strbreak(a):
            b=[]
            c=0
            for _ in a:
                if c<=60:
                    b.append(_)
                else:
                    b.append("\n")
                    b.append(_)
                    c=0
                c+=1
            return "".join(b)

        def dtformat(dtraw):
            yr=dtraw.split("-")[0]
            mnt=dtraw.split("-")[1]
            day=dtraw.split("-")[2].split("T")[0]
            tz=dtraw.split("-")[2].split("T")[1].split("+")[1]
            hour=dtraw.split("-")[2].split("T")[1].split("+")[0].split(":")[0]
            mint=dtraw.split("-")[2].split("T")[1].split("+")[0].split(":")[1]
            secs=dtraw.split("-")[2].split("T")[1].split("+")[0].split(":")[2].split(".")[0]
            dtval1=dt(int(yr),int(mnt),int(day),int(hour),int(mint),int(secs))
            dtval=dtval1+timedelta(hours=5,minutes=30)
            return dtval.strftime("%d")+" "+dtval.strftime("%b")+" "+dtval.strftime("%Y")+" "+dtval.strftime("%I")+":"+dtval.strftime("%M")+":"+dtval.strftime("%S")+" "+dtval.strftime("%p")+": "

        with open(str(a),"r", encoding="utf-8") as jsonfile:
            jsondata=json.load(jsonfile)
        jsondata.reverse()
        ind=0
        for k1 in jsondata:
            k1["conversation"].reverse()
            b.append({"cont":"\nChat b/w "+ k1["participants"][1]+" and "+ k1["participants"][0]+"\n"})
            b[ind]["align"]="c"
            ind+=1
            for k2 in k1["conversation"]:
                b.append({"time":dtformat(k2["created_at"])})
                b[ind]["sender"]=k2["sender"]
                if b[ind]["sender"]==k1["participants"][0]:
                    b[ind]["align"]="r"
                else:
                    b[ind]["align"]="l"
                if "story_share" in k2:
                    b[ind]["cont"]=strbreak(k2["story_share"])+"\n"
                if "text" in k2:
                    if "cont"in b[ind]:
                        b[ind]["cont"]+=strbreak(k2["text"])
                    else:
                        b[ind]["cont"]=strbreak(k2["text"])
                if "media" in k2:
                    b[ind]["cont"]=strbreak(k2["media"])

                ind+=1
        print("DONE")
        self.fillists(self.listWidget)

    def fillists(self,a):
        i=0
        _translate = QtCore.QCoreApplication.translate
        for dts in self.dtl:
            item = QtWidgets.QListWidgetItem()
            a.addItem(item)
            item = a.item(i)
            if dts["align"]=="r":
                item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignRight)
            if dts["align"]=="c":
                item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignHCenter)
            if "cont" in dts:
                item.setText(_translate("MainWindow", dts["cont"]))
            else:
                continue
            i+=1
    
    def listItemclicked(self):
        item1=self.listWidget.currentRow()
        if item1<len(self.dtl):
            if "time" in self.dtl[item1]:
                self.statusbar.showMessage("Date Added: "+self.dtl[item1]["time"])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    dark_palette = QPalette()

    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255,255,255))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255,255,255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255,255,255))
    dark_palette.setColor(QPalette.Text, QColor(255,255,255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255,255,255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(142,45,197).lighter())
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
