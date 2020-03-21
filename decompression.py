#!/usr/bin/env python3

def decompress(string):
    decompStr = ''
    multList = []
    strListTBM = []  # TBM = to be multiplied
    within = False
    indexJump = 1
    i = 0
    n = len(string)
    multiplier = 1
    while i < n:
        s = string[i]
        try:
            intOrStr = int(s)
        except:
            intOrStr = s
        if type(intOrStr) is int:
            if not within:
                multList.append(s)
            else:
                d, indexJump = decompress(string[i:])
                strListTBM.append(d)
                #print('Jumping: {}'.format(indexJump))
                i += indexJump
                indexJump = 1
                continue
        else:
            if s == '[':
                within = True
            elif s == ']':
                if not within:
                    break
                within = False
                multiplier = int(''.join(multList))
                decompStr += ''.join(multiplier * strListTBM)
                multiplier = 1
                multList = []
                strListTBM = []
            else:
                if within:
                    strListTBM.append(s)
                else:
                    decompStr += s
        i += 1
        indexJump += 1
    decompStr += ''.join(strListTBM)
    indexJump = i
    return decompStr, i

if __name__ == "__main__":
    tests = ['3[abc]', '10[a]b', '2[3[a]b]', 'b', '2[3[a]b4[c]]', '2[10[a]b]']
    for string in tests:
        output, _ = decompress(string)
        print('{}\t:\t{} {}'.format(string, output, len(output)))
