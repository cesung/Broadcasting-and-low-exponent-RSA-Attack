import math

class CRT:
    def __init__(self, C, N):
        # given input: ciphertext
        C1 = int(C[0], 16)
        C2 = int(C[1], 16)
        C3 = int(C[2], 16)
        self.C = [C1, C2, C3]
        
        # given input: Modulus (512 bits)
        N1 = int("".join(N[0].split(":")), 16)
        print("N1 hex = {}\nN1 = {}\n".format(N[0], N1))
        N2 = int("".join(N[1].split(":")), 16)
        print("N2 hex = {}\nN2 = {}\n".format(N[1], N2))
        N3 = int("".join(N[2].split(":")), 16)
        print("N3 hex = {}\nN3 = {}\n".format(N[2], N3))
        self.N = [N1, N2, N3]
        print("GCD(N1, N2) = {}".format(math.gcd(N1, N2)))
        print("GCD(N2, N3) = {}".format(math.gcd(N2, N3)))
        print("GCD(N3, N1 = {}".format(math.gcd(N3, N1)))

        print("\n" + "="*100 + "\n")
        self.e = 3
        print("e = {}".format(self.e))

    def get_multiplicative_inverse(self, n, N):
        # base case
        if N == 1: 
            return 1

        # if x1 (coefficient of N) less than 0, add N to make it positive
        N0 = N

        # n*x0 + N*x1 = 1 (mod N)
        x0, x1 = 0, 1

        # Euclidean algorithm (iterative form)
        while n > 1:
            # quotient
            q = n // N
            n, N = N, n%N
            x0, x1 = x1 - q * x0, x0

        return x1 if x1 >= 0 else x1 + N0

    def get_inverse_pow(self, X):
        # initailze high = 1
        high = 1
        #  exponential serach
        while high ** self.e < X:
            high *= 2

        # set low equals to half of high
        low = high // 2
    
        # binary search find the first value so that val**n >= X
        while low < high:
            mid = (low + high) // 2
            if mid**self.e < X:
                low = mid + 1
            else:
                high = mid

        return low

    def crt(self):
        """
        X \equiv C1 (mod N1)
        X \equiv C2 (mod N2)
        X \equiv C3 (mod N3)
        """
        # X == M^{e} where e == 3
        X = 0

        # prod = N1 * N2 * N3
        prod = 1
        for Ni in self.N:
            prod *= Ni

        print("prod = N1 * N2 * N3 = {}".format(prod))

        for Ci, Ni in zip(self.C, self.N):
            n = prod // Ni
            X += Ci * self.get_multiplicative_inverse(n, Ni) * n
        X %= prod
        print("X (M**e, decimal) = {}".format(X))
        print("\n" + "="*100 + "\n")

        M = self.get_inverse_pow(X)
        print("M (decimal) = {}".format(M))
        print("\n" + "="*100 + "\n")

        print("M (hex) = {}".format(hex(M)[2:]))
        print("\n" + "="*100 + "\n")

        return bytes.fromhex(hex(M)[2:]).decode('utf-8')

    def run(self):
        M = self.crt()
        print("M = {}".format(M))

C = [
    "34d2fc2fa4785e1cdb1c09c9a5db98317d702aaedd2759d96e8938f740bf982e2a42b904e54dce016575142f1b0ed112cc214fa8378b0d5eebc036dc7df3eeea",
    "3ddd68eeff8be9fee7d667c3c0ef21ec0d56cefab0fa10199c933cffbf0924d486296c604a447f48b9f30905ee49dd7ceef8fc689a1c4c263c1b3a9505091b00",
    "956f7cbf2c9da7563365827aba8c66dc83c9fb77cf7ed0ca225e7d155d2f573d6bd18e1c18044cb14c59b52d3d1f6c38d8941a1d58942ed7f13a52caccc48154",
]

N = [
    "00:96:23:51:1e:67:69:64:4d:69:3e:89:f6:92:ff:c2:55:8e:ef:12:1d:42:ca:98:69:97:81:e1:39:e2:9c:2e:1a:a5:8d:88:83:bb:db:a4:11:65:fd:eb:85:a9:a5:64:8f:c2:9a:65:d5:9e:94:01:69:4d:d1:1a:e2:05:f0:ce:3b",
    "00:ad:4b:c0:f9:80:f4:52:3f:49:0f:c4:0c:12:ef:ce:cc:1e:8a:f6:78:90:b6:56:24:49:87:6e:8e:09:1e:86:1c:da:69:9e:5a:8e:b3:09:b0:a9:d6:b2:93:10:0c:12:29:fb:d1:8a:59:51:f3:3b:6f:ba:b1:fd:8d:90:f7:c8:29",
    "00:b7:22:33:64:d8:83:53:ec:02:b0:85:0e:8a:01:d2:ba:9c:a2:66:3c:32:c1:5d:f7:b5:96:40:6c:6f:c1:c1:71:ac:96:5a:55:4b:8b:33:8f:4b:b0:46:c5:43:93:7b:4b:19:c6:99:86:4f:1d:0d:d4:be:01:77:ec:cc:e0:bb:57",
]

crt = CRT(C, N)
X = crt.run()
