import json
import os

class Record:

    def __init__(self, name):
        self.RECORD_FILE = os.path.join(os.path.dirname(__file__), name+'.json')

    def save_user_agents(self, id, index, exp_num, get_num):
        df = {
            'id': [], 'index': [],
            'exp_num': [], 'get_num': []
        }

        if os.path.exists(self.RECORD_FILE):
            with open(self.RECORD_FILE, 'r') as f:
                df = json.load(f)

        rec_temp = {
            'id': [id], 'index': [index],
            'exp_num': [exp_num], 'get_num': [get_num]
        }
        df = {
            'id': df['id'] + rec_temp['id'],
            'index': df['index'] + rec_temp['index'],
            'exp_num': df['exp_num'] + rec_temp['exp_num'],
            'get_num': df['get_num'] + rec_temp['get_num']
        }

        with open(self.RECORD_FILE, 'w') as f:
            json.dump(df, f, indent=2)


    def get_record(self):
        if not os.path.exists(self.RECORD_FILE):
            return False

        with open(self.RECORD_FILE, 'r') as f:
            df = json.load(f)

        return df

        # return set(df['id'])