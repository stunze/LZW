MAX_DICT_SIZE = 4096
from bitarray import bitarray

def init_dictionary():
    alphabet = {}
    for i in range(0, 256):
        alphabet.update({format(i, "08b"):i})
    return  alphabet

def check_dictionary(dictionary: dict, element: str):  # reik nepamirst daugiau checku uzdet
    if len(dictionary) < MAX_DICT_SIZE:
        return True


def bytes_from_file(filename):
    with open(filename, "rb") as input_stream:
        while True:
            byte = input_stream.read(1)
            if not byte:
                break
            yield byte


def find_in_dictionary(dictionary: dict, key):
    for k, v in dictionary.items():
        if k == key:
            return v


def encoded_to_file(filename: str, encoded):
    with open(filename,'wb') as output_stream:
        output_stream.write(encoded)


def encoder(filename_in: str, filename_out: str):
        dictionary = init_dictionary()
    code = ""
    encoded = ""

    for byte in bytes_from_file(filename_in):
        #     if not (check_dictionary(dictionary, code)):
        #         break
        code += '{:08b}'.format(ord(byte))
        if len(code) < 16:
            pass
        elif code in dictionary.keys():
            pass
        else:
            root = code[:-8]
            entry = dictionary[root]
            encoded += format(entry, 'b')
            dictionary.update({code: len(dictionary)})
            code = code[-8:]

    encoded += format(dictionary[code], 'b')
    encoded_to_file(filename_out, encoded)

def read_from_file(filename: str):
    # perskaitom abeceles dydi
    try:
        with open(filename, mode='rb') as input_stream:  # reading characters from file

            entryList = []
            while True:
                dataByte = input_stream.read(4)
                if not dataByte:
                    break
                entryList.append(int.from_bytes(dataByte, "big"))
            return entryList

    except OSError:
        print("Failas nerastas.")


def write_to_file(outputFile: str, text: str):
    try:
        with open(outputFile, "wb") as output_stream:
            bitarray(text).tofile(output_stream)
        return True
    except OSError:
        print("Failas nerastas")
    return False


def decode(alphabet: dict, entryList: list) -> str:
    text = ""
    newWord = ""
    previousEntry = -1

    for entry in entryList:

        # print(text)
        if previousEntry > -1:
            if entry != len(alphabet):
                newWord += alphabet[previousEntry] + alphabet[entry][0:8]
            else:
                newWord += alphabet[previousEntry] + alphabet[previousEntry][0:8]
            # print(newWord)
            alphabet.update({len(alphabet): newWord})
            # print(alphabet)
            newWord = ""

        text += alphabet[entry]
        previousEntry = entry

    return text


def build_table() -> dict:
    alphabet = {}
    for i in range(0, 256):
        alphabet.update({i: format(i, "08b")})

    return alphabet


def decoder(comprfile: str, decomprfile: str):
    entryList = read_from_file(comprfile)
    alphabet = build_table()
    decoded_text = decode(alphabet, entryList)
    write_to_file(decomprfile, decoded_text)



if __name__ == '__main__':
    #encoder("test.txt", "temp.lzw")
    decoder("temp2.lzw", "flowers2.bmp")
