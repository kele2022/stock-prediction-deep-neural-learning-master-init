"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
介绍如何批量导入一个文件夹中的所有数据
"""
import os

from datetime import datetime, timedelta

import pandas
import pandas as pd
import glob

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# path = os.getcwd()

# 筛选出指定币种和指定时间
# symbol_list = ['DOT-USDT_1m', 'ETH-USDT_1m', 'SUSHI-USDT_1m']


def scv_output_h5(data_path: str, start_time: str, end_time: str, symbol: str):
    """
    :param data_path: 数据所在目录
    :param start_time: 开始日期     "2021-01-01"
    :param end_time:    结束日期    "2021-01-01"
    :param symbol:      交易对     'DOT-USDT_15m'
    :return:            错误返回None  正确返回 h5 路径
    """
    global new_time
    df_list = []
    path_list = glob.glob(data_path + "/*/*.csv")  # python自带的库，获得某文件夹中所有csv文件的路径
    path_list = list(filter(lambda x: (symbol in x), path_list))

    if not path_list:
        print(symbol + " ERR： path_list == 0 ")
        return None

    # 处理 过滤掉 多余的日期
    datetime_start_time = datetime.strptime(start_time, "%Y-%m-%d")
    datetime_end_time = datetime.strptime(end_time, "%Y-%m-%d")
    path_list_tow = []
    for date in path_list:
        # 获取最后一个 "\\"的 index
        end_indxe = date.rfind("\\")
        # 获取倒数第二个的index
        ent_2_index = date.rfind("\\", 0, end_indxe)
        temp_date = date[ent_2_index+1: end_indxe]
        # 转换成时间数组
        timeArray = datetime.strptime(temp_date, "%Y-%m-%d")

        if datetime_start_time <= timeArray <= datetime_end_time:
            path_list_tow.append(date)

    if not path_list_tow:
        return None
    # 合并数据
    for path in sorted(path_list_tow):

        # 爬的数据
        # df = pd.read_csv(path, header=0, encoding="GBK")  # header=1 跳过第一行
        # df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]     #

        # 邢大 网站下载数据  跳过第一行
        df = pd.read_csv(path, header=1, encoding="GBK")
        # 自己爬的数据  不需要跳过
        # df = pd.read_csv(path, header=0, encoding="GBK")

        df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume', 'quote_volume', 'trade_num', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']]

        df_list.append(df)
        # print(df.head(5))

    # 整理完整数据
    data = pd.concat(df_list, ignore_index=True)
    data.sort_values(by='candle_begin_time', inplace=False)
    data.reset_index(drop=False, inplace=False)
    # temp = pd.to_datetime("2021-01-01")

    # 查看数据是否缺失
    # 将交易日期由字符串改为时间变量
    data['candle_begin_time'] = pd.to_datetime(data['candle_begin_time'])
    try:
        new_time = datetime_end_time+timedelta(days=1)-timedelta(minutes=10)
    except Exception as Err:
        print(Err)
    temp = data[data['candle_begin_time'] > new_time]
    if temp.shape[0] == 0:
        print("整理数据发现,数据不完整,请检查数据!")
        return None
    # 导出完整数据
    data_path= data_path+"\\"+symbol+"-"+str(start_time)+"-"+str(end_time) + ".h5"

    # data.to_hdf(data_path, key=symbol, mode='w')

    return data


# 输出 合成 的 df 数据
def get_data_frame(data_path, symbol, start_time, end_time, rule_type):
    # 合并 生成h5 文件
    try:
        # scv 文件 生成 h5文件
        # scv 合并
        df = scv_output_h5(data_path, start_time, end_time, symbol)
        if df is None:
            print("scv 文件 生成 h5文件 失败 文件 可能不存在!")
            exit()
        print("数据合并完成!")
        start_time = df.at[0, 'candle_begin_time']
        end_time = df.at[df.shape[0] - 1, 'candle_begin_time']
        print("start_time:" + str(start_time))
        print("end_time:" + str(end_time))

    except Exception as Err:
        print("get_data_frame:", Err)
        exit()

    # 将交易日期由字符串改为时间变量
    df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'])
    # 任何原始数据读入都进行一下排序、去重，以防万一
    df.sort_values(by=['candle_begin_time'], inplace=True)
    df.drop_duplicates(subset=['candle_begin_time'], inplace=True)
    df.reset_index(inplace=True, drop=True)

    # =====转换为其他分钟数据
    period_df = df.resample(rule=rule_type, on='candle_begin_time', label='left', closed='left').agg(
        {'open': 'first',
         'high': 'max',
         'low': 'min',
         'close': 'last',
         'volume': 'sum',
         'quote_volume': 'sum',
         'trade_num': 'sum',
         'taker_buy_base_asset_volume': 'sum',
         'taker_buy_quote_asset_volume': 'sum'
         })
    period_df.dropna(subset=['open'], inplace=True)  # 去除一天都没有交易的周期
    period_df = period_df[period_df['volume'] > 0]  # 去除成交量为0的交易周期
    period_df.reset_index(inplace=True)
    df = period_df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume', 'quote_volume', 'trade_num', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']]
    df = df[df['candle_begin_time'] >= pd.to_datetime('2017-01-01')]
    df.reset_index(inplace=True, drop=True)
    print("转换数据为: {}数据size: {} ".format(rule_type, len(df)))
    print(df.head(2))
    print(df.tail(2))
    return df


if __name__ == '__main__':
    try:
        # 获取数据的路径
        symbol = 'DOT-USDT_5m'
        data_path = 'D:\\binance\\spot\\BNB'  # 改成电脑本地的地址
        data_path = scv_output_h5(data_path, "2021-01-01", "2021-4-6", symbol)
        print(data_path)
    except Exception as Err:
        print(Err)