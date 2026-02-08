from PySide6.QtWidgets import QApplication, QLineEdit, QLabel, QComboBox, QPushButton, QMainWindow 

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana")
        self.setGeometry(100, 100, 280, 120)  # Aumenté la altura para acomodar mejor los elementos

        self.label = QLabel("HOLA", self)  
        self.edit_line = QLineEdit(self)
        self.botton = QPushButton("Mostrar", self)
        self.combo = QComboBox(self)
        
        self.initUI()
 
    def initUI(self):
        
        self.edit_line.setMaxLength(5)
        self.edit_line.setFixedSize(50, 30)
        self.edit_line.move(10, 20)
        

        self.edit_line.textChanged.connect(self.actualizar_label_automatico)

       
        self.label.setFixedSize(50, 30)
        self.label.move(70, 20) 
        self.label.setStyleSheet("border: 1px solid gray; padding: 2px;")

        
        self.botton.setFixedSize(100, 30)
        self.botton.move(130, 20)
        self.botton.clicked.connect(self.mostrar_texto)

        
        self.combo.setFixedSize(150, 25)
        self.combo.move(10, 60)  # Uso move para posicionar el ComboBox
        

        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        self.combo.addItems(meses)
        
       
        self.combo.currentIndexChanged.connect(self.mes)
        
        # Label adicional para mostrar información del mes seleccionado
        self.info_label = QLabel("Enero es el mes número 1.", self)
        self.info_label.setFixedSize(200, 25)
        self.info_label.move(10, 90)
        self.info_label.setStyleSheet("background-color: #f0f;")

    def actualizar_label_automatico(self, text):
        """Actualiza el label automáticamente cuando cambia el texto del LineEdit"""
        if text:
            self.label.setText(text)
        else:
            self.label.setText("Hola")  

    def mostrar_texto(self):
        """Función del botón - copia texto del LineEdit al Label"""
        text = self.edit_line.text()
        if text:
            self.label.setText(text)
            # Intentar seleccionar el texto en el ComboBox si existe
            index = self.combo.findText(text)
            if index >= 0:
                self.combo.setCurrentIndex(index)
        
    def mes(self, index):
        """Maneja el cambio de selección en el ComboBox"""
        if index >= 0:  # Verificar que el índice sea válido
            month = self.combo.itemText(index)
            
            # Mostrar información en consola
            print(f"Elemento seleccionado: {month} - Posición: {index}")
            
            # Actualizar el label de información con el número de mes
            mes_numero = index + 1
            self.info_label.setText(f"{month} es el mes número {mes_numero}.")
            
            self.label.setText(month)
            # mostramos lo elemento seleccionado en  el combobox para que salga en el editline
            
            #VAMOS A AJUSTA LA VNTANA AL TAMAÑO DE LOS ELEMENTOS
           
           


if __name__ == "__main__":
    app = QApplication([])
    ventana = Ventana()
    ventana.show()
    app.exec()