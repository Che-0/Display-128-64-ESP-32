from machine import Pin, I2C
from libs import sh1106
import framebuf



def mostrar_imagen(img_array):
    # Configuración de la pantalla
    WIDTH = 128
    HEIGHT = 64

    # Inicializar I2C
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=200000)

    # Inicializar pantalla OLED
    oled = sh1106.SH1106_I2C(WIDTH, HEIGHT, i2c)

    # Limpiar la pantalla
    oled.fill(0)

    # Crear datos para una imagen de 128x64 píxeles
    image_data = bytearray([img_array])

    # Crear FrameBuffer para la imagen
    image_width = 128
    image_height = 64
    image_fb = framebuf.FrameBuffer(image_data, image_width, image_height, framebuf.MONO_HLSB)

    # Dibujar la imagen en la posición (x, y)
    x_pos = 0  # Comienza en el borde izquierdo
    y_pos = 0
    oled.blit(image_fb, x_pos, y_pos)

    # Actualizar la pantalla
    oled.show()