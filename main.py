import image_to_c_array
import redimensionador
#import mostrar

def ejecutar_proyecto():
    print("--- Generador de Byte Arrays para Arduino ---")
    
    # 1. Entrada dinámica
    imagen_objetivo = input("Introduce el nombre de la imagen (ej. gato.jpg): ")
    ancho = int(input("Introduce el ancho deseado: "))
    alto = int(input("Introduce el alto deseado: "))

    print(f"\n[1/3] Redimensionando {imagen_objetivo}...")
    
    # 2. Redimensionamos y CAPTURAMOS el nombre del nuevo archivo
    # La función nos devuelve la ruta exacta, ej: "gato_128x64.jpg"
    imagen_procesada = redimensionador.redimensionar_imagen(imagen_objetivo, ancho, alto)

    if imagen_procesada:
        print(f"[2/3] Convirtiendo {imagen_procesada} a Byte Array...")
        
        # 3. Usamos la variable anterior para la conversión
        codigo, w, h = image_to_c_array.imagen_a_byte_array(imagen_procesada)
        
        print(f"\n[3/3] ¡Proceso completado con éxito!")
        print(f"Dimensiones finales: {w}x{h}")
        
        # 4. Mostrar o guardar resultado
        opcion = input("\n¿Deseas imprimir el código en pantalla? (s/n): ")
        if opcion.lower() == 's':
            print("-" * 50)
            print(f"const unsigned char bitmap_{w}x{h} [] PROGMEM = {{")
            print(codigo)
            print("};")
            print("-" * 50)
            #oled = mostrar.inicializar_pantalla()
            #mostrar.dibujar_bitmap(oled, codigo)
    else:
        print("❌ Hubo un error en el primer paso. Revisa que el archivo existe.")

if __name__ == "__main__":
    ejecutar_proyecto()