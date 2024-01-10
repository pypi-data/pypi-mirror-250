import random

def encode_data_to_pixel(pixel, data):
    """Encode data to a pixel

    The function takes a pixel and data and encodes the data into the pixel.
    The data is encoded into the least significant bits of the pixel.
    The data should be a character represented as an integer, using for example utf-8 encoding.

    arguments:
    - pixel - tuple - The pixel to encode the data into
    - data - int - The data to encode into the pixel

    returns:
    - tuple - The pixel with the encoded data

    example:
    ```
    pixel = (0, 0, 0, 0)
    data = 65
    new_pixel = encode_data_to_pixel(pixel, ord(data))
    ```
    """

    new_pixel = [0, 0, 0, 0]

    data = bin(data)

    for i in range(4):
        channel = pixel[i]

        # Konverterar data till binärt i en sträng med korrekt antal siffror (8) 
        binary_data = f"0b{"0" * (10 - len(data))}{data[2:]}"
        
        # Plockar ut delen av datan att sätta i varje pixel
        subdata = int((binary_data)[2*i+2 : 2*i+4], 2)

        # Sätter in data
        channel = channel >> 2 << 2 
        channel += subdata
        
        new_pixel[i] = channel

    return tuple(new_pixel)


def decode_data_from_pixel(pixel):
    """Decode data from a pixel

    The function takes a pixel and decodes the data from the pixel.
    The data is decoded from the least significant bits of the pixel.
    The data is returned as an integer.

    arguments:
    - pixel - tuple - The pixel to decode the data from

    returns:
    - int - The decoded data

    example:
    ```
    pixel = (0, 0, 0, 0)
    data = decode_data_from_pixel(pixel)
    ```
    """

    data = "0b"

    for channel in pixel:

        if len(bin(channel)) < 4:
            binary_data = f"0b0{bin(channel)[-1]}"
        else:
            binary_data = bin(channel)

        data += binary_data[-2:]

    data = int(data, 2)
    return data

  
def get_rail_fence_pixels(width, height, rail_fence_height):
    """Get the pixels to use for the rail fence cipher

    The function takes the width and height of the image and the height of the rail fence cipher.
    The function returns a generator that yields the pixels to use for the rail fence cipher.

    arguments:
    - width - int - The width of the image
    - height - int - The height of the image
    - rail_fence_height - int - The height of the rail fence cipher

    returns:
    - generator - The pixels to use for the rail fence cipher

    example:
    ```
    width = 100
    height = 100
    rail_fence_height = 4
    enumerator = get_rail_fence_pixels(width, height, rail_fence_height)
    ```
    """
    h = 0
    w = 0
    rail = 0
    down = True
    while h < height:
        if down:
            h += 1
            rail += 1
        else:
            h -= 1
            rail -= 1
        if rail % (rail_fence_height - 1) == 0:
            down = not down
        yield (w, h)
        w += 1
        if w + 1 == width:
            w = 0
            h += rail_fence_height

def get_random_spacing_pixels(height, width, key):
    """Get the pixels to use for the random spacing cipher

    The function takes the width and height of the image and a key.
    The function returns a generator that yields the pixels to use for the random spacing cipher.

    arguments:
    - width - int - The width of the image
    - height - int - The height of the image
    - key - int - The key to use to generate the random spacing

    returns:
    - generator - The pixels to use for the random spacing cipher

    example:
    ```
    width = 100
    height = 100
    key = 123456789
    enumerator = get_random_spacing_pixels(width, height, key)
    ```
    """
    random.seed(key)
    i = 0
    while i < height:
        j = 0
        while j < width:
            j += random.randint(1,5)
            if j >= width:
                break
            yield(i, j)
        i += 1
