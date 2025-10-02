# bots

## Login bot

El script `login_bot.py` abre la página de inicio de sesión de CEDSa Postítulos,
carga el usuario y la contraseña desde un archivo de texto y presiona el botón
**Acceder**. Luego ingresa a la página principal de Postítulos, espera 10
segundos y abre la diplomatura **“DIPLOMATURA SUPERIOR EN PROGRAMACIÓN Y
ROBÓTICA | 2DO INICIO 2025”**.

### Requisitos

- Python 3.9 o superior
- [Google Chrome](https://www.google.com/chrome/)
- Paquetes de Python: `selenium` y `webdriver-manager`

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

### Archivo de credenciales

Crea un archivo de texto (por ejemplo, `credentials.txt`) con el siguiente
formato:

```
username=tu_usuario
password=tu_contraseña
```

Puedes usar `credentials.example.txt` como plantilla.

### Uso

```bash
python login_bot.py credentials.txt
```

El script se ejecuta en modo *headless* (sin ventana) por defecto. Para ver el
navegador mientras se ejecuta, usa:

```bash
python login_bot.py credentials.txt --show
```
