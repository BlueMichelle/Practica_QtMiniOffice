from PySide6.QtWidgets import QApplication, QLineEdit, QLabel, QComboBox, QPushButton, QMainWindow 

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana")
        self.setGeometry(100, 100, 280, 120)  # Aumenté la altura para acomodar mejor los elementos

        self.label = QLabel("Usuario:", self)
        self.label = QLabel("Contraseña:", self)
        self.edit_line = QLineEdit(self)
        self.botton = QPushButton("Login", self)
       
        
        self.initUI()

    def initUI(self):
        self.label.move(20, 20)
        self.edit_line.move(20, 50)
        self.botton.move(20, 80)
        self.combo.move(150, 50)

        self.botton.clicked.connect(self.mostrar)

    def mostrar(self):
        texto = self.edit_line.text()
        self.label.setText(texto)
        self.combo.addItem(texto)

if __name__ == "__main__":
    app = QApplication([])
    ventana = Ventana()
    ventana.show()
    app.exec()