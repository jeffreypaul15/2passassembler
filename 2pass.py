def precision(string, length=6):
    return '0'*(length-len(string))+string

def getMnemonicCode(mnemonic):
    if mnemonic == "LDA":
        return 33
    elif mnemonic == "STA":
        return 44
    elif mnemonic == "LDCH":
        return 53
    elif mnemonic == "STCH":
        return 57
    else:
        return -1

def findInSYMTAB(findLabel):
    counter3 = 0
    SYMTAB_ = open("symtab.dat","r")
    SYMTAB = SYMTAB_.readlines()
    label, addr = SYMTAB[counter3].split()
    counter3 += 1

    for i in range(len(SYMTAB)):
        if findLabel == label:
            SYMTAB_.close()
            return int(addr)
        label, addr = SYMTAB[counter3].split()
        counter3 += 1

def main():
    mnemonic = ["START", "LDA", "STA", "LDCH", "STCH", "END"]
    locctr = start = j = i = length = tlength = count = 0
    finalAddress = startAddress = None

    INPUT = open("input.dat","r")
    OUTPUT = open("output.dat","w")
    SYMTAB = open("symtab.dat","w")

    INPUT  = INPUT.readlines()
    label, opcode, operand = INPUT[0].split()

    if opcode == "START":
        start = int(operand)
        locctr = start
        OUTPUT.write(f"\t{label}\t{opcode}\t{operand}\n")
        label, opcode, operand = INPUT[1].split()
        print(label, opcode, operand)
    else:
        locctr = 0
    counter = 2
    while(opcode != "END"):
        j=0
        OUTPUT.write(f"{locctr}\t")
        if label != "**":
           SYMTAB.write(f"\t{label}\t{locctr}\n")
        
        while mnemonic[j] != 'END':
            if mnemonic[j] == opcode:
                locctr += 3
            j += 1
        
        if opcode == "WORD":
            locctr += 3
        elif opcode == "RESW":
            locctr += 3*int(operand)
            count += 3*int(operand)
        
        elif opcode == "RESB":
            locctr += int(operand)
            count += int(operand)
        elif opcode == 'BYTE':
            print('gg', len(operand))
            locctr = locctr+(len(operand)-3)
        else:
            print(" ")
        OUTPUT.write(f"{label}\t{opcode}\t{operand}\n")
        label, opcode, operand = INPUT[counter].split()
        counter += 1

    OUTPUT.write(f"{locctr}")
    OUTPUT.write(f"\t{label}\t{opcode}\t{operand}\n")
    print(f'The length of the program is {locctr-start}')
    length = locctr-start
    finalAddress = locctr
    tlength = length-count
    OUTPUT.close()
    SYMTAB.close()

    # 2nd pass

    INTERMEDIATE_ = open("output.dat", "r")
    OBJ = open("obj.dat", "w")
    FINAL = open("final.dat", "w")

    counter2 = 0

    INTERMEDIATE = INTERMEDIATE_.readlines()
    label, opcode, operand = INTERMEDIATE[counter2].split()

    counter2 += 1

    startAddress = int(operand)

    if opcode == "START":
        FINAL.write(f"{label}\t{opcode}\t{operand}\n")
        OBJ.write(f"H^{label}^00{operand}^00{length}\n")
        address, label, opcode, operand = INTERMEDIATE[counter2].split()
        counter2 += 1
        OBJ.write(f"T^{precision(address)}^{tlength}^")

    while opcode != "END":
        if label == "**":
            OBJ.write(f"{getMnemonicCode(opcode)}{findInSYMTAB(operand)}^")
            FINAL.write(f"{address}\t{label}\t{opcode}\t{operand}\t{getMnemonicCode(opcode)}{findInSYMTAB(operand)}\n")
            address, label, opcode, operand = INTERMEDIATE[counter2].split()
            counter2+=1

        elif opcode == "BYTE":
            FINAL.write(f"{address}\t{label}\t{opcode}\t{operand}")

            OBJ.write(f"{operand[2:-1]}")
            FINAL.write(f" {operand[2:-1]}\n")
            address, label, opcode, operand = INTERMEDIATE[counter2].split()
            counter2 += 1

        elif opcode == "WORD":
            OBJ.write(f"{precision(hex(int(operand))[-1].upper())}^")
            FINAL.write(f"{address}\t{label}\t{opcode}\t{operand}\t{precision(hex(int(operand))[-1].upper())}\n")
            address, label, opcode, operand = INTERMEDIATE[counter2].split()
            counter2 += 1
        else:
            address, label, opcode, operand = INTERMEDIATE[counter2].split()
            counter2 += 1

    FINAL.write(f"{address}\t{label}\t{opcode}\t{operand}\n")
    OBJ.write(f"\nE^{precision(str(startAddress))}\n")
    FINAL.close()
    OBJ.close()
    INTERMEDIATE_.close()


if __name__ == "__main__":
    main()