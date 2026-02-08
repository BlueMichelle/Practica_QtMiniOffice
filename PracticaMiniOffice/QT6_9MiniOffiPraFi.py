import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog,
    QToolBar, QMessageBox, QStatusBar, QLabel,
    QColorDialog, QFontDialog,
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton
)
from PySide6.QtGui import QIcon, QKeySequence, QAction, QTextDocument, QFont
from PySide6.QtCore import Qt, QThread, Signal
import speech_recognition as sr
from WordCounterWidget import WordCounterWidget


class FindReplacePanel(QWidget):
    
    def __init__(self, text_edit: QTextEdit, main_window: QMainWindow, parent=None):
        super().__init__(parent)
        self.text_edit = text_edit
        self.main_window = main_window

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Campos de texto
        self.find_edit = QLineEdit()
        self.find_edit.setPlaceholderText("Texto a buscar")
        self.replace_edit = QLineEdit()
        self.replace_edit.setPlaceholderText("Reemplazar con")

        # Botones
        self.btn_find_next = QPushButton("Buscar sig.")
        self.btn_find_prev = QPushButton("Buscar ant.")
        self.btn_find_all = QPushButton("Buscar todas")
        self.btn_replace = QPushButton("Reemplazar")
        self.btn_replace_all = QPushButton("Reemplazar todas")

        # Conexiones
        self.btn_find_next.clicked.connect(self.find_next)
        self.btn_find_prev.clicked.connect(self.find_prev)
        self.btn_find_all.clicked.connect(self.find_all)
        self.btn_replace.clicked.connect(self.replace_one)
        self.btn_replace_all.clicked.connect(self.replace_all)

        # Enter en el campo de búsqueda -> buscar siguiente
        self.find_edit.returnPressed.connect(self.find_next)

        layout.addWidget(self.find_edit)
        layout.addWidget(self.replace_edit)
        layout.addWidget(self.btn_find_next)
        layout.addWidget(self.btn_find_prev)
        layout.addWidget(self.btn_find_all)
        layout.addWidget(self.btn_replace)
        layout.addWidget(self.btn_replace_all)
        layout.addStretch(1)

    # ===== Helpers =====
    def _get_find_text(self) -> str:
        return self.find_edit.text()

    def _get_replace_text(self) -> str:
        return self.replace_edit.text()

    def _show_status(self, msg: str):
        if hasattr(self.main_window, "status_bar"):
            self.main_window.status_bar.showMessage(msg, 3000)

    # ===== Buscar =====
    def find_next(self):
        text = self._get_find_text()
        if not text:
            return

        doc = self.text_edit.document()
        cursor = self.text_edit.textCursor()
        found = doc.find(text, cursor)

        if found.isNull():
            # buscar desde el principio
            start_cursor = self.text_edit.textCursor()
            start_cursor.setPosition(0)
            found = doc.find(text, start_cursor)

        if not found.isNull():
            self.text_edit.setTextCursor(found)
            self._show_status(f'Siguiente "{text}" encontrado')
        else:
            self._show_status(f'No se encontró "{text}"')

    def find_prev(self):
        text = self._get_find_text()
        if not text:
            return

        doc = self.text_edit.document()
        cursor = self.text_edit.textCursor()
        found = doc.find(text, cursor, QTextDocument.FindFlag.FindBackward)

        if found.isNull():
            # buscar desde el final
            end_cursor = self.text_edit.textCursor()
            end_cursor.movePosition(end_cursor.MoveOperation.End)
            found = doc.find(text, end_cursor, QTextDocument.FindFlag.FindBackward)

        if not found.isNull():
            self.text_edit.setTextCursor(found)
            self._show_status(f'Anterior "{text}" encontrado')
        else:
            self._show_status(f'No se encontró "{text}"')

    def find_all(self):
        text = self._get_find_text()
        if not text:
            return

        full_text = self.text_edit.toPlainText()
        count = full_text.count(text)
        self._show_status(f'Se encontraron {count} apariciones de "{text}"')

    # ===== Reemplazar =====
    def replace_one(self):
        find_text = self._get_find_text()
        replace_text = self._get_replace_text()
        if not find_text:
            return

        cursor = self.text_edit.textCursor()
        selected = cursor.selectedText()

        if selected == find_text:
            cursor.insertText(replace_text)
            self.text_edit.setTextCursor(cursor)
            self._show_status("Texto reemplazado, buscando siguiente...")
            self.find_next()
        else:
            self.find_next()

    def replace_all(self):
        find_text = self._get_find_text()
        replace_text = self._get_replace_text()
        if not find_text:
            return

        full_text = self.text_edit.toPlainText()
        count = full_text.count(find_text)
        if count == 0:
            self._show_status(f'No se encontró "{find_text}"')
            return

        new_text = full_text.replace(find_text, replace_text)
        self.text_edit.setPlainText(new_text)
        self._show_status(
            f'Reemplazadas {count} apariciones de "{find_text}" por "{replace_text}"'
        )


class VoiceWorker(QThread):
    recognized_text = Signal(str)
    error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True
        self.recognizer = sr.Recognizer()
    
    def run(self):
        try:
            with sr.Microphone() as source:
                # Calibrar para ruido ambiental
                self.recognizer.adjust_for_ambient_noise(source)
                while self.running:
                    try:
                        # Escuchar con timeout para permitir salir del loop
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                        text = self.recognizer.recognize_google(audio, language="es-ES")
                        self.recognized_text.emit(text.lower())
                    except sr.WaitTimeoutError:
                        continue # No se detectó audio, seguir intentando
                    except sr.UnknownValueError:
                        pass # No se entendió el audio
                    except sr.RequestError as e:
                        self.error.emit(f"Error de red/API: {e}")
                    except Exception as e:
                        self.error.emit(f"Error inesperado: {e}")
        except Exception as e:
            self.error.emit(f"Error inicializando micrófono: {e}")

    def stop(self):
        self.running = False
        self.wait()


class MiniWord(QMainWindow):
    def __init__(self):
        super().__init__()

        # ---- Ventana principal ----
        self.setWindowTitle("Mini Word")
        self.current_file = None

        # ---- Área de texto ----
        self.text_edit = QTextEdit()

        # ---- Panel central: texto + panel buscar/reemplazar ----
        central_widget = QWidget()
        central_layout = QHBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)

        self.find_panel = FindReplacePanel(self.text_edit, self)
        self.find_panel.setFixedWidth(250)

        central_layout.addWidget(self.text_edit, 1)
        central_layout.addWidget(self.find_panel, 0)

        self.setCentralWidget(central_widget)

        # ---- Barra de estado ----
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Componente reutilizable para conteo de palabras/caracteres
        self.word_counter = WordCounterWidget(
            wpm=200,
            mostrarPalabras=True,
            mostrarCaracteres=True,
            mostrarTiempoLectura=True
        )
        self.cursor_label = QLabel("Línea: 1, Columna: 1")  # funcionalidad extra
        self.status_bar.addPermanentWidget(self.word_counter)
        self.status_bar.addPermanentWidget(self.cursor_label)

        # Conexiones para contador de palabras y posición del cursor
        self.text_edit.textChanged.connect(self._on_text_changed)
        self.text_edit.cursorPositionChanged.connect(self.update_cursor_position)
        
        # Conectar señal del componente (ejemplo de uso)
        self.word_counter.conteoActualizado.connect(self._on_conteo_actualizado)

        # Crear acciones, menús y barra de herramientas
        self.create_actions()
        self.create_menus()
        self.create_toolbar()

        # Voice worker
        self.voice_worker = None


    # ================== Acciones ==================
    def create_actions(self):
        # Archivo
        self.new_action = QAction("Nuevo", self)
        self.new_action.setShortcut(QKeySequence.StandardKey.New)
        self.new_action.triggered.connect(self.new_file)
        # --- control de teclado para crear nuevo archivo ---
        self.new_action.setShortcut("Ctrl+N");
        

        self.open_action = QAction("Abrir", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.open_action.triggered.connect(self.open_file)
        # --- control de teclado para abrir archivo ---
        self.open_action.setShortcut("Ctrl+O");

        self.save_action = QAction("Guardar", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_action.triggered.connect(self.save_file)
        # --- control de teclado para guardar archivo ---
        self.save_action.setShortcut("Ctrl+S"); # Ctrl+S para guardar

        self.exit_action = QAction("Salir", self)
        self.exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        self.exit_action.triggered.connect(self.close)
        # --- control de teclado para salir ---
        self.exit_action.setShortcut("Ctrl+Q"); # Ctrl+Q para salir

        # Editar
        self.undo_action = QAction("Deshacer", self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.triggered.connect(self.text_edit.undo)
        # --- control de teclado para deshacer ---
        self.undo_action.setShortcut("Ctrl+Z"); # Ctrl+Z para deshacer
        

        self.redo_action = QAction("Rehacer", self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.triggered.connect(self.text_edit.redo)
        # --- control de teclado para rehacer ---
        self.redo_action.setShortcut("Ctrl+Y"); # Ctrl+Y para rehacer

        self.cut_action = QAction("Cortar", self)
        self.cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        self.cut_action.triggered.connect(self.text_edit.cut)
        # --- control de teclado para cortar ---
        self.cut_action.setShortcut("Ctrl+X"); # Ctrl+X para cortar

        self.copy_action = QAction("Copiar", self)
        self.copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        self.copy_action.triggered.connect(self.text_edit.copy)
        # --- control de teclado para copiar ---
        self.copy_action.setShortcut("Ctrl+C"); # Ctrl+C para copiar

        self.paste_action = QAction("Pegar", self)
        self.paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        self.paste_action.triggered.connect(self.text_edit.paste)
        # --- control de teclado para pegar ---
        self.paste_action.setShortcut("Ctrl+V"); # Ctrl+V para pegar

        # Buscar / Reemplazar (ahora activan el panel lateral)
        self.find_action = QAction("Buscar", self)
        self.find_action.setShortcut(QKeySequence.StandardKey.Find)
        self.find_action.triggered.connect(self.find_text)
        # --- control de teclado para buscar ---
        self.find_action.setShortcut("Ctrl+F"); # Ctrl+F para buscar
        

        self.replace_action = QAction("Reemplazar", self)
        self.replace_action.setShortcut("Ctrl+H")
        self.replace_action.triggered.connect(self.replace_text)

        # Personalización
        self.bgcolor_action = QAction("Color de fondo", self)
        self.bgcolor_action.triggered.connect(self.change_background_color)

        self.font_action = QAction("Tipo de letra", self)
        self.font_action.triggered.connect(self.change_font)

        self.voice_action = QAction("Activar Voz", self)
        self.voice_action.setCheckable(True)
        self.voice_action.triggered.connect(self.toggle_voice_control)


    # ================== Menús ==================
    def create_menus(self):
        menu_bar = self.menuBar()

        # Menú Archivo
        file_menu = menu_bar.addMenu("Archivo")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # Menú Editar
        edit_menu = menu_bar.addMenu("Editar")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.find_action)
        edit_menu.addAction(self.replace_action)

        # Menú Formato / Personalización
        format_menu = menu_bar.addMenu("Formato")
        format_menu.addAction(self.bgcolor_action)
        format_menu.addAction(self.font_action)

    # ================== Barra de herramientas ==================
    def create_toolbar(self):
        toolbar = QToolBar("Barra de herramientas")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.undo_action)
        toolbar.addAction(self.redo_action)
        toolbar.addSeparator()
        toolbar.addAction(self.cut_action)
        toolbar.addAction(self.copy_action)
        toolbar.addAction(self.paste_action)
        toolbar.addSeparator()
        toolbar.addAction(self.find_action)
        toolbar.addAction(self.replace_action)
        toolbar.addSeparator()
        toolbar.addAction(self.voice_action)

    # ================== Funciones Archivo ==================
    def new_file(self):
        self.text_edit.clear()
        self.current_file = None
        self.status_bar.showMessage("Nuevo documento", 3000)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Abrir archivo", "", "Archivos de texto (*.txt);;Todos (*.*)"
        )
        if file_name:
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    text = f.read()
                self.text_edit.setPlainText(text)
                self.current_file = file_name
                self.status_bar.showMessage(f"Archivo abierto: {file_name}", 3000)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo abrir el archivo:\n{e}")

    def save_file(self):
        if self.current_file is None:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Guardar archivo", "", "Archivos de texto (*.txt);;Todos (*.*)"
            )
            if not file_name:
                return
            self.current_file = file_name

        try:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text_edit.toPlainText())
            self.status_bar.showMessage("Archivo guardado con éxito", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar el archivo:\n{e}")

    # ================== Buscar / Reemplazar (activa panel) ==================
    def find_text(self):
        self.find_panel.find_edit.setFocus()
        self.find_panel.find_edit.selectAll()
        self.status_bar.showMessage("Panel de búsqueda activo", 2000)

    def replace_text(self):
        self.find_panel.replace_edit.setFocus()
        self.find_panel.replace_edit.selectAll()
        self.status_bar.showMessage("Panel de reemplazo activo", 2000)

    # ================== Color de fondo ==================
    def change_background_color(self):
        color = QColorDialog.getColor(
            self.text_edit.palette().base().color(), self, "Elegir color de fondo"
        )
        if color.isValid():
            palette = self.text_edit.palette()
            palette.setColor(self.text_edit.viewport().backgroundRole(), color)
            self.text_edit.setPalette(palette)
            self.status_bar.showMessage("Color de fondo cambiado", 3000)

    def change_font(self):
        font, ok = QFontDialog.getFont(self.text_edit.font(), self, "Elegir tipo de letra")
        if ok:
            self.text_edit.setFont(font)
            self.status_bar.showMessage("Fuente cambiada", 3000)

    # ================== Contador de palabras (usando componente reutilizable) ==================
    def _on_text_changed(self):
        """Slot que actualiza el contador cuando cambia el texto."""
        text = self.text_edit.toPlainText()
        self.word_counter.update_from_text(text)
    
    def _on_conteo_actualizado(self, palabras: int, caracteres: int):
        """Slot que recibe la señal conteoActualizado del WordCounterWidget."""
        # Aquí se puede usar la información emitida por la señal si es necesario
        pass

    # ================== Línea y columna  ==================
    def update_cursor_position(self):
        cursor = self.text_edit.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        self.cursor_label.setText(f"Línea: {line}, Columna: {column}")

    # ================== Control de Voz ==================
    def toggle_voice_control(self, checked):
        if checked:
            self.status_bar.showMessage("Iniciando reconocimiento de voz...", 2000)
            self.voice_worker = VoiceWorker(self)
            self.voice_worker.recognized_text.connect(self.handle_voice_command)
            self.voice_worker.error.connect(lambda e: self.status_bar.showMessage(e, 5000))
            self.voice_worker.start()
            self.voice_action.setText("Desactivar Voz")
            self.voice_action.setIcon(QIcon.fromTheme("microphone-sensitivity-high")) # Icono genérico si existe
        else:
            if self.voice_worker:
                self.voice_worker.stop()
                self.voice_worker = None
            self.voice_action.setText("Activar Voz")
            self.status_bar.showMessage("Reconocimiento de voz detenido", 2000)

    def handle_voice_command(self, text):
        self.status_bar.showMessage(f"Voz detectada: {text}", 3000)
        
        # Comandos
        if "negrita" in text:
            fmt = self.text_edit.fontWeight()
            new_weight = QFont.Bold if fmt != QFont.Bold else QFont.Normal
            self.text_edit.setFontWeight(new_weight)
        
        elif "cursiva" in text:
            self.text_edit.setFontItalic(not self.text_edit.fontItalic())
            
        elif "subrayado" in text:
            self.text_edit.setFontUnderline(not self.text_edit.fontUnderline())
            
        elif "guardar archivo" in text:
            self.save_file()
            
        elif "nuevo documento" in text:
            self.new_file()


def main():
    app = QApplication(sys.argv)
    window = MiniWord()
    window.resize(900, 600)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()