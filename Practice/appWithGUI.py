from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sys
import time

class Main_app(QMainWindow):
    def __init__(self):
        super(Main_app, self).__init__()
        uic.loadUi('C:/Users/Computer Market/Desktop/Depi/Depi_Amit_AI_BNS3/DataScience/std.ui',self)
        self.tabWidget.tabBar().setvisible(False)
        self.InitUI()
        self.handle_btn()
    def InitUI(self):
        self.setWindowTitle("Student System")
    def handle_btn(self):
        # ------students-------
        self.std_add_btn.clicked.connect(self.add_std_info)
        self.std_update_btn.clicked.connect(self.update_std_info)
        self.std_delete_btn.clicked.connect(self.delete_std_info)
        # ------enrollment-------
        # self.std_add_btn.clicked.connect(self.add_std_info)
        # self.std_update_btn.clicked.connect(self.update_std_info)
        # self.std_delete_btn.clicked.connect(self.delete_std_info)
        # # --------
        # self.std_add_btn.clicked.connect(self.add_std_info)
        # self.std_update_btn.clicked.connect(self.update_std_info)
        # self.std_delete_btn.clicked.connect(self.delete_std_info)
        
    def add_std_info(self):
        print("welcome to my app, by Rawnaa")        
    def update_std_info(self):
        print("welcome to my app, by Rawnaa") 
    def delete_std_info(self):
        print("welcome to my app, by Rawnaa")     
        
        
if __name__ =='__main__':
    app=QApplication(sys.argv)        
    window=Main_app()
    window.show()
    sys.exit(app.exec_())