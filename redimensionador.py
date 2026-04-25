from PIL import Image
import os

def redimensionar_imagen(ruta_entrada, ancho=128, alto=64, ruta_salida=None):
    """
    Redimensiona una imagen permitiendo especificar ancho, alto o ambos.
    """
    try:
        with Image.open(ruta_entrada) as img:
            ancho_org, alto_org = img.size
            
            # Lógica de dimensiones
            if ancho and alto:
                # Redimensión forzada a medidas específicas
                nuevas_dims = (ancho, alto)
            elif ancho:
                # Proporcional basado en el ancho
                prop = ancho / float(ancho_org)
                nuevas_dims = (ancho, int(float(alto_org) * prop))
            elif alto:
                # Proporcional basado en el alto
                prop = alto / float(alto_org)
                nuevas_dims = (int(float(ancho_org) * prop), alto)
            else:
                print("⚠️ Debes especificar al menos una dimensión.")
                return None

            # Procesamiento
            img_final = img.resize(nuevas_dims, Image.Resampling.LANCZOS)

            # Gestión de ruta de salida
            if not ruta_salida:
                nombre, ext = os.path.splitext(ruta_entrada)
                ruta_salida = f"{nombre}_{nuevas_dims[0]}x{nuevas_dims[1]}{ext}"

            img_final.save(ruta_salida)
            print(f"✅ Éxito: {ruta_salida} [{nuevas_dims[0]}x{nuevas_dims[1]}]")
            return ruta_salida

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Ejemplos de uso:
if __name__ == "__main__":
    # 1. Ancho y alto específicos (puede deformar si no es la misma proporción)
    redimensionar_imagen("gato-11.jpg", ancho=128, alto=64)
    
    # 2. Solo ancho (mantiene proporción)
    # redimensionar_imagen("foto.jpg", ancho=800)