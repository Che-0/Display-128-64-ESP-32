import unittest
from unittest.mock import patch
import main  # tu archivo principal

class TestEjecutarProyecto(unittest.TestCase):

    @patch("main.redimensionador.redimensionar_imagen", return_value="test_img_128x64.jpg")
    @patch("main.image_to_c_array.imagen_a_byte_array", return_value=("0xFF, 0x00", 128, 64))
    @patch("builtins.input", side_effect=[
        "test_img.jpg",  # nombre de imagen
        "128",           # ancho
        "64",            # alto
        "n"              # NO imprimir el código
    ])
    def test_flujo_completo(self, mock_input, mock_conversor, mock_redim):
        """Prueba el flujo completo sin impresión del byte array"""
        main.ejecutar_proyecto()

        # Verifica que se llamó redimensionar con los args correctos
        mock_redim.assert_called_once_with("test_img.jpg", 128, 64)

        # Verifica que se llamó el conversor con la imagen redimensionada
        mock_conversor.assert_called_once_with("test_img_128x64.jpg")

if __name__ == "__main__":
    unittest.main()