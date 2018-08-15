from Project_gui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow , QApplication
import os.path as osp
import os
from glob import glob

class MyappGui(QMainWindow,Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.init_main_buttons()
		self.init_edit_buttons()

	def init_main_buttons(self):
		self.create_pushButton.clicked.connect(self.create_file)
		self.update_pushButton.clicked.connect(self.update_file)
		self.delete_pushButton.clicked.connect(self.delete_file)
		self.read_pushButton.clicked.connect(self.read_file)
		self.search_pushButton.clicked.connect(self.search_file)

	def init_edit_buttons(self):
		self.save_pushButton.clicked.connect(self.save_file)
		self.back_pushButton.clicked.connect(self.mov_to_main)
		
	def create_file(self):
		path=self.path_lineEdit.text()
		l=[]
		name=self.lineEdit.text()
		if len(name)<=0:
			self.status_label.setText("Enter file name")
		elif len(path)<=0:
			self.status_label.setText("Enter path")
		elif not osp.isdir(path):
			self.status_label.setText("Path Wrong")
		else:
			for i in glob(path+"\*"):
				if osp.isfile(i):
					l.append(i[i.rindex("\\")+1:])
			if name in l:
				self.status_label.setText("Already exist")
			else:
				self.stackedWidget.setCurrentIndex(0)
				self.label_label.setText("Create")
				self.textEdit.clear()
				self.name_label.setText("FILE NAME : "+name)

	def update_file(self):
		self.status_label.setText("STATUS")
		path=self.path_lineEdit.text()
		name=self.files_comboBox.currentText()
		if len(name)<=0:
			self.status_label.setText("No file Selected")
		elif name[:9]=="Dir-->>  ":
			self.status_label.setText("Folder Selected instead of file")
		else:
			self.name_label.setText("FILE NAME : "+name)
			self.stackedWidget.setCurrentIndex(0)
			self.label_label.setText("Update")
			f=open(path+"/"+name,"r")
			self.textEdit.setText(f.read())
			f.close()

		
	def delete_file(self):
		path=self.path_lineEdit.text()
		name=self.files_comboBox.currentText()
		if len(name)>0:
			os.remove(path+"/"+name)
			self.status_label.setText(name+"  Deleted")
		else:
			self.status_label.setText("No file Selected")
			
	def read_file(self):
		self.status_label.setText("STATUS")
		path=self.path_lineEdit.text()
		name=self.files_comboBox.currentText()
		if len(name)<0:
			self.status_label.setText("No file Selected")
		elif name[:9]=="Dir-->>  ":
			self.status_label.setText("Folder Selected instead of file")
		else:
			self.name_label.setText("FILE NAME : "+name)
			self.stackedWidget.setCurrentIndex(0)
			self.label_label.setText("Read")
			self.textEdit.clear()
			f=open(path+"/"+name,"r")
			self.textEdit.setText(f.read())
			f.close()
			
	def search_file(self):
		self.status_label.setText("STATUS")
		path=self.path_lineEdit.text()
		self.files_comboBox.clear()
		if len(path)>0:
			for i in glob(path+"\*"):
				if osp.isfile(i):
					self.files_comboBox.addItems([i[i.rindex("\\")+1:]])
				if osp.isdir(i):
					self.files_comboBox.addItems(["Dir-->>  "+i[i.rindex("\\")+1:]])
				
	def mov_to_main(self):
		self.stackedWidget.setCurrentIndex(1)	
	
	def save_file(self):
		path=self.path_lineEdit.text()
		name=self.name_label.text()[12:]
		if self.label_label.text()!="Read":
			f=open(path+"/"+name,"w")
			f.write(self.textEdit.toPlainText())
			f.close()
		self.mov_to_main()
		


if __name__ =='__main__':
	application=QApplication([]) #firsrt create QApplication object
	Project_gui=MyappGui()
	Project_gui.show()

	application.exec_()