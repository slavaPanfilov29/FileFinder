import sys
import os
import subprocess
## ЕСЛИ НЕ РАБОТАЕТ, ПОМЕНЯЙ ВЕРСИЮ PYQT
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow
from PyQt5.Qt import *
from PyQt5 import QtWidgets
from ui_imagedialog import Ui_MainWindow

#python -m PyQt5.uic.pyuic -x ui_imagedialog.ui -o ui_imagedialog.py

supportedExtensions = {".cpp; .c; .h; .hpp" : "--cpp", 
                       ".php" : "--php", 
                       ".json" : "--json",
                       ".java; .properties" : "--java", 
                       ".py" : "--python", 
                       ".ipynb" : "--ipython", 
                       ".htm; .html; .shtml; .xhtml" : "--html", 
                       "Все расширения" : "all"}
filePreviews = []

startDirectory = ""
textToFind = ""

## ПЕРВОНАЧАЛЬНАЯ НАСТРОЙКА, ЛУЧШЕ НЕ ТРОГАЙ - УБЬЕТ
app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
window.show()

## ДОБАВЛЯЕМ ТИПЫ ФАЙЛОВ В COMBOBOX
ui.extensionSelect.clear()
for i in supportedExtensions.keys():
    ui.extensionSelect.addItem(i)

## ФУНКЦИЯ ВЫЧЛИНЕНИЯ ИЗ ВЫВОДА ФАЙЛА НУЖНЫХ ДАННЫХ
def makePreviewText(s):
    ui.fileSelect.clear()
    filePreviews.clear()    

    rows = s.split('\n')
    
    for i in reversed(range(len(rows))):
        if (rows[i].find(startDirectory) == -1):
            rows.pop(i)

    if (len(rows) == 0): 
        messageBox = QMessageBox()
        messageBox.setText("Ничего не найдено.")
        messageBox.exec()
        return

    prevIndex = -1
    for row in rows:
        if not ui.searchInName.isChecked():
            file = row[0 : row.find(':', 3)]
            file = file.replace(startDirectory + "/", "")
            row = row.replace(row[0 : row.find(':', 3) + 1], "", 1)

            if (row.find('-') == -1 or row.find(':') != -1 and row.find(':') < row.find('-')):  
                currIndex = int(row[0 : row.find(':')])
                row = row.replace(row[0 : row.find(':') + 1], "", 1)
            else:                                                                               
                currIndex = int(row[0 : row.find('-')])
                row = row.replace(row[0 : row.find('-') + 1], "", 1)

            if (ui.fileSelect.findText(file) == -1):    
                filePreviews.append(row + "\n")
            else:
                if (currIndex - prevIndex == 1):        
                    filePreviews[len(filePreviews) - 1] += row + "\n"
                else:                                   
                    filePreviews[len(filePreviews) - 1] += "\n\n\n" + row + "\n"
            prevIndex = currIndex
        else:
            file = row
            file = file.replace(startDirectory + "/", "")

        if (ui.fileSelect.findText(file) == -1):
            ui.fileSelect.addItem(file)  
        
## ГЛАВНАЯ ФУНКЦИЯ ПОИСКА, ВЫЗЫВАЕТСЯ ПРИ НАЖАТИИ НА КНОПКУ НАЙТИ
def onFindButtonClick():
    selectedExtension = supportedExtensions.get(ui.extensionSelect.currentText())
    textToFind = ui.textToFind.toPlainText()    

    if (textToFind == ""): 
        messageBox = QMessageBox()
        messageBox.setText("Введите искомый текст.")
        messageBox.exec()
        return
    if (startDirectory == ""): 
        messageBox = QMessageBox()
        messageBox.setText("Выберите директорию поиска.")
        messageBox.exec()
        return

    params = []
    params.append("ag")
    params.append("-s" if ui.useRegister.isChecked() else "-i") 
    if (ui.searchInName.isChecked()):
        params.append("-g" + textToFind)
    if (selectedExtension != "all"):
        params.append(selectedExtension) 
    if (not ui.searchInName.isChecked()):
        params.append(textToFind) 
    params.append(startDirectory) 
    
    rawOutput = subprocess.Popen(params, encoding='utf-8', stdout=subprocess.PIPE).communicate()[0]

    makePreviewText(rawOutput)
    onFileSelectChange()

## СМЕНА ФАЙЛА       
def onFileSelectChange():
    if (len(filePreviews) > 0):
        ui.filePreview.setText(filePreviews[ui.fileSelect.currentIndex()])
    else:
        ui.filePreview.setText("")

## ВЫБРАТЬ ДИРЕКТОРИЮ ДЛЯ НАЧАЛА ПОИСКА
def onDirectoryClick():
    global startDirectory
    buffDirectory = QtWidgets.QFileDialog.getExistingDirectory(ui.selectDirectoryButton, 'Выберите директорию', os.getenv('HOME'), QtWidgets.QFileDialog.ShowDirsOnly)
    
    if buffDirectory != "":
        startDirectory = buffDirectory
        ui.selectDirectoryButton.setText(startDirectory)

## ОТКРЫТЬ ВЫБРАННЫЙ ФАЙЛ
def onOpenFileButtonClicked():
    os.startfile(startDirectory + "/" + ui.fileSelect.currentText())

ui.findButton.clicked.connect(onFindButtonClick)
ui.fileSelect.currentIndexChanged.connect(onFileSelectChange)
ui.selectDirectoryButton.clicked.connect(onDirectoryClick)
ui.openFileButton.clicked.connect(onOpenFileButtonClicked)

sys.exit(app.exec())