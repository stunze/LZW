def read_from_file(filename: str):
    #perskaitom abeceles dydi
    try:
        with open(filename, mode='rb') as input_stream:  # reading characters from file
            size_of_alphabet = int.from_bytes(input_stream.read(1), "big") #IRGI GALI NETILPT
            alphabet = {}
            num = 1
            for byte in input_stream.read(size_of_alphabet):
                alphabet.update({'{:08b}'.format(ord(byte)): num}) #GAL GERIAU APKEIST VIETOM
                num += 1

            entryList = []
            while True:
                dataByte = input_stream.read(1)
                if not dataByte:
                    break
                entryList.append(int.from_bytes(dataByte, "big"))  # CIA CRASHINS SU DIDELIAIS FAILAIS

            return alphabet, entryList

    except OSError:
        print("Failas nerastas.")


def decode(alphabet: dict, entryList: list) -> str:
    text = ""
    firstLetter = alphabet.get(entryList[0]) #nu tikrai negerai lol
    alphabet.update({firstLetter: 0})
    for entry in entryList:
        # TINGIU TOLIAU DARYT




def decoder(comprfile: str):
    alphabet, entryList = read_from_file(comprfile)
    decode(alphabet, entryList)


if __name__ == '__main__':
    decoder("mhm.txt")
