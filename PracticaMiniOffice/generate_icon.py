from PySide6.QtGui import QImage, QPainter, QColor
import sys

def create_dummy_icon():
    image = QImage(64, 64, QImage.Format.Format_ARGB32)
    image.fill(QColor("blue"))
    painter = QPainter(image)
    painter.setBrush(QColor("red"))
    painter.drawEllipse(16, 16, 32, 32)
    painter.end()
    image.save("icono.ico")
    print("icono.ico created")

if __name__ == "__main__":
    create_dummy_icon()
