import os

base = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(base, 'data')

config_path = os.path.join(base, 'config')

log_path = os.path.join(base, 'out_put', 'log_file')

cf_path = os.path.join(base, 'config/config_file.ini')

product_goods_path = os.path.join(base, 'data', 'file')

erp_ft_path = os.path.join(config_path, 'config/azft.azft')

erp_aws_path = os.path.join(config_path, 'erp-test-aws.rsa')
if __name__ == '__main__':
    print(erp_aws_path)
