# 🖥️ Display 128x64 — ESP32 Image Converter

Herramienta en Python para convertir imágenes a byte arrays compatibles con displays OLED SH1106 de 128×64 px conectados a un ESP32 vía I2C.

---

## ¿Qué hace este proyecto?

Toma cualquier imagen (JPG, PNG, etc.), la redimensiona al tamaño exacto del display (128×64 px) y la convierte a un array de bytes en formato hexadecimal listo para copiar y usar directamente en Arduino/MicroPython.

```
imagen.jpg  →  [redimensionar]  →  imagen_128x64.jpg  →  [convertir]  →  0xFF, 0x00, 0x1A, ...
```

---

## 📁 Estructura del proyecto

```
Display-128-64-ESP-32/
│
├── main.py                # Punto de entrada — orquesta el flujo completo
├── redimensionador.py     # Módulo: redimensiona imágenes con PIL
├── image_to_c_array.py    # Módulo: convierte imagen a byte array hex
├── mostrar.py             # Módulo: dibuja el bitmap en el display (MicroPython)
├── procesador_lotes.py    # Procesamiento de múltiples imágenes en lote
├── libreria_imagenes.py   # Librería de imágenes pregeneradas
├── fast_test.py           # Tests rápidos sin inputs manuales
├── test_main.py           # Suite de tests con unittest
└── cat-*.jpg / gato-*.jpg # Imágenes de ejemplo
```

---

## ⚙️ Flujo de funcionamiento

```
┌─────────────┐     ┌──────────────────┐     ┌───────────────────┐     ┌──────────────┐
│  imagen.jpg │────▶│ redimensionador  │────▶│ image_to_c_array  │────▶│  Byte Array  │
│  (entrada)  │     │  128 × 64 px     │     │  formato hex      │     │  para OLED   │
└─────────────┘     └──────────────────┘     └───────────────────┘     └──────────────┘
                                                                               │
                                                                               ▼
                                                                    ┌──────────────────┐
                                                                    │    mostrar.py     │
                                                                    │  (en MicroPython) │
                                                                    └──────────────────┘
```

---

## 🧩 Descripción de módulos

### `redimensionador.py`
Redimensiona una imagen usando la librería **Pillow** con el algoritmo LANCZOS (alta calidad).

- Soporta redimensión forzada (`ancho` + `alto`) o proporcional (solo uno de los dos).
- Genera automáticamente el nombre del archivo de salida: `imagen_128x64.jpg`.
- Devuelve la ruta del archivo generado para encadenarlo con el siguiente paso.

```python
from redimensionador import redimensionar_imagen

ruta = redimensionar_imagen("foto.jpg", ancho=128, alto=64)
# → guarda "foto_128x64.jpg" y retorna esa ruta
```

---

### `image_to_c_array.py`
Convierte la imagen redimensionada a un string de bytes hexadecimales en formato Arduino.

- Convierte la imagen a modo **1-bit (blanco/negro puro)**.
- Procesa los píxeles con **MSB First** (bit más significativo primero).
- Soporta inversión de colores con el parámetro `invertir=True`.
- Retorna el código generado, el ancho y el alto.

```python
from image_to_c_array import imagen_a_byte_array

codigo, w, h = imagen_a_byte_array("foto_128x64.jpg")
print(f"const unsigned char bitmap_{w}x{h} [] PROGMEM = {{")
print(codigo)
print("};")
```

**Salida de ejemplo:**
```c
const unsigned char bitmap_128x64 [] PROGMEM = {
  0xff, 0x00, 0x1a, 0xf3, ...
};
```

---

### `mostrar.py`
Módulo MicroPython que corre **en el ESP32** para dibujar el bitmap en la pantalla OLED.

- Inicializa la comunicación I2C (pines SDA=21, SCL=22, frecuencia 400kHz).
- Usa el driver `sh1106` para controlar el display.
- Dibuja el bitmap con `framebuf.FrameBuffer` en modo `MONO_HLSB`.

```python
# En tu script de MicroPython (ESP32)
import mostrar

oled = mostrar.inicializar_pantalla()
mostrar.dibujar_bitmap(oled, mi_array_de_bytes)
```

> **Nota:** si la imagen aparece invertida, cambia `MONO_HLSB` por `MONO_HMSB` en `mostrar.py`.

---

### `main.py`
Orquesta el flujo completo de forma interactiva.

```
[1/3] Redimensionando imagen...
[2/3] Convirtiendo a Byte Array...
[3/3] ¡Proceso completado! → 128x64
```

---

## 🚀 Uso rápido

### 1. Instalar dependencias

```bash
pip install pillow
```

### 2. Ejecutar el flujo completo

```bash
python main.py
```

El programa pedirá:
- Nombre del archivo imagen (ej. `gato.jpg`)
- Ancho deseado (ej. `128`)
- Alto deseado (ej. `64`)
- Si deseas imprimir el código en pantalla (`s/n`)

### 3. Copiar el output a tu sketch de Arduino/MicroPython

Pega el array generado en tu código:

```c
// En Arduino
#include <Adafruit_SSD1306.h>

const unsigned char bitmap_128x64 [] PROGMEM = {
  0xff, 0x00, ...
};

display.drawBitmap(0, 0, bitmap_128x64, 128, 64, WHITE);
```

---

## 🧪 Tests

El proyecto incluye una suite de tests con `unittest` que simula los inputs automáticamente sin necesidad de interacción manual.

```bash
python -m unittest test_main -v
```

Para tests rápidos sin mocks:

```bash
python fast_test.py
```

---

## 🔧 Hardware compatible

| Componente | Especificación |
|---|---|
| Microcontrolador | ESP32 (cualquier variante) |
| Display | OLED SH1106 128×64 px |
| Protocolo | I2C |
| Pin SDA | GPIO 21 |
| Pin SCL | GPIO 22 |
| Frecuencia I2C | 400 kHz |

---

## 📦 Dependencias

| Librería | Entorno | Uso |
|---|---|---|
| `Pillow` | Python (PC) | Redimensionar e procesar imágenes |
| `machine` | MicroPython (ESP32) | Control de pines I2C |
| `sh1106` | MicroPython (ESP32) | Driver del display OLED |
| `framebuf` | MicroPython (ESP32) | Buffer de imagen para dibujar |
| `unittest` | Python (PC) | Tests automatizados |

---

## 🌐 Recursos que me ayudaron

Estas herramientas fueron clave durante el desarrollo del proyecto y las recomiendo si quieres experimentar con imágenes en displays OLED:

| Herramienta | Descripción |
|---|---|
| [image2cpp — javl.github.io](https://javl.github.io/image2cpp/) | Conversor online de imagen a byte array para Arduino. Muy útil para verificar y comparar resultados con los generados por este proyecto. |
| [iLoveIMG](https://www.iloveimg.com/es) | Suite online de edición y conversión de imágenes. Fue de gran ayuda para preparar imágenes antes de procesarlas. |

> Parte de la lógica de conversión de este proyecto se inspiró en explorar cómo funcionan estas herramientas por dentro.

---

## 🤝 Agradecimientos

Este proyecto no hubiera salido igual sin la ayuda de:

- **[Google Gemini](https://gemini.google.com/)** — apoyo durante las primeras etapas del desarrollo, exploración de ideas y resolución de dudas iniciales.
- **[Claude (Anthropic)](https://claude.ai/)** — ayuda con la estructura del código, generación de tests automatizados y redacción de este README.

> Dos IAs, un display, y muchas horas de prueba y error. 🤖

---

## 📝 Licencia

Este proyecto es de uso libre para fines educativos y de prototipado.
