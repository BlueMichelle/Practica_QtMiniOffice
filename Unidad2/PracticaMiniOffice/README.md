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
- **Contador de palabras** en tiempo real
- **Línea y columna del cursor** (funcionalidad extra)

### Control por Voz (funcionalidad extra)
- Activar/desactivar reconocimiento de voz
- Comandos: "negrita", "cursiva", "subrayado", "guardar archivo", "nuevo documento"

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
