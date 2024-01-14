import os
import pandas as pd

LOCAL_DATASET_PATH = os.path.expanduser('~/') + '.local/coggle/'
if not os.path.exists(LOCAL_DATASET_PATH):
    try:
        os.makedirs(LOCAL_DATASET_PATH)
    except:
        print(f'The cache path {LOCAL_DATASET_PATH} created fails.')

DATASET_CDN_URL = {
    "waimai": "http://mirror.coggle.club/dataset/waimai_10k.csv.zip",

    "LCQMC_train": "http://mirror.coggle.club/dataset/LCQMC.train.data.zip",
    "LCQMC_valid": "http://mirror.coggle.club/dataset/LCQMC.valid.data.zip",
    "LCQMC_test": "http://mirror.coggle.club/dataset/LCQMC.test.data.zip",

    "CSL_train": "http://mirror.coggle.club/dataset/CSL.kg.train.tsv.zip",
    "CSL_valid": "http://mirror.coggle.club/dataset/CSL.kg.dev.tsv.zip",
    "CSL_test": "http://mirror.coggle.club/dataset/CSL.kg.test.tsv.zip",

    "titanic": "http://mirror.coggle.club/dataset/titanic.csv.zip",
    "housing": "https://mirror.coggle.club/dataset/housing.csv.zip",
    "AirPassengers": "http://mirror.coggle.club/dataset/AirPassengers.csv",
}


def load_waimai() -> pd.DataFrame:
    '''
    外卖评论数据集
    '''
    if os.path.exists(LOCAL_DATASET_PATH + 'waimai_10k.csv'):
        data = pd.read_csv(LOCAL_DATASET_PATH + 'waimai_10k.csv')
    else:
        data = pd.read_csv(DATASET_CDN_URL["waimai"])
        data.to_csv(LOCAL_DATASET_PATH + 'waimai_10k.csv', index=None)
    return data


def load_lcqmc() -> pd.DataFrame:
    '''
    LCQMC文本匹配数据集
    '''
    if os.path.exists(LOCAL_DATASET_PATH + 'LCQMC.train'):
        train = pd.read_csv(LOCAL_DATASET_PATH + 'LCQMC.train')
        valid = pd.read_csv(LOCAL_DATASET_PATH + 'LCQMC.valid')
        test = pd.read_csv(LOCAL_DATASET_PATH + 'LCQMC.test')
    else:
        train = pd.read_csv(DATASET_CDN_URL["LCQMC_train"], 
            sep='\t', names=['query1', 'query2', 'label'])

        valid = pd.read_csv(DATASET_CDN_URL["LCQMC_valid"], 
            sep='\t', names=['query1', 'query2', 'label'])

        test = pd.read_csv(DATASET_CDN_URL["LCQMC_test"], 
            sep='\t', names=['query1', 'query2', 'label'])

        train.to_csv(LOCAL_DATASET_PATH + 'LCQMC.train', index=None)
        valid.to_csv(LOCAL_DATASET_PATH + 'LCQMC.valid', index=None)
        test.to_csv(LOCAL_DATASET_PATH + 'LCQMC.test', index=None)

    return train, valid, test


def load_cslkg() -> pd.DataFrame:
    '''
    中文科学文献数据集
    https://github.com/ydli-ai/CSL
    '''
    if os.path.exists(LOCAL_DATASET_PATH + 'CSL.kg.train.tsv'):
        train = pd.read_csv(LOCAL_DATASET_PATH + 'CSL.kg.train.tsv')
        valid = pd.read_csv(LOCAL_DATASET_PATH + 'CSL.kg.dev.tsv')
        test = pd.read_csv(LOCAL_DATASET_PATH + 'CSL.kg.test.tsv')
    else:
        train = pd.read_csv(DATASET_CDN_URL["CSL_train"], sep='\t', header=None)
        valid = pd.read_csv(DATASET_CDN_URL["CSL_valid"], sep='\t', header=None)
        test = pd.read_csv(DATASET_CDN_URL["CSL_test"], sep='\t', header=None)

        train.to_csv(LOCAL_DATASET_PATH + 'CSL.kg.train.tsv', index=None)
        valid.to_csv(LOCAL_DATASET_PATH + 'CSL.kg.dev.tsv', index=None)
        test.to_csv(LOCAL_DATASET_PATH + 'CSL.kg.test.tsv', index=None)

    return train, valid, test


def load_titanic() -> pd.DataFrame:
    '''
    泰坦尼克号幸存数据集
    '''
    if os.path.exists(LOCAL_DATASET_PATH + 'titanic.csv'):
        data = pd.read_csv(LOCAL_DATASET_PATH + 'titanic.csv')
    else:
        data = pd.read_csv(DATASET_CDN_URL["titanic"])
        data.to_csv(LOCAL_DATASET_PATH + 'titanic.csv', index=None)
    return data


def load_housing() -> pd.DataFrame:
    '''
    房价预测数据集
    '''
    if os.path.exists(LOCAL_DATASET_PATH + 'housing.csv'):
        data = pd.read_csv(LOCAL_DATASET_PATH + 'housing.csv')
    else:
        data = pd.read_csv(DATASET_CDN_URL["housing"])
        data.to_csv(LOCAL_DATASET_PATH + 'housing.csv', index=None)
    return data


def load_air_passengers() -> pd.DataFrame:
    '''
    从 1949 年到 1960 年美国航空公司每月乘客总数
    '''
    if os.path.exists(LOCAL_DATASET_PATH + 'AirPassengers.csv'):
        data = pd.read_csv(LOCAL_DATASET_PATH + 'AirPassengers.csv')
    else:
        data = pd.read_csv(DATASET_CDN_URL["AirPassengers"])
        data.to_csv(LOCAL_DATASET_PATH + 'AirPassengers.csv', index=None)
    return data
