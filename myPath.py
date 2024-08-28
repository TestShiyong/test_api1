import os

base = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(base, 'data')

config_path = os.path.join(base, 'config')

log_path = os.path.join(base, 'outPut', 'log_file')

cf_path = os.path.join(base, 'config/config_file.ini')

product_goods_path = os.path.join(base, 'data', 'file')

erp_ft_path = os.path.join(config_path, 'azft.azft')

erp_aws_path = os.path.join(config_path, 'erp-test-aws.rsa')


translatedLanguageFile = os.path.join(base, 'primeData','translatedLanguage.xlsx')
# csv 文件路径
primeDataDir = os.path.join(base, 'primeData')
if __name__ == '__main__':
    print(primeDataDir)
