# Practica Qt Mini Office

Mini Word desarrollado en Python con PySide6 (Qt6).

## Ejecutable

📁 **Ubicación del .exe:** `dist/MiniWord.exe`

El ejecutable está listo para usar, solo hay que ejecutar el archivo `MiniWord.exe` ubicado en la carpeta `dist`.

## Funcionalidades

### Menú Archivo
- **Nuevo** (Ctrl+N): Crear documento vacío
- **Abrir** (Ctrl+O): Abrir archivos de texto (.txt)
- **Guardar** (Ctrl+S): Guardar documento actual
- **Salir** (Ctrl+Q): Cerrar la aplicación

### Menú Editar
- **Deshacer** (Ctrl+Z) / **Rehacer** (Ctrl+Y)
- **Cortar** (Ctrl+X) / **Copiar** (Ctrl+C) / **Pegar** (Ctrl+V)
- **Buscar** (Ctrl+F) / **Reemplazar** (Ctrl+H)

### Menú Formato
- Cambio de **color de fondo** del área de texto
- Cambio de **tipo de letra**

### Panel Buscar/Reemplazar
- Buscar siguiente / anterior / todas las coincidencias
- Reemplazar una / todas las coincidencias

### Barra de Estado
- Mensajes informativos
- **Contador de palabras y caracteres** en tiempo real (componente reutilizable)
- **Tiempo estimado de lectura**
- **Línea y columna del cursor** (funcionalidad extra)

### Control por Voz (funcionalidad extra)
- Activar/desactivar reconocimiento de voz
- Comandos: "negrita", "cursiva", "subrayado", "guardar archivo", "nuevo documento"

---

## Documentación de Señales (Qt Signals)

Esta sección documenta las señales utilizadas en la aplicación siguiendo el patrón Signal-Slot de Qt.

### VoiceWorker

Clase que maneja el reconocimiento de voz en un hilo separado.

| Señal | Parámetros | Descripción |
|-------|------------|-------------|
| `recognized_text` | `str` | Emitida cuando se reconoce texto por voz. El parámetro contiene el texto reconocido en minúsculas. |
| `error` | `str` | Emitida cuando ocurre un error en el reconocimiento. El parámetro contiene el mensaje de error. |

**Ejemplo de conexión:**
```python
self.voice_worker.recognized_text.connect(self.handle_voice_command)
self.voice_worker.error.connect(lambda e: self.status_bar.showMessage(e, 5000))
```

### WordCounterWidget (Componente Reutilizable)

Widget reutilizable para contar palabras, caracteres y estimar tiempo de lectura.

| Señal | Parámetros | Descripción |
|-------|------------|-------------|
| `conteoActualizado` | `int, int` | Emitida cada vez que se actualiza el conteo. Primer parámetro: número de palabras. Segundo parámetro: número de caracteres. |

**Parámetros del constructor:**
- `wpm` (int): Palabras por minuto para calcular tiempo de lectura (default: 200)
- `mostrarPalabras` (bool): Mostrar contador de palabras (default: True)
- `mostrarCaracteres` (bool): Mostrar contador de caracteres (default: True)
- `mostrarTiempoLectura` (bool): Mostrar tiempo estimado de lectura (default: True)

**Métodos públicos:**
- `update_from_text(text: str)`: Actualiza los contadores con el texto proporcionado y emite la señal `conteoActualizado`.

**Ejemplo de uso:**
```python
from WordCounterWidget import WordCounterWidget

# Crear el widget
self.word_counter = WordCounterWidget(
    wpm=200,
    mostrarPalabras=True,
    mostrarCaracteres=True,
    mostrarTiempoLectura=True
)

# Conectar señal a un slot
self.word_counter.conteoActualizado.connect(self._on_conteo_actualizado)

# Actualizar desde el texto
self.text_edit.textChanged.connect(lambda: self.word_counter.update_from_text(self.text_edit.toPlainText()))

# Slot que recibe la señal
def _on_conteo_actualizado(self, palabras: int, caracteres: int):
    print(f"Palabras: {palabras}, Caracteres: {caracteres}")
```

### Diagrama de Flujo de Señales

```
┌─────────────────┐     textChanged      ┌──────────────────────┐
│    QTextEdit    │ ──────────────────►  │  _on_text_changed()  │
└─────────────────┘                      └──────────┬───────────┘
                                                    │
                                                    ▼
                                         ┌──────────────────────┐
                                         │ WordCounterWidget    │
                                         │ update_from_text()   │
                                         └──────────┬───────────┘
                                                    │
                                          conteoActualizado(int, int)
                                                    │
                                                    ▼
                                         ┌──────────────────────┐
                                         │ _on_conteo_actualizado│
                                         │ (palabras, caracteres)│
                                         └──────────────────────┘
```

---

## Ejecución desde código fuente

```bash
python main.py
```

## Generar ejecutable

```bash
pyinstaller MiniWord.spec
```

## Dependencias

- PySide6
- SpeechRecognition (para control por voz)
- PyInstaller (para generar .exe)

## Estructura del Proyecto

```
PracticaMiniOffice/
├── QT6_9MiniOffiPraFi.py    # Aplicación principal MiniWord
├── WordCounterWidget.py      # Componente reutilizable de conteo
├── main.py                   # Punto de entrada
├── dist/
│   └── MiniWord.exe          # Ejecutable
└── README.md                 # Esta documentación
```
