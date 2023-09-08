import math
import numpy as np

class img_hid:
    def __init__(self) -> None:
        pass

    def img_dvd(self):
        pass

    def key_gen(self, seed : bytes, h : int, w : int) -> np.ndarray:
        # RC4 key generation
        S = np.zeros(256, dtype=np.uint8)
        T = np.zeros(256, dtype=np.uint8)
        for i in range(256):
            S[i] = i
            T[i] = seed[i % len(seed)]
        j = 0
        for i in range(256):
            j = (j + S[i] + T[i]) % 256
            S[i], S[j] = S[j], S[i]
        key = np.zeros((h, w), dtype=np.uint8)
        i, j = 0, 0
        for k in range(h * w):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            key[k // w][k % w] = S[(S[i] + S[j]) % 256]
        return key

    def block_enc(self, block : np.ndarray, key):
        key = key & 0xff
        return block ^ key

    def img_enc(self, img : np.ndarray, key : bytes):
        block_row = math.floor(img.shape[0] / 2)
        block_col = math.floor(img.shape[1] / 2)
        enc_key = self.key_gen(key, block_row, block_col)
        enc_img = np.zeros(img.shape, dtype=np.uint8)
        for i in range(block_row):
            for j in range(block_col):
                enc_block = self.block_enc(img[i * 2 : i * 2 + 2, j * 2 : j * 2 + 2], enc_key[i][j])
                # replace the block
                for m in range(2):
                    for n in range(2):
                        enc_img[i * 2 + m][j * 2 + n] = enc_block[m][n]
        # if row number is odd
        if img.shape[0] % 2 != 0:
            for i in range(img.shape[1]):
                enc_img[img.shape[0] - 1][i] = img[img.shape[0] - 1][i]
        # if col number is odd
        if img.shape[1] % 2 != 0:
            for i in range(img.shape[0]):
                enc_img[i][img.shape[1] - 1] = img[i][img.shape[1] - 1]
        return enc_img
    
    def img_block_resort(self, img : np.ndarray):


        pass

    def img_rvt(self):
        md = (block >> 21) & 0b111
        pass