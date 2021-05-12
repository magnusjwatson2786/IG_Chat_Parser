
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime as dt
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
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
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
        font1 = QtGui.QFont()
        font1.setFamily("Monospac821 BT")
        font1.setPointSize(20)
        self.listWidget.setFont(font) 
        self.label.setFont(font1)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "IG_Chat_Parser"))
        self.label.setText(_translate("MainWindow", "Chat Participant"))
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
        print(filename)
        if filename != ('', ''):
            self.getdata(filename[0],self.dtl)
        
    def getdata(self,a,b):
        def endec(a):
            return strbreak(str(a.encode("ISO-8859-1").decode("utf-8")))
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
            day=dtraw.split("-")[2].split(" ")[0]
            hour=dtraw.split("-")[2].split(" ")[1].split(".")[0].split(":")[0]
            mint=dtraw.split("-")[2].split(" ")[1].split(".")[0].split(":")[1]
            secs=dtraw.split("-")[2].split(" ")[1].split(".")[0].split(":")[2]
            dtval=dt(int(yr),int(mnt),int(day),int(hour),int(mint),int(secs))
            return dtval.strftime("%d")+" "+dtval.strftime("%b")+" "+dtval.strftime("%Y")+" "+dtval.strftime("%I")+":"+dtval.strftime("%M")+":"+dtval.strftime("%S")+" "+dtval.strftime("%p")

        with open(str(a),"r", encoding="utf-8") as jsonfile:
            jsondata=json.load(jsonfile)
        jsondata["messages"].reverse()
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow",endec(jsondata["participants"][0]["name"])))
        #c=endec(jsondata["participants"][0]["name"])#+".txt"),"w", encoding="utf-8")
        ind=0
        for message in jsondata["messages"]:
            b.append({"time":dtformat(str(dt.fromtimestamp((message["timestamp_ms"])/1000)))})
            b[ind]["sender"]=endec(message["sender_name"])
            if message["sender_name"]==jsondata["participants"][-1]["name"]:
                b[ind]["align"]="r"
            else:
                b[ind]["align"]="l"
            if message["type"]=="Generic":
                if "content" in message:
                    # b.append(endec(message["sender_name"])+": "+ endec(message["content"]))
                    # b.append("\n")
                    b[ind]["cont"]=endec(message["content"])+"\n"
                if "photos" in message:
                    # b.append(endec(message["sender_name"])+" shared a photo.")
                    # b.append("\n")
                    b[ind]["cont"]="Shared a photo."+"\n"
                if "videos" in message:
                    # b.append(endec(message["sender_name"])+" shared a video.")
                    # b.append("\n")
                    b[ind]["cont"]="Shared a video."+"\n"
            if message["type"]=="Share":
                if "share" in message:
                    if "link" in message["share"]:
                        # b.append(endec(message["sender_name"])+" shared a link "+ endec(message["share"]["link"]))# + endec(message["share"]["share_text"]))
                        b[ind]["cont"]=" shared a link "+ endec(message["share"]["link"])+"\n"
                        if "share_text" in message["share"]:
                            b[ind]["cont"]+="\n"+endec(message["share"]["share_text"])+"\n"
                            # b.append(endec(message["share"]["share_text"]))
                        #b.append("\n")
                    elif "original_content_owner" in message["share"]:
                        b[ind]["cont"]="Shared content by "+ endec(message["share"]["original_content_owner"])+"\n"
                        # b.append(endec(message["sender_name"])+" shared content by "+ endec(message["share"]["original_content_owner"]))
                        # b.append("\n")                    
                if "content" in message:
                    b[ind]["cont"]="Shared and commented: \n"+ endec(message["content"])+"\n"
                    # b.append(endec(message["sender_name"])+" shared and commented: "+ endec(message["content"]))
                    # b.append("\n")
            if "reactions" in message:
                if "cont" in b[ind]:
                    b[ind]["cont"]+="("+endec(message["reactions"][0]["actor"])+" reacted with "+ endec(message["reactions"][0]["reaction"])+"  )\n"
                # b.append("("+endec(message["reactions"][0]["actor"])+" reacted with "+ endec(message["reactions"][0]["reaction"])+"  )")
                # b.append("\n")
            ind+=1
        #outfile.close()
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
            if "cont" in dts:
                item.setText(_translate("MainWindow", dts["cont"]))
            else:
                continue
            i+=1
        #self.label.setText(_translate("MainWindow", self.dtp))
    
    def listItemclicked(self):
        item1=self.listWidget.currentRow()
        if item1<len(self.dtl):
            if "time" in self.dtl[item1]:
                self.statusbar.showMessage("Date Added: "+self.dtl[item1]["time"])
        # self.imgcont.setPixmap(QtGui.QPixmap(item1))

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
