from PIL import Image, ImageSequence
import base64

class ImageHandler:
    """A class to handle images for cryptography

    Attributes
    ----------
    image : Image - The parsed image

    Methods
    -------
    write(file_path): Writes the image data to a file
    file_info(): Gets the file information of the image
    encode(method, **kwargs): Encodes data into the image
    decode(method, **kwargs): Decodes data from the image
    """

    def __init__(self, file_path):
        """Initialise the ImageHandler class

        arguments:
        - file_path - string - The path to the file to parse

        returns:
        - ImageHandler - The ImageHandler object

        example:
        ```
        image_handler = ImageHandler("./img/TechSmith-Blog-JPGvsPNG-DE.png")
        ```
        """

        self.image = Image.open(file_path)
        image_info = self.file_info()
        if image_info["format"] != "PNG":
            raise ValueError("Image must be in PNG format")

    @classmethod
    def from_base64(cls, base64_string):
        """Initialise the ImageHandler class from a string

        arguments:
        - base64_string - string - The string to parse

        returns:
        - ImageHandler - The ImageHandler object

        example:
        ```
        with open("./img/TechSmith-Blog-JPGvsPNG-DE.png", "rb") as file:
            image_handler = ImageHandler.from_base64(file.read())
        ```
        """

        return cls(BytesIO(base64_string))

    def write(self, file_path):
        """Write to the image data to a file

        arguments:
        - file_path - string - The path to the file to write to

        returns:
        - no-return

        example:
        ```
        image_handler = ImageHandler("./img/TechSmith-Blog-JPGvsPNG-DE.png")

        image_handler.write("./img/test.png")
        ```
        """

        self.image.save(file_path, format="PNG")

    def to_string(self):
        """Write to the image data to a string

        returns:
        - string - The image data

        example:
        ```
        image_handler = ImageHandler("./img/TechSmith-Blog-JPGvsPNG-DE.png")

        image_handler.to_string()
        ```
        """

        buffer = BytesIO()
        self.image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue())

    def file_info(self):
        """Get the file information of the image

        The information returned is:
        - mode: The mode of the image
        - size: The size of the image
        - format: The format of the image
        - filename: The filename of the image

        returns:
        - dict - The file information

        example:
        ```
        image_handler = ImageHandler("./img/TechSmith-Blog-JPGvsPNG-DE.png")

        image_handler.file_info()
        ```
        """

        filename = ""
        if not self.image.filename:
            filename = None
        else:
            filename = self.image.filename

        return {"mode": self.image.mode, "size": self.image.size, "format": self.image.format, "filename": filename}

    def encode(self, method, **kwargs):
        """Encode data into the image

        The method allows selecting the method to use to encode the data, and
        it accepts keyword arguments to pass to the method. The keywords are:
        - data: The data to encode
        - key: The key to use to encode the data

        The method raises a NotImplementedError if the method is not implemented.

        arguments:
        - method - string - The method to use to encode the data
        - kwargs - dict - The arguments to pass to the method

        returns:
        - no-return

        example:
        ```
        image_handler = ImageHandler("./img/TechSmith-Blog-JPGvsPNG-DE.png")

        image_handler.encode("rail_fence_cipher", data="This is a secret message", key=4)
        ```
        """
        match method:
            case "rail_fence_cipher":
                info = self.file_info()
                enumerator = get_rail_fence_pixels(info["size"][0], info["size"][1], kwargs["key"])
                encoded_data = encode_rail_fence_cipher(kwargs["data"], kwargs["key"])
                for (idx, pixel) in enumerate(enumerator):
                    new_pixel = encode_data_to_pixel(self.__get_pixel(pixel), ord(encoded_data[idx]))
                    self.image.putpixel(pixel, new_pixel)
                    if idx == len(encoded_data) - 1:
                        break
                pixel = next(enumerator)
                new_pixel = encode_data_to_pixel(self.__get_pixel(pixel), ord('©'))
                self.image.putpixel(pixel, new_pixel)
            case "random_spacing":
                info = self.file_info()
                enumerator = get_random_spacing_pixels(info["size"][0], info["size"][1], kwargs["key"])
                data = kwargs["data"]
                for (idx, pixel) in enumerate(enumerator):
                    new_pixel = encode_data_to_pixel(self.__get_pixel(pixel), ord(data[idx]))
                    print(new_pixel)
                    self.image.putpixel(pixel, new_pixel)
                    if idx == len(data) - 1:
                        break
                pixel = next(enumerator)
                new_pixel = encode_data_to_pixel(self.__get_pixel(pixel), ord('©'))
                self.image.putpixel(pixel, new_pixel)
            case _:
                raise NotImplementedError(f"Method {method} not implemented")
                    

    def decode(self, method, **kwargs):
        """Decode data from the image

        The method allows selecting the method to use to decode the data, and
        it accepts keyword arguments to pass to the method. The keywords are:
        - key: The key to use to decode the data

        The method raises a NotImplementedError if the method is not implemented.

        arguments:
        - method - string - The method to use to decode the data
        - kwargs - dict - The arguments to pass to the method

        returns:
        - string - The decoded data
        """

        match method:
            case "rail_fence_cipher":
                info = self.file_info()
                enumerator = get_rail_fence_pixels(info["size"][0], info["size"][1], kwargs["key"])
                decoded_data = ""
                for pixel in enumerator:
                    character = chr(decode_data_from_pixel(self.image.getpixel(pixel)))
                    if character == '©':
                        break
                    decoded_data += character
                return decode_rail_fence_cipher(decoded_data, kwargs["key"])
            case "random_spacing":
                info = self.file_info()
                enumerator = get_random_spacing_pixels(info["size"][0], info["size"][1], kwargs["key"])
                decoded_data = ""
                for pixel in enumerator:
                    character = chr(decode_data_from_pixel(self.image.getpixel(pixel)))
                    if character == '©':
                        break
                    decoded_data += character
                return decoded_data
            case _:
                raise NotImplementedError(f"Method {method} not implemented")

    def __get_pixel(self, pixel):
        """A default key for the alpha channel

        arguments:
        - pixel - tuple - The pixel to get the alpha channel from

        returns:
        - tuple - The pixel with the alpha channel
        """
        new_pixel = self.image.getpixel(pixel)
        if len(new_pixel) == 3:
            self.image.putalpha(255)
            new_pixel = self.image.getpixel(pixel)
        return new_pixel