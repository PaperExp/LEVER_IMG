import cv2
import hashlib
import os
import random
import sys

db_dir = ['../db/unsplash/', '../db/sisp/img/']
out_dir = './result/perf/'
fcnt = 1000

class fake_server:
    sh_len = 1

    def __init__(self) -> None:
        self.sh_dic = {}
        # to record storage overhead
        self.init_file_dic = {} # to store inital file
        self.file_dic = {}      # to store uploaded file
        self.ttl_size = 0
        # to record communication overhead
        self.scheme_comm = 0
        self.lever_comm = 0
        self.odd_comm = 0

    @staticmethod
    def get_key_size():
        # item 1 size, n = 2048
        item1_size = 2048 >> 2
        # item 2 size, use homorphic encryption with RSA-4096
        item2_size = 4096 >> 3
        return item1_size + item2_size
    
    def __get_img_hash(self, img) -> str:
        alg = hashlib.sha256()
        alg.update(img.tobytes())
        return alg.hexdigest()
    
    def init_server(self, img_path):
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        h, w = img.shape
        alg = hashlib.sha256()
        alg.update(img.tobytes())
        img_hash = alg.hexdigest()
        
        sh = img_hash[:fake_server.sh_len * 2]
        # add to index dic
        if sh not in self.sh_dic.keys():
            self.sh_dic[sh] = 1
        # not store file, add row, so sh will add.
        elif img_hash not in self.init_file_dic.keys():
            self.sh_dic[sh] += 1
        # add to file dic
        self.init_file_dic[img_hash] = h * w * 8
    
    def upload(self, img_path):
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        h, w = img.shape
        alg = hashlib.sha256()
        alg.update(img.tobytes())
        img_hash = alg.hexdigest()
        
        # record communication overhead
        sh = img_hash[:fake_server.sh_len * 2]
        # sh not in sh_dic, file must not exist
        if sh not in self.sh_dic.keys():
            self.scheme_comm += h * w * 8
            self.lever_comm += h * w * 8 + fake_server.get_key_size()
            self.odd_comm += h * w * 8
            # add sh and file into dic
            self.sh_dic[sh] = 1
            if img_hash not in self.init_file_dic.keys():
                self.file_dic[img_hash] = h * w * 8
        # sh in sh_dic, verify whether file exists, and find file exists, then not upload
        elif img_hash in self.file_dic.keys():
            self.scheme_comm += h * w * 8 * self.sh_dic[sh]
            self.lever_comm += (h * w * 8 + fake_server.get_key_size()) * self.sh_dic[sh]
            self.odd_comm += h * w * 8
        # sh in sh_dic, verify whether file exists, and find file not exists, then should upload
        else:
            self.scheme_comm += h * w * 8 * self.sh_dic[sh]
            self.lever_comm += (h * w * 8 + fake_server.get_key_size()) * (self.sh_dic[sh] + 1)
            self.odd_comm += h * w * 8
            # add sh number
            # add file into dic
            self.sh_dic[sh] += 1
            if img_hash not in self.init_file_dic.keys():
                self.file_dic[img_hash] = h * w * 8
        # record storage overhead
        self.ttl_size += h * w * 8

def read_dir(dir_path : str) -> list:
    fps = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            fps.append(os.path.join(root, file))
            if len(fps) == fcnt:
                break
    return fps

def test_server(fps : list):
    fcomm = open(out_dir + 'comm_KB.csv', 'w')
    fcomm.write('exist_rate, scheme, lever, odd,\n')

    fdedup = open(out_dir + 'dedup.csv', 'w')
    fdedup.write('exist_rate, scheme, lever, odd, ttl_size\n')
    for exist_rate in range(11):
        exist_rate /= 10
        init_cnt = int(len(fps) * exist_rate)
        server = fake_server()
        # select init_cnt files to init server
        for fp in fps[:init_cnt]:
            server.init_server(fp)
        # upload all files
        for fp in fps:
            server.upload(fp)
        fcomm.write(str(exist_rate) + ', ' + str(server.scheme_comm / 1024) + ', ' + str(server.lever_comm / 1024) + ', ' + str(server.odd_comm / 1024) + ',\n')
        # compute deduplication rate
        odd_strg = 0
        # odd only store file content
        for key in server.file_dic.keys():
            odd_strg += server.file_dic[key]
        # this scheme store file content and short hash
        scheme_strg = odd_strg + server.sh_len * len(server.file_dic.keys())
        # lever scheme store file content, short hash, and key
        lever_strg = odd_strg + (server.sh_len + fake_server.get_key_size()) * len(server.file_dic.keys())
        fdedup.write(str(exist_rate) + ', ' + str(scheme_strg) + ', ' + str(lever_strg) + ', ' + str(odd_strg) + ', ' + str(server.ttl_size) + ',\n')
    fcomm.close()   

if __name__ == '__main__':
    if os.path.exists(out_dir) == False:
        os.makedirs(out_dir)
    fps = []
    if sys.argv[1] == 'unsplash':
        fps = read_dir(db_dir[0])
    elif sys.argv[1] == 'sisp':
        fps = read_dir(db_dir[1])
    else:
        print('Error: wrong dataset name')
        exit(-1)
    test_server(fps)
    print('Done the performance test in %s datasets with %d images!' % (sys.argv[1], len(fps)))