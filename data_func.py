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
