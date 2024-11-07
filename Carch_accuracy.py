import os
import random
# import time
import numpy as np

# Remember to change asm file name to your asm file
asm_file = "convolution.asm"
epsilon = 1e-3 # based on your precision, i.e. set precision n -> epsilon = 1e-(n)

def randomize():
    N = random.randint(3,7)
    M = random.randint(2,4)
    p = random.randint(0,4)
    s = random.randint(1,3)
    img = []
    for i in range(N**2):
        img.append(random.random())
    krn = []
    for i in range(M**2):
        krn.append(random.random())
        
    img = ' '.join("{:.3f}".format(round(a, 3)) for a in img)
    krn = ' '.join("{:.3f}".format(round(a, 3)) for a in krn)
    # print(img)
    outp = f'{N} {M} {p} {s}\n{img}\n{krn}'
    open('input_matrix.txt', 'w').write(outp)
    return outp

def get_sol():
    f = open('input_matrix.txt', 'r').read()
    f = f.split('\n')

    rows = [[i.strip() for i in f[n].split(' ')] for n in range(3)]

    N = int(rows[0][0])
    M = int(rows[0][1])
    p = int(rows[0][2])
    s = int(rows[0][3])

    INP_s = N + 2 * p
    OUT_s = (N - M + 2 * p) // s + 1

    if OUT_s < 1:
        return []

    INP = np.zeros((INP_s, INP_s), dtype = float)
    OUT = np.zeros((OUT_s, OUT_s), dtype = float)
    KRN = np.zeros((M, M), dtype = float)

    for x in range(p, N + p):
        for y in range(p, N + p):
            INP[x][y] = float(rows[1][(x - p) * N + (y - p)])
            
    for x in range(M):
        for y in range(M):
            KRN[x][y] = float(rows[2][x * M + y])

    for x in range(OUT_s):
        for y in range(OUT_s):
            a = s * x
            b = s * y
            tot = 0
            for i in range(M):
                for j in range(M):
                    tot += INP[a + i][b + j] * KRN[i][j]
            OUT[x][y] = tot
    
    return [float(i) for i in OUT.flatten()]

def checkvar():
    f = open('output_matrix.txt', 'r').read()
    sol = get_sol()
    if len(f) == 0:
        if len(sol) == 0:
            return True
        return False
    x = [float(i) for i in f.split(' ')]
        
    if len(x) == len(sol):
        for i in range(len(x)):
            if abs(x[i] - sol[i]) > epsilon:
                return False
        return True
    return False

n = 10
cnt = 0
# place fixed seed if you want to reproduce testcases
random.seed(random.random())

for i in range(n):
    randomize()
    # time.sleep(0.2)
    print(f'Random Test num {i}')
    outp = os.popen(f'cat input_matrix.txt').read()
    print(outp)
    os.system(f"java -jar ./Mars4_5.jar ./{asm_file}")
    if checkvar():
        print('wow')
        cnt += 1
    else:
        print('chicken')
    
    # outp = os.popen(f'cat output_matrix.txt').read()
    # print(outp)
    
print(f'Accuracy: {cnt/n * 100}%')