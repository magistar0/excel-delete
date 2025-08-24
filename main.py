import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import pandas as pd

class Function ():
    def readDataFromExcel(filepath: str):
        df = pd.read_excel(open(filepath, 'rb'), index_col=None, header=None)
        return df


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, MainWindow):
        self.setWindowTitle("Excel deletion script")
        self.setMinimumWidth(600)
        self.setMinimumHeight(200)

        self.table1_df = None
        self.table2_df = None
        self.result_df = None

        self.stackedWidget = QStackedWidget()
        self.main_widget = QWidget()
        self.main_layout = QGridLayout()
        self.header = QLabel("Удалить из таблицы 1 имена, имеющиеся в таблице 2.")
        self.from_header = QLabel("Таблица 1: ")
        self.to_header = QLabel("Таблица 2: ")
        self.from_line = QLineEdit()
        self.from_line.setPlaceholderText("Копировать из...")
        self.from_line.setEnabled(False)
        self.from_choose_btn = QPushButton("Выбрать")
        self.to_line = QLineEdit()
        self.to_line.setPlaceholderText("Копировать в...")
        self.to_line.setEnabled(False)
        self.to_choose_btn = QPushButton("Выбрать")
        self.process_btn = QPushButton("Старт")
        self.main_layout.addWidget(self.header, 0, 0, 1, 3, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.from_header, 1, 0)
        self.main_layout.addWidget(self.from_line, 1, 1)
        self.main_layout.addWidget(self.from_choose_btn, 1, 2)
        self.main_layout.addWidget(self.to_header, 2, 0)
        self.main_layout.addWidget(self.to_line, 2, 1)
        self.main_layout.addWidget(self.to_choose_btn, 2, 2)
        self.main_layout.addWidget(self.process_btn, 3, 0, 1, 3)

        self.from_choose_btn.clicked.connect(self.__fromButtonClicked)
        self.to_choose_btn.clicked.connect(self.__toButtonClicked)
        self.process_btn.clicked.connect(self.__process)

        self.main_widget.setLayout(self.main_layout)
        self.stackedWidget.addWidget(self.main_widget)
        self.stackedWidget.setCurrentIndex(0)
        self.setCentralWidget(self.stackedWidget)


    def __fromButtonClicked(self):
        self.from_destination = QFileDialog.getOpenFileName(self, "Выбрать", "", "Excel Files (*.xls *.xlsx)")
        self.from_line.setText(self.from_destination[0])
        df = Function.readDataFromExcel(self.from_destination[0])
        self.table1_df = df

    def __toButtonClicked(self):
        self.to_destination = QFileDialog.getOpenFileName(self, "Выбрать", "", "Excel Files (*.xls *.xlsx)")
        self.to_line.setText(self.to_destination[0])
        df = Function.readDataFromExcel(self.to_destination[0])
        self.table2_df = df

    def __process(self):
        names_to_delete = self.table2_df[0].tolist()
        table1_list = self.table1_df.values.tolist()
        new_table = []
        for i in table1_list:
            if i[0] not in names_to_delete:
                new_table.append(i)
        self.result_df = pd.DataFrame(new_table)
        QMessageBox.information(self,"Готово", "Выберите, куда сохранить файл с результатом.", QMessageBox.Ok)
        self.destination = QFileDialog.getExistingDirectory()
        self.result_df.to_excel(self.destination + "/result.xlsx", index=False)
        QMessageBox.information(self,"Готово", "Файл сохранен по адресу " + self.destination + "/result.xlsx" + ".", QMessageBox.Ok)


def main():
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    app.exec_()

if __name__ == "__main__":
    main()