import re
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout


class WordCounterWidget(QWidget):
    """
    Widget reutilizable para contar palabras, caracteres y tiempo de lectura.
    
    Señales:
        conteoActualizado(int, int): Emitida cuando se actualiza el conteo.
            - Primer parámetro: número de palabras
            - Segundo parámetro: número de caracteres
    """
    conteoActualizado = Signal(int, int)

    def __init__(self, wpm=200, mostrarPalabras=True, mostrarCaracteres=True, mostrarTiempoLectura=True, parent=None):
        """
        Inicializa el widget contador.
        
        Args:
            wpm (int): Palabras por minuto para calcular tiempo de lectura (default: 200)
            mostrarPalabras (bool): Mostrar contador de palabras (default: True)
            mostrarCaracteres (bool): Mostrar contador de caracteres (default: True)
            mostrarTiempoLectura (bool): Mostrar tiempo estimado de lectura (default: True)
            parent: Widget padre (default: None)
        """
        super().__init__(parent)
        self.wpm = max(1, int(wpm))
        self.mostrarPalabras = bool(mostrarPalabras)
        self.mostrarCaracteres = bool(mostrarCaracteres)
        self.mostrarTiempoLectura = bool(mostrarTiempoLectura)

        self.lblP = QLabel("Palabras: 0")
        self.lblC = QLabel("Caracteres: 0")
        self.lblT = QLabel("Lectura: 0 min")

        lay = QHBoxLayout(self)
        lay.setContentsMargins(6, 2, 6, 2)
        lay.setSpacing(12)
        lay.addWidget(self.lblP)
        lay.addWidget(self.lblC)
        lay.addWidget(self.lblT)
        lay.addStretch()

        self._apply_visibility()

    def _apply_visibility(self):
        """Aplica la configuración de visibilidad a los labels."""
        self.lblP.setVisible(self.mostrarPalabras)
        self.lblC.setVisible(self.mostrarCaracteres)
        self.lblT.setVisible(self.mostrarTiempoLectura)

    def update_from_text(self, text: str):
        """
        Actualiza los contadores basándose en el texto proporcionado.
        
        Args:
            text (str): Texto a analizar
            
        Emite:
            conteoActualizado(palabras, caracteres): Señal con los valores actualizados
        """
        text = text or ""
        palabras = len(re.findall(r"\b\w+\b", text))
        caracteres = len(text)
        seg = int((palabras / self.wpm) * 60)

        self.lblP.setText(f"Palabras: {palabras}")
        self.lblC.setText(f"Caracteres: {caracteres}")
        self.lblT.setText(f"Lectura: {seg}s" if seg < 60 else f"Lectura: {round(seg/60)} min")

        self.conteoActualizado.emit(palabras, caracteres)
