import image_to_c_array
import redimensionador
import mostrar

print("""
      
    explicación
      
      
      
      """)

imagen_objetivo = "gato-11.jpg"

#primero redimensionamos la imagen
redimensionador.redimensionar_imagen(imagen_objetivo, 128, 64)
#Esto generara una imagen redimensionada en la carpeta en la que se ejecuto o puedes especificar una ruta de salida
#la imagen redimensionada se guardara con el nombre "imagen_128x64.jpg" 128x64 variara dependiendo de la proporción que pongas

#Despues de redimensionar, podemos convertir la imagen a un array C para usarlo en nuestro código
codigo, w, h = image_to_c_array.imagen_a_byte_array("gato-11_128x64.jpg")
# print(f"Array C generado: {codigo}")
mostrar.mostrar_imagen(codigo)