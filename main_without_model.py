"""
"""


import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, 
                               QWidget, QComboBox, QPushButton, QFileDialog, QLineEdit,
                               QLabel)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

import warnings
warnings.filterwarnings("ignore")


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        self.data = None

        # Main Layout ---------------------------------------
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        # ---------------------------------------------------

        # CSV File Selector ----------------------------------
        self.file_widget = QWidget()
        self.file_layout = QHBoxLayout(self.file_widget)

        self.file_line = QLineEdit()
        self.file_line.setPlaceholderText("파일을 선택해주세요.")
        self.file_line.setReadOnly(True)
        self.file_layout.addWidget(self.file_line)

        self.open_button = QPushButton("Open File", self)
        self.open_button.clicked.connect(self.open_file)
        self.file_layout.addWidget(self.open_button)

        self.layout.addWidget(self.file_widget)
        # --------------------------------------------------

        # Combo Box ----------------------------------------
        self.combo_box1 = QComboBox(self)
        self.combo_box2 = QComboBox(self)
        self.layout.addWidget(self.combo_box1)
        self.layout.addWidget(self.combo_box2)
        self.combo_box1.setPlaceholderText("로드된 데이터가 없습니다.")
        self.combo_box2.setPlaceholderText("로드된 데이터가 없습니다.")
        # --------------------------------------------------

        # Draw Plot -----------------------------------------
        self.canvas = FigureCanvas(Figure())
        self.layout.addWidget(self.canvas)

        self.ax = self.canvas.figure.add_subplot(111)
        # ---------------------------------------------------

        # Connect Event --------------------------------------
        self.combo_box1.currentIndexChanged.connect(self.update_plot)
        self.combo_box2.currentIndexChanged.connect(self.update_plot)
        # ----------------------------------------------------


    # Open file dialog
    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV Files (*.csv)")

        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            self.file_line.setText(selected_file)
        
            self.read_data()
            self.set_columns()

    
    # Read data -> DataFrame
    def read_data(self):
        csv_file_path = self.file_line.text()
        if csv_file_path != "":
            self.data = pd.read_csv(csv_file_path)
            

    # Set columns 
    def set_columns(self):
        if self.data is not None :
            self.combo_box1.clear()
            self.combo_box1.setPlaceholderText("컬럼을 선택해주세요.")
            self.combo_box1.addItems(self.data.columns)

            self.combo_box2.clear()
            self.combo_box2.setPlaceholderText("컬럼을 선택해주세요.")
            self.combo_box2.addItems(self.data.columns)


    # Draw canvas
    def update_plot(self):
        selected_column1 = self.combo_box1.currentText()
        selected_column2 = self.combo_box2.currentText()
        self.ax.clear()
        if selected_column1 and selected_column2 :
            self.ax.scatter(self.data[selected_column1], self.data[selected_column2])
            self.ax.set_xlabel(selected_column1)
            self.ax.set_ylabel(selected_column2)
            self.ax.set_title(f'Scatter Plot: {selected_column1} vs {selected_column2}')
            self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
