from PIL import Image

def imagen_a_byte_array(ruta_imagen, invertir=False):
    """
    Convierte una imagen a un array de bytes en formato hexadecimal (Arduino style).
    """
    try:
        # Abrimos la imagen y la convertimos a modo 1-bit (blanco y negro puro)
        with Image.open(ruta_imagen) as img:
            img = img.convert('1') 
            ancho, alto = img.size
            datos = list(img.getdata())

            byte_array = []
            byte_actual = 0
            contador_bits = 0

            for pixel in datos:
                # En modo '1', 255 es blanco y 0 es negro. 
                # Ajustamos la lógica según si queremos invertir la imagen.
                bit = 1 if pixel > 0 else 0
                if invertir:
                    bit = 1 - bit

                # Vamos construyendo el byte (MSB First - el primer bit es el más significativo)
                byte_actual = (byte_actual << 1) | bit
                contador_bits += 1

                # Cuando completamos 8 bits, lo guardamos y reseteamos
                if contador_bits == 8:
                    byte_array.append(f"0x{byte_actual:02x}")
                    byte_actual = 0
                    contador_bits = 0

            # Si quedaron bits sueltos al final de una fila
            if contador_bits > 0:
                byte_actual <<= (8 - contador_bits)
                byte_array.append(f"0x{byte_actual:02x}")

            # Formatear la salida como texto para Arduino
            salida_formateada = ", ".join(byte_array)
            return salida_formateada, ancho, alto

    except Exception as e:
        return f"Error: {e}", 0, 0

# --- Ejemplo de uso ---
if __name__ == "__main__":
    codigo, w, h = imagen_a_byte_array("gato-1.jpg")
    print(f"// Imagen de {w}x{h} píxeles")
    print(f"const unsigned char mi_imagen [] PROGMEM = {{")
    print(codigo)
    print("};")