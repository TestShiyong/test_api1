import os

base = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(base, 'data')

log_path = os.path.join(base, 'out_put', 'log_file')

cf_path = os.path.join(base, 'config_file.ini')

product_goods_path = os.path.join(base, 'data', 'file')
if __name__ == '__main__':
    print(cf_path)
