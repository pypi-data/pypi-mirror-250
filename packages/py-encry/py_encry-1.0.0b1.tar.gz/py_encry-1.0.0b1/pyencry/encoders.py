def encode_rail_fence_cipher(message, rails):
    """Encode a message with the rail fence cipher

    arguments:
    - message - string - The message to encode
    - rails - int - The number of rails to use to encode the message

    returns:
    - string - The encoded message

    example:
    ```
    message = "This is a secret message"
    rails = 4
    encoded_message = encode_rail_fence_cipher(message, rails)
    ```
    """
    
    fence = {}
    for rail in range(rails):
        fence[rail] = ""
    rail = 0
    down = True
    for item in message:
        fence[rail] += item
        if down:
            rail += 1
        else:
            rail -= 1
        if rail % (rails - 1) == 0 :
            down = not down
    result = ""
    for value in fence.values():
        result += value
    return result
