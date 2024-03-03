import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, 
                               QWidget, QComboBox, QPushButton, QFileDialog, QLineEdit,
                               QLabel)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

# import my model
from models.my_analysis import MyModel

import warnings
warnings.filterwarnings("ignore")


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        self.my_model = MyModel()

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

        # My Analysis Model ---------------------------------
        self.my_model_label = QLabel("분석 결과(상관관계)")
        self.my_model_line = QLineEdit()
        self.layout.addWidget(self.my_model_label)
        self.layout.addWidget(self.my_model_line)
        # ----------------------------------------------------

        # Connect Event --------------------------------------
        self.combo_box1.currentIndexChanged.connect(self.update_board)
        self.combo_box2.currentIndexChanged.connect(self.update_board)
        # ----------------------------------------------------

    # Open File Dialog
    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV Files (*.csv)")

        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            self.file_line.setText(selected_file)
        
            self.read_data()
            self.set_columns()

    # Read Data 
    def read_data(self):
        csv_file_path = self.file_line.text()
        if csv_file_path != "":
            self.my_model.set_data(data=pd.read_csv(csv_file_path))
            

    # Set columns from data
    def set_columns(self):
        if self.my_model.data is not None :
            self.combo_box1.clear()
            self.combo_box1.setPlaceholderText("컬럼을 선택해주세요.")
            self.combo_box1.addItems(self.my_model.data.columns)

            self.combo_box2.clear()
            self.combo_box2.setPlaceholderText("컬럼을 선택해주세요.")
            self.combo_box2.addItems(self.my_model.data.columns)


    # Data select board
    def update_board(self):
        selected_column1 = self.combo_box1.currentText()
        selected_column2 = self.combo_box2.currentText()
        self.ax.clear()
        if selected_column1 and selected_column2 :
            self.draw_plot(selected_column1, selected_column2)
            self.my_analysis(selected_column1, selected_column2)

    
    # Draw Canvas
    def draw_plot(self, selected_column1:str, selected_column2:str):
        self.ax.scatter(self.my_model.data[selected_column1], self.my_model.data[selected_column2])
        self.ax.set_xlabel(selected_column1)
        self.ax.set_ylabel(selected_column2)
        self.ax.set_title(f'Scatter Plot: {selected_column1} vs {selected_column2}')
        self.canvas.draw()

    # My models
    def my_analysis(self, selected_column1:str, selected_column2:str) :
        corr_result = self.my_model.calc_corr(ca1=selected_column1, ca2=selected_column2)
        self.my_model_line.setText(f"{corr_result:.2f}")

# Define main
def main():
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
