# Copyright 2020 Jordi Corbilla. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import glob
import os

import numpy as np
from absl import app
import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from stock_prediction_lstm import LongShortTermMemory
from stock_prediction_numpy import StockData
from datetime import date
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
import stock_prediction_deep_learning


def main(argv):

    stock_prediction_deep_learning.prediction()

    # print(tf.version.VERSION)
    # inference_folder = os.path.join(os.getcwd(), 'ETH-USDT_20220118_e205a90294764edf1b09c6f2bfb58dc2')
    #
    # # load future data
    # # data = StockData()
    # # min_max = MinMaxScaler(feature_range=(0, 1))
    # # x_test, y_test = data.generate_future_data(TIME_STEPS, min_max, date(2020, 7, 5), date(2021, 7, 5))
    #
    # # load the weights from our best model
    #
    # all_data = pd.read_csv(inference_folder + "\\downloaded_data_ETH-USDT.csv")
    #
    # #  获取 测试数据
    # all_data = all_data[['Date', 'Close']]
    #
    # all_data['Date'] = pd.to_datetime(all_data['Date'])
    #
    # test_data = all_data[all_data['Date'] >= pd.to_datetime("2021-07-01")].copy()
    #
    # test_data.set_index(['Date'], inplace=True)
    # all_data.set_index(['Date'], inplace=True)
    # print(test_data)
    #
    # sc = MinMaxScaler(feature_range=(0, 1))
    #
    # sc.fit(all_data)
    #
    # test_scaled = sc.transform(test_data)
    #
    # # 打包测试数据
    # time_steps = 5
    # x_test = []
    # y_test = []
    # for i in range(time_steps, test_scaled.shape[0]):
    #     x_test.append(test_scaled[i - time_steps:i])
    #     y_test.append(test_scaled[i, 0])
    #
    # x_test, y_test = np.array(x_test), np.array(y_test)
    # x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    #
    #
    #
    # # 获取目录下所有的模型
    # path_list = glob.glob(inference_folder + "/*.ckpt.index")
    # for path in path_list:
    #     # model = tf.keras.models.load_model(os.path.join(inference_folder, 'model_weights.h5'))
    #
    #
    #
    #     lstm = LongShortTermMemory(inference_folder)
    #
    #     model = lstm.create_model(x_test)
    #     model.summary()
    #
    #     model.load_weights(filepath=path)
    #
    #
    #
    #     # # display the content of the model
    #     # baseline_results = model.evaluate(x_test, y_test, verbose=2)
    #     # for name, value in zip(model.metrics_names, baseline_results):
    #     #     print(name, ': ', value)
    #     # print()
    #
    #     # perform a prediction
    #     test_predictions_baseline = model.predict(x_test)
    #     test_predictions_baseline = sc.inverse_transform(test_predictions_baseline)
    #     test_predictions_baseline = pd.DataFrame(test_predictions_baseline)
    #     test_predictions_baseline.to_csv(os.path.join(inference_folder, 'inference.csv'))
    #     print(test_predictions_baseline)


if __name__ == '__main__':
    TIME_STEPS = 60
    app.run(main)