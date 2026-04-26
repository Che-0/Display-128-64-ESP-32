import os
import redimensionador
import image_to_c_array

#Este es un programa meeeeenos interactivo
#Busca las imagenes que estan en el directorio, las redimenciona, las hace strings de bytearray y despues genera un 
#archivo de python  que contiene una lista con los arrays

def procesar_todo(ancho=128, alto=64, archivo_salida="libreria_imagenes.py"):
    # Extensiones compatibles
    extensiones = ('.jpg', '.jpeg', '.png', '.bmp')
    
    # Filtrar archivos en el directorio actual
    imagenes = [f for f in os.listdir('.') if f.lower().endswith(extensiones)]
    
    if not imagenes:
        print("📭 No se encontraron imágenes en la carpeta actual.")
        return

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write("# Archivo generado automáticamente\n")
        f.write("# Formato: MONO_HLSB (ajusta según tu framebuf)\n\n")
        
        for nombre_img in imagenes:
            print(f"📦 Procesando: {nombre_img}...")
            
            # 1. Redimensionar (usamos una carpeta temporal o nombres fijos)
            img_temp = redimensionador.redimensionar_imagen(nombre_img, ancho, alto)
            
            if img_temp:
                # 2. Convertir a Array
                codigo, w, h = image_to_c_array.imagen_a_byte_array(img_temp)
                
                # 3. Crear un nombre de variable válido (sin puntos ni guiones)
                var_name = os.path.splitext(nombre_img)[0].replace("-", "_").replace(" ", "_")
                
                # 4. Escribir en el archivo con formato MicroPython
                f.write(f"{var_name} = bytearray([\n{codigo}\n])\n\n")
                
                # Opcional: borrar la imagen redimensionada temporal para no llenar la carpeta
                if img_temp != nombre_img:
                    os.remove(img_temp)
                    
    print(f"\n✅ ¡Listo! Se han procesado {len(imagenes)} imágenes.")
    print(f"📄 Los arrays están en: {archivo_salida}")

if __name__ == "__main__":
    procesar_todo()