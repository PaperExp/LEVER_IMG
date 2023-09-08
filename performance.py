

db_dir = ['../db/', '../db/']

class fake_server:
    sh_len = 1

    def __init__(self) -> None:
        self.file_dic = {}

    @staticmethod
    def __get_key_size():
        # item 1 size, n = 2048
        item1_size = 2048 >> 2
        # item 2 size, use homorphic encryption with RSA-4096
        item2_size = 4096 >> 3
        return item1_size + item2_size
    
    
