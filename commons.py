import math
chunk_size = 1000


def pad_encoded_text(encoded_text):
    """
    padding the encoded text to bytes. if bit string is 14 we need 2 bits padding
    :param encoded_text: the encoded text without padding
    :return: padded encoded text
    """
    padding = 8 - len(encoded_text) % 8
    encoded_text = padding * "0" + encoded_text

    padded_info = "{0:08b}".format(padding)
    encoded_text = padded_info + encoded_text
    return encoded_text


def remove_padding(padded_encoded_text):
    """
    removing the extra padded bits from encoded_text
    :param padded_encoded_text: encoded string in bits
    :return: encoded text without padding
    """
    padded_text = padded_encoded_text[:8]
    padding = int(padded_text, 2)

    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1 * padding]

    return encoded_text


def get_byte_array(padded_encoded_text):
    """
    creating bytes array from bits string
    :param padded_encoded_text: string of bits
    :return: bytearray()
    """
    if len(padded_encoded_text) % 8 != 0:
        print("Encoded text not padded properly")
        exit(0)

    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i + 8]
        b.append(int(byte, 2))
    return b


def number_of_bits(k):
    return int(math.log2(256+k)+1)


def yield_bytes_from_stream(stream):
    """Returns a chunk of bytes from a stream"""
    while True:
        chunk = stream.read(chunk_size)
        if chunk:
            yield chunk
        else:
            break


def yield_from_file(path_to_file):
    with open(path_to_file, "rb") as stream:
        while True:
            data = stream.read(1)
            if data:
                yield data
            else:
                break