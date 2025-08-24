import sys
import os
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from modules import Modules


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, MainWindow):
        self.setWindowTitle("Шифровальщик")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)

        self.stackedWidget = QStackedWidget()
        self.main_widget = QWidget()
        self.main_layout = QGridLayout()
        self.header = QLabel("Введите текст:")
        self.combo = QComboBox()
        self.list_of_items = ["Метод перестановки", "Метод Цезаря", "Ассиметричный метод"]
        self.combo.addItems(self.list_of_items)
        self.combo.setCurrentIndex(0)
        self.header2 = QLabel("Выберите способ шифрования:")
        self.text_edit = QPlainTextEdit(self)
        self.from_file_btn = QPushButton("Прочитать из файла .txt")
        self.encode_btn = QPushButton("Зашифровать")
        self.text_edit_result = QPlainTextEdit(self)
        self.text_edit_result.setReadOnly(True)
        self.text_edit_result.setPlaceholderText("Здесь будет результат шифрования...")
        self.to_file_btn = QPushButton("Записать в файл .txt")

        self.current_mode = 0 # 0 - encode, 1 - decode
        self.btn_header = QLabel("Выберите режим работы программы:")
        self.encode_mode_btn = QPushButton("Шифрование")
        self.decode_mode_btn = QPushButton("Дешифрование")
        self.encode_mode_btn.setEnabled(False)

        self.main_layout.addWidget(self.btn_header, 0, 0, 1, 2, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.encode_mode_btn, 1, 0, 1, 2)
        self.main_layout.addWidget(self.decode_mode_btn, 2, 0, 1, 2)
        self.main_layout.addWidget(self.header, 3, 0, 1, 2, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.text_edit, 4, 0, 1, 1)
        self.main_layout.addWidget(self.from_file_btn, 4, 1, 1, 1)
        self.main_layout.addWidget(self.header2, 5, 0, 1, 2, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.combo, 6, 0, 1, 2)
        self.main_layout.addWidget(self.encode_btn, 7, 0, 1, 2)
        self.main_layout.addWidget(self.text_edit_result, 8, 0, 1, 1)
        self.main_layout.addWidget(self.to_file_btn, 8, 1, 1, 1)

        self.encode_btn.clicked.connect(self.__encodeButtonClicked)
        self.from_file_btn.clicked.connect(self.__fromfileButtonClicked)
        self.to_file_btn.clicked.connect(self.__tofileButtonClicked)
        self.encode_mode_btn.clicked.connect(self.__encodeModeClicked)
        self.decode_mode_btn.clicked.connect(self.__decodeModeClicked)

        self.main_widget.setLayout(self.main_layout)
        self.stackedWidget.addWidget(self.main_widget)
        self.stackedWidget.setCurrentIndex(0)
        self.setCentralWidget(self.stackedWidget)

    def __encodeModeClicked(self):
        self.encode_mode_btn.setEnabled(False)
        self.decode_mode_btn.setEnabled(True)
        self.current_mode = 0
        self.encode_btn.setText("Зашифровать")
        self.header2.setText("Выберите способ шифрования:")

    def __decodeModeClicked(self):
        self.decode_mode_btn.setEnabled(False)
        self.encode_mode_btn.setEnabled(True)
        self.current_mode = 1
        self.encode_btn.setText("Расшифровать")
        self.header2.setText("Выберите способ дешифрования:")

    def __encodeButtonClicked(self):
        self.type = self.combo.currentIndex()
        match self.type:
            case 0:
                if (not self.current_mode):
                    self.crypted = Modules.shuffleCrypto(self.text_edit.toPlainText(),1)
                else:
                    self.crypted = Modules.shuffleDecrypt(self.text_edit.toPlainText(),1)
            case 1:
                if (not self.current_mode):
                    self.crypted = Modules.caesarCrypto(self.text_edit.toPlainText(),1)
                else:
                    self.crypted = Modules.caesarDecrypt(self.text_edit.toPlainText(),1)
            case 2:
                self.crypted = self.text_edit.toPlainText()
                QMessageBox.information(self, "Информация", "Пока недоступно.", QMessageBox.Ok)
        self.text_edit_result.setPlainText(self.crypted)

    def __fromfileButtonClicked(self):
        filename = QFileDialog.getOpenFileName(self,"Выбор файла",'.')
        if not bool(filename[0]):
            pass
        elif not filename[0].endswith(".txt"):
            QMessageBox.critical(self, "Ошибка", "Поддерживаются только файлы формата .txt.", QMessageBox.Ok)
        else:
            text = Modules.readTextFromTxt(filename[0])
            self.text_edit.setPlainText(text)

    def __tofileButtonClicked(self):
        QMessageBox.information(self, "Сохранение файла", "Выберите директорию для сохранения результата шифрования. В ней будет создан файл result.txt с результатом шифрования. Внимание: если файл с таким именем уже существует, его содержимое будет стёрто.", QMessageBox.Ok)
        directory = QFileDialog.getExistingDirectory(self,"Сохранение файла",'.')
        Modules.writeTxtInDir(directory,self.text_edit_result.toPlainText())
        

def main():
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    app.exec_()

if __name__ == "__main__":
    main()