#!/usr/bin/env python
# coding: utf-8

# In[20]:


import pandas as pd
import numpy as np
from datetime import date
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.font_manager as fm
from matplotlib import gridspec


path = '../9.데이터/0.작업 데이터/0.전처리 데이터/'
path_3d = '../9.데이터/0.작업 데이터/9.3D 그래프/'
path_h = "../9.데이터/0.작업 데이터/2.사고 데이터/0.히트맵/"

# In[21]:


##  요일별 평균 속도 및 교통량 피벗 테이블 생성
####  속도 교통량을 함께 가지는 피벗테이블을 만드는 코드

## dataset : 피벗스타일로 만들 데이터셋 입력
## values : "속도", "교통량" 중 선택


def to_pivot_mean_data(dataset, values):
    dataset["차로"] = 1
    line1_data = dataset.copy()

    dataset["차로"] = 2
    line2_data = dataset.copy()

    dataset["차로"] = 3
    line3_data = dataset.copy()

    dataset["차로"] = 4
    line4_data = dataset.copy()

    line1_data = line1_data[["통계날짜", "통계시각", "레이더ID", "차로", "요일", "1차로 교통량", "1차로 속도"]]
    line1_data.columns = ["통계날짜", "통계시각", "레이더ID", "차로", "요일", "교통량", "속도"]
    line2_data = line2_data[["통계날짜", "통계시각", "레이더ID", "차로", "요일", "2차로 교통량", "2차로 속도"]]
    line2_data.columns = ["통계날짜", "통계시각", "레이더ID", "차로", "요일", "교통량", "속도"]
    line3_data = line3_data[["통계날짜", "통계시각", "레이더ID", "차로", "요일", "3차로 교통량", "3차로 속도"]]
    line3_data.columns = ["통계날짜", "통계시각", "레이더ID", "차로", "요일", "교통량", "속도"]
    line4_data = line4_data[["통계날짜", "통계시각", "레이더ID", "차로", "요일", "4차로 교통량", "4차로 속도"]]
    line4_data.columns = ["통계날짜", "통계시각", "레이더ID", "차로", "요일", "교통량", "속도"]

    total_line= pd.concat([line1_data, line2_data, line3_data, line4_data])
    
    day_data = []
    pivot_day_data = []
    
    for i in range(7):
        tmp = total_line.loc[total_line["요일"] == i]
        day_data.append(tmp)
        tmp1 = pd.pivot_table(tmp, index=["통계시각"], columns= ["차로", "레이더ID"], values = values, aggfunc = 'mean')
        pivot_day_data.append(tmp1)
    
    return pivot_day_data


# In[22]:


##  평일, 주말별 평균 속도 및 교통량 피벗 테이블 생성
####  속도 교통량을 함께 가지는 피벗테이블을 만드는 코드
####  평일 주말로 나누어서 피벗테이블 생성

## dataset : 피벗스타일로 만들 데이터셋 입력
## values : "속도", "교통량" 중 선택

def to_pivot_mean_data_week(dataset, values):
    dataset["차로"] = 1
    line1_data = dataset.copy()

    dataset["차로"] = 2
    line2_data = dataset.copy()

    dataset["차로"] = 3
    line3_data = dataset.copy()

    dataset["차로"] = 4
    line4_data = dataset.copy()

    line1_data = line1_data[["통계날짜", "통계시각", "레이더ID", "차로", "요일", "1차로 교통량", "1차로 속도"]]
    line1_data.columns = ["통계날짜", "통계시각", "레이더ID", "차로", "요일", "교통량", "속도"]
    line2_data = line2_data[["통계날짜", "통계시각", "레이더ID", "차로", "요일", "2차로 교통량", "2차로 속도"]]
    line2_data.columns = ["통계날짜", "통계시각", "레이더ID", "차로", "요일", "교통량", "속도"]
    line3_data = line3_data[["통계날짜", "통계시각", "레이더ID", "차로", "요일", "3차로 교통량", "3차로 속도"]]
    line3_data.columns = ["통계날짜", "통계시각", "레이더ID", "차로", "요일", "교통량", "속도"]
    line4_data = line4_data[["통계날짜", "통계시각", "레이더ID", "차로", "요일", "4차로 교통량", "4차로 속도"]]
    line4_data.columns = ["통계날짜", "통계시각", "레이더ID", "차로", "요일", "교통량", "속도"]

    total_line= pd.concat([line1_data, line2_data, line3_data, line4_data])
    
    weekday_total = total_line.loc[total_line["요일"] <= 4]
    weekend_total = total_line.loc[total_line["요일"] > 4]
    
    pivot_weekday = pd.pivot_table(weekday_total, index=["통계시각"], columns= ["차로", "레이더ID"], values = values, aggfunc = 'mean')
    pivot_weekend = pd.pivot_table(weekend_total, index=["통계시각"], columns= ["차로", "레이더ID"], values = values, aggfunc = 'mean')
    
    return pivot_weekday, pivot_weekend

# In[23]:

##  각 날짜 별로 피벗 테이블 생성

def to_pivot_each_data(dataset, values):
    dataset["차로"] = 1
    line1_data = dataset.copy()

    dataset["차로"] = 2
    line2_data = dataset.copy()

    dataset["차로"] = 3
    line3_data = dataset.copy()

    dataset["차로"] = 4
    line4_data = dataset.copy()

    line1_data = line1_data[["통계날짜", "통계시각", "레이더ID", "차로", "요일", "1차로 교통량", "1차로 속도"]]
    line1_data.columns = ["통계날짜", "통계시각", "레이더ID", "차로", "요일", "교통량", "속도"]
    line2_data = line2_data[["통계날짜", "통계시각", "레이더ID", "차로", "요일", "2차로 교통량", "2차로 속도"]]
    line2_data.columns = ["통계날짜", "통계시각", "레이더ID", "차로", "요일", "교통량", "속도"]
    line3_data = line3_data[["통계날짜", "통계시각", "레이더ID", "차로", "요일", "3차로 교통량", "3차로 속도"]]
    line3_data.columns = ["통계날짜", "통계시각", "레이더ID", "차로", "요일", "교통량", "속도"]
    line4_data = line4_data[["통계날짜", "통계시각", "레이더ID", "차로", "요일", "4차로 교통량", "4차로 속도"]]
    line4_data.columns = ["통계날짜", "통계시각", "레이더ID", "차로", "요일", "교통량", "속도"]

    total_line= pd.concat([line1_data, line2_data, line3_data, line4_data])
    
    day_data = []
    pivot_day_data = []
    day_data_date = []
    
    for i in range(7):
        tmp = total_line.loc[total_line["요일"] == i]
        day_data.append(tmp)
        
        tmp1 = tmp["통계날짜"].unique()
        day_data_date.append(tmp1)
        
        tmp2 = pd.pivot_table(tmp, index=["통계날짜", "통계시각"], columns= ["차로", "레이더ID"], values = values)
        pivot_day_data.append(tmp2)
    
    return pivot_day_data, day_data_date

# In[24]:


##  사고로 판단되는 데이터 리스트 및 날짜 리턴, 히트맵 출력 함수
#### 사고라고 판단되는 데이터의 리스트와 해당날짜를 리턴하고, 해당 데이터의 히트맵과 패턴데이터의 히트맵을 출력하는 함수
#### 사고판단기준 : 속도 감소율이 30% 이상이며, 이 감소율이 30분 이상 지속되고, 그 영향이 하류부로 퍼질때 사고로 판단
#### 코드의 한계 : 코드에서 사고로 출력기준은 패턴에 비해 30% 감소한 레이더가 6시퀀트 이상 있을때 사고로 판단
####               1)지속기준으로 바꾸어 줘야함 2) 하류부로 전파가 되어야함

def create_accident_list(dataset, values):
    
    fig = plt.figure(figsize=(21, 5)) 
    gs = gridspec.GridSpec(1, 2)
    
    RADR_list = dataset["레이더ID"].unique()
    
    pivot_day_data = to_pivot_mean_data(dataset, values)
    pivot_eachday_data, day_data_date = to_pivot_each_data(dataset, values)

    for dayNum in range(7):
        
        p_it = pivot_day_data[dayNum]
        c_it = pivot_eachday_data[dayNum]
        date_list = day_data_date[dayNum]
        
        accident_list = []
        accident_list_name = []
        accident_num = 0
        
        for itm in date_list:

            each_date = c_it.loc[itm]
            test = (p_it - each_date) - (p_it * 0.3)
            test = test.reset_index()

            for i in range(1, 5):

                for j in RADR_list:

                    if len(test.loc[test[i, j]>0][i, j]) > 6:

                        index_list = test.loc[test[i, j]>0][i, j].index
                        radr_num = len(RADR_list)
                        
                        if i == 1:
                            accident = each_date.iloc[(index_list[0] - 25):(index_list[0] +25), :radr_num]
                        elif i == 2:
                            accident = each_date.iloc[(index_list[0] - 25):(index_list[0] +25), radr_num:radr_num*2]
                        elif i == 3:
                            accident = each_date.iloc[(index_list[0] - 25):(index_list[0] +25), radr_num*2:radr_num*3]
                        else:
                            accident = each_date.iloc[(index_list[0] - 25):(index_list[0] +25), radr_num*3:]   
                        try:
                            pattern = p_it.loc[accident.index[0]:accident.index[49]][i]
                        except: continue
                        
                        create_heatmap(fig, gs, accident, pattern, radr_num, itm, i, j, accident_num)                        
                        
                        accident_list.append(accident)
                        accident_list_name.append(itm)

                        accident_num += 1

                    break

            
    return accident_list, accident_list_name


# In[25]:


def create_heatmap(fig, gs, accident, pattern, radr_num, itm, i, j, accident_num):
    plt.rcParams['figure.figsize'] = [12, 7]
    
    plt.subplot(gs[0])
    sns.heatmap(accident, yticklabels = radr_num, vmin=0, vmax=100)
    plt.title("{} {}차선 {} - accident#{}".format(itm, i, j,accident_num), fontsize=15)
    plt.subplot(gs[1])
    sns.heatmap(pattern, yticklabels = radr_num, vmin=0, vmax=100)
    plt.title("{} {}차선 {} - Pattern".format(itm, i, j), fontsize=15)

    fig.savefig(path_h + "{} {}차선 {} - accident#{}".format(itm, i, j,accident_num) + ".jpg", dpi=400)
    plt.cla()
    plt.clf()


# In[26]:

##   3D 그래프와 등고선을 생성하는 함수
#### 차선별, 요일별 시간-레이더 3D 그래프와 등고선 그래프를 생성

## dataset : 피벗스타일로 만들 데이터셋 입력
## line : 생성할 라인 입력
## values : "속도", "교통량" 중 선택

def create_3D_Graph(dataset, line, values):
    pivot_weekday, pivot_weekend = to_pivot_mean_data_week(dataset, values)
    pivot_list = [pivot_weekday, pivot_weekend]
    
    for i_list in pivot_list:
        
        x = range(288)
        y = range(int(i_list.shape[1]/4))
        Z = i_list[line].T.to_numpy()       

        X, Y = np.meshgrid(x, y)

        ## 3D 그래프 생성
        
        fig = plt.figure(1, figsize = (8, 8))
        ax = fig.add_subplot(111, projection = '3d')

        ax.set_title("시간-레이더 3D {} 그래프 ({}차로)".format(values, line), fontsize=12)

        ax.set_xlabel("Time")
        ax.set_xticks([0, 23, 47, 71, 95, 119, 143, 167, 191, 215, 239, 263, 287], minor=False)
        ax.set_xticklabels(["0","2","4","6","8","10","12","14","16","18","20","22","24"])

        ax.set_ylabel("RADR")
        ax.set_yticks(list(range(int(i_list.shape[1]/4))))
        ax.set_yticklabels(list(range(1, int(i_list.shape[1]/4)+1)))

        ax.set_zlabel("{}".format(values))

        if values == "속도":
            ax.set_zlim(0, 110)
        else:
            ax.set_zlim(0, 170)

        surface = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=matplotlib.cm.coolwarm, linewidth=0.1)
        plt.show()
        
        
        ## 등고선 그래프 생성
        
        fig1, ax1 = plt.subplots()    

        ax1.set_title("시간-레이더 등고선 {} 그래프 ({}차로)".format(values, line), fontsize=12)
        
        ax1.set_xlabel("Time")
        ax1.set_xticks([0, 23, 47, 71, 95, 119, 143, 167, 191, 215, 239, 263, 287], minor=False)
        ax1.set_xticklabels(["0","2","4","6","8","10","12","14","16","18","20","22","24"])

        ax1.set_ylabel("RADR")
        ax1.set_yticks(list(range(int(i_list.shape[1]/4))))
        ax1.set_yticklabels(list(range(1, int(i_list.shape[1]/4)+1)))

        contour = ax1.contourf(X, Y, Z, cmap=matplotlib.cm.coolwarm)
        plt.colorbar(contour)
        plt.show()
        
# 5개 이상 숫자가 연속될 시 연속의 시작이 되는 숫자를 리스트에 넣어서 리스트를 리턴
def contiueNum(queue): 
    
    packet = []
    turnNum = 0
    
    if len(queue) == 0:
        return packet

    v = queue.pop(0)    
    while len(queue)>0:
        vv = queue.pop(0)

        if v+1 == vv:
            v = vv
            turnNum = turnNum + 1
            if turnNum > 3:
                v = v - 4
                packet.append(v)
        else:
            turnNum = 0
            v = vv
            
    return packet

# 인덱스로 맞춰져 있는 시간 숫자(0~287)를 시간 문자로 바꾸어 리턴
def chage_datetime(dateNum):

    data = ['00:00:00','00:05:00','00:10:00','00:15:00','00:20:00','00:25:00','00:30:00','00:35:00','00:40:00','00:45:00','00:50:00','00:55:00',
            '01:00:00','01:05:00','01:10:00','01:15:00','01:20:00','01:25:00','01:30:00','01:35:00','01:40:00','01:45:00','01:50:00','01:55:00',
            '02:00:00','02:05:00','02:10:00','02:15:00','02:20:00','02:25:00','02:30:00','02:35:00','02:40:00','02:45:00','02:50:00','02:55:00',
            '03:00:00','03:05:00','03:10:00','03:15:00','03:20:00','03:25:00','03:30:00','03:35:00','03:40:00','03:45:00','03:50:00','03:55:00',
            '04:00:00','04:05:00','04:10:00','04:15:00','04:20:00','04:25:00','04:30:00','04:35:00','04:40:00','04:45:00','04:50:00','04:55:00',
            '05:00:00','05:05:00','05:10:00','05:15:00','05:20:00','05:25:00','05:30:00','05:35:00','05:40:00','05:45:00','05:50:00','05:55:00',
            '06:00:00','06:05:00','06:10:00','06:15:00','06:20:00','06:25:00','06:30:00','06:35:00','06:40:00','06:45:00','06:50:00','06:55:00',
            '07:00:00','07:05:00','07:10:00','07:15:00','07:20:00','07:25:00','07:30:00','07:35:00','07:40:00','07:45:00','07:50:00','07:55:00',
            '08:00:00','08:05:00','08:10:00','08:15:00','08:20:00','08:25:00','08:30:00','08:35:00','08:40:00','08:45:00','08:50:00','08:55:00',
            '09:00:00','09:05:00','09:10:00','09:15:00','09:20:00','09:25:00','09:30:00','09:35:00','09:40:00','09:45:00','09:50:00','09:55:00',
            '10:00:00','10:05:00','10:10:00','10:15:00','10:20:00','10:25:00','10:30:00','10:35:00','10:40:00','10:45:00','10:50:00','10:55:00',
            '11:00:00','11:05:00','11:10:00','11:15:00','11:20:00','11:25:00','11:30:00','11:35:00','11:40:00','11:45:00','11:50:00','11:55:00',
            '12:00:00','12:05:00','12:10:00','12:15:00','12:20:00','12:25:00','12:30:00','12:35:00','12:40:00','12:45:00','12:50:00','12:55:00',
            '13:00:00','13:05:00','13:10:00','13:15:00','13:20:00','13:25:00','13:30:00','13:35:00','13:40:00','13:45:00','13:50:00','13:55:00',
            '14:00:00','14:05:00','14:10:00','14:15:00','14:20:00','14:25:00','14:30:00','14:35:00','14:40:00','14:45:00','14:50:00','14:55:00',
            '15:00:00','15:05:00','15:10:00','15:15:00','15:20:00','15:25:00','15:30:00','15:35:00','15:40:00','15:45:00','15:50:00','15:55:00',
            '16:00:00','16:05:00','16:10:00','16:15:00','16:20:00','16:25:00','16:30:00','16:35:00','16:40:00','16:45:00','16:50:00','16:55:00',
            '17:00:00','17:05:00','17:10:00','17:15:00','17:20:00','17:25:00','17:30:00','17:35:00','17:40:00','17:45:00','17:50:00','17:55:00',
            '18:00:00','18:05:00','18:10:00','18:15:00','18:20:00','18:25:00','18:30:00','18:35:00','18:40:00','18:45:00','18:50:00','18:55:00',
            '19:00:00','19:05:00','19:10:00','19:15:00','19:20:00','19:25:00','19:30:00','19:35:00','19:40:00','19:45:00','19:50:00','19:55:00',
            '20:00:00','20:05:00','20:10:00','20:15:00','20:20:00','20:25:00','20:30:00','20:35:00','20:40:00','20:45:00','20:50:00','20:55:00',
            '21:00:00','21:05:00','21:10:00','21:15:00','21:20:00','21:25:00','21:30:00','21:35:00','21:40:00','21:45:00','21:50:00','21:55:00',
            '22:00:00','22:05:00','22:10:00','22:15:00','22:20:00','22:25:00','22:30:00','22:35:00','22:40:00','22:45:00','22:50:00','22:55:00',
            '23:00:00','23:05:00','23:10:00','23:15:00','23:20:00','23:25:00','23:30:00','23:35:00','23:40:00','23:45:00','23:50:00','23:55:00']
    dateStr = data[dateNum]
    return dateStr