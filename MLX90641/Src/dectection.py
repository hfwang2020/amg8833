# 计算每一列的平均值展示
# 基于"data01.npy" 200farme有人
# mlx90641
# 单人检测v0.2
# 较v0.1加入index权重

import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.subscribe as subscribe
import matplotlib; matplotlib.use('TkAgg')
from Frame import Frame
from Track import Track
from utils import *

data01 = np.load("/home/hfwang/Desktop/DeV/VsCoDe/TrackDectection/MLX90641/Dataset/data02.npy")


T = Track()

fig, ax = plt.subplots()
col = np.ones(16)
for i in range(0, 10000):
    ax.cla()
    piexls = data01[i]
    # piexls = receiveMqtt()
    # piexls.resize(12, 16)
    F = Frame(piexls)
    if F.index > 0:
        if not (F.index == T.pointList[-1]):
            T.pointList.append(F.index)
            T.judge()
            print(T.pointList, "\t", "diff: ", T.diff)

    col = F.col_diff
    col_img = col.copy()
    col_img.resize(1, 16)
    # ax.imshow(col_img, vmin=20, vmax=30)
    ax.imshow(col_img, vmin=2, vmax=5)
    # ax.imshow(piexls, cmap="gray", vmin=20, vmax=35)
    ax.set_title("frame {}".format(i))
    plt.pause(0.1)