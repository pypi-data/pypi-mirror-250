import MyTT
import numpy as np


def calc_score():
    # x值和y值
    x = np.array([2, 5, 10, 20, 30])
    y = np.array([10, 8, 6, 2, 1])

    # 使用numpy的polyfit函数进行最小二乘拟合
    coefficients = np.polyfit(x, y, 1)
    print(coefficients)
    return coefficients


def calc_value_price(x):
    return -0.32 * x + 9.7

    # 测试
    print(calc_value_price(10))  # 输出: 5.342105263157895


def calc_market_value():

    pass


def score_by_price(df):
    pass


if __name__ == "__main__":
    n = 3
    r = calc_value_price(n)

    print("result = ", r)
