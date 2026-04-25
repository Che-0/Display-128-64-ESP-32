from machine import Pin, I2C
from libs import sh1106
import framebuf

# Configuración fija
WIDTH = 128
HEIGHT = 64

def inicializar_pantalla():
    # Inicializar I2C (ajusta los pines si es necesario)
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000) # Subí a 400kHz para más fluidez
    oled = sh1106.SH1106_I2C(WIDTH, HEIGHT, i2c)
    return oled

def dibujar_bitmap(oled, byte_data, w=128, h=64):
    """
    Recibe el objeto oled y el bytearray de la imagen.
    """
    oled.fill(0) # Limpiar buffer
    
    # IMPORTANTE: Asegúrate de que el formato coincida con tu generador
    # Si la imagen sale rara, cambia MONO_HLSB por MONO_HMSB
    fb = framebuf.FrameBuffer(bytearray(byte_data), w, h, framebuf.MONO_HLSB)
    
    oled.blit(fb, 0, 0)
    oled.show()

# Así podrías usarlo en tu main de MicroPython:
# import mostrar
# oled = mostrar.inicializar_pantalla()
# mostrar.dibujar_bitmap(oled, mi_array_de_bytes)