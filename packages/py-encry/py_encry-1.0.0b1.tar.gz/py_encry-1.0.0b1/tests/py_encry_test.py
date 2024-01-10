import unittest
from src.pyencry.image_handler import ImageHandler 

class PyEncryTests(unittest.TestCase):
    def test_can_encode_picture_with_rail_fence(self):
        image_handler = ImageHandler("./img/d.png")
        image_handler.encode("rail_fence_cipher", data="This is a secret message", key=4)
        image_handler.write("./img/test_encoded.png")
        self.assertTrue(self.__compare_files("./img/test_encoded.png", "./img/test_encoded_rail_fence.png"))

    def test_can_encode_picture_with_random_spacing(self):
        image_handler = ImageHandler("./img/d.png")
        image_handler.encode("random_spacing", data="This is a secret message", key=4)
        image_handler.write("./img/test_encoded.png")
        self.assertTrue(self.__compare_files("./img/test_encoded.png", "./img/test_encoded_random_spacing.png"))

    def test_can_encode_then_decode_with_rail_fence(self):
        image_handler = ImageHandler("./img/d.png")
        image_handler.encode("rail_fence_cipher", data="This is a secret message", key=4)
        image_handler.write("./img/test_encoded.png")
        image_handler = ImageHandler("./img/test_encoded.png")
        self.assertEqual(image_handler.decode("rail_fence_cipher", key=4), "This is a secret message")

    def test_can_encode_then_decode_with_random_spacing(self):
        image_handler = ImageHandler("./img/d.png")
        image_handler.encode("random_spacing", data="This is a secret message", key=4)
        image_handler.write("./img/test_encoded.png")
        image_handler = ImageHandler("./img/test_encoded.png")
        self.assertEqual(image_handler.decode("random_spacing", key=4), "This is a secret message")

    def __compare_files(self, file1, file2):
        with open(file1, "rb") as f1:
            with open(file2, "rb") as f2:
                return f1.read() == f2.read()
