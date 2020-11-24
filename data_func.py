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


path = '../9.data/0.work_data/0.전처리 데이터/'
path_3d = '../9.data/0.work_data/9.3D 그래프/'
path_AL = '../9.data/0.work_data/3.Accident_list/'
path_h = "../9.data/0.work_data/2.heatmap/"

# In[21]:

# 공휴일 제거 함수
def holiday_remove(dataset):
    holiday_list = ['2018-02-15','2018-02-16','2018-02-17','2018-03-01','2018-05-05','2018-05-22','2018-06-06','2018-08-15',
                   '2018-09-23','2018-09-24','2018-09-25','2018-10-03','2018-10-06','2018-10-09','2018-10-27','2018-12-24','2018-12-25',
                   '2019-01-01','2019-02-04','2019-02-05','2019-02-06','2019-03-01','2019-05-05','2019-05-12','2019-06-06',
                   '2019-08-15','2019-09-12','2019-09-13','2019-09-14','2019-10-03','2019-10-09','2019-11-02','2019-12-24','2019-12-25',
                   '2020-01-01','2020-01-24','2020-01-25','2020-01-26','2020-03-01']
    for i in holiday_list:
        dataset = dataset[dataset['통계날짜'] != i]
    
    dataset = dataset.reset_index()
    return dataset


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


##  사고로 판단되는 히트맵 출력 함수
#### 사고라고 판단되는 데이터의 리스트와 해당날짜를 리턴하고, 해당 데이터의 히트맵과 패턴데이터의 히트맵을 출력하는 함수
#### 사고판단기준 : 속도 감소율이 30% 이상이며, 이 감소율이 30분 이상 지속되고, 그 영향이 하류부로 퍼질때 사고로 판단

def create_accident_heatmap(dataset, values):

    fig = plt.figure(figsize=(21, 12))
    gs = gridspec.GridSpec(2, 2)

    RADR_list = dataset["레이더ID"].unique()
    accident_num = 0

    dataset = holiday_remove(dataset)
    pivot_day_data = to_pivot_mean_data(dataset, values)
    pivot_eachday_data, day_data_date = to_pivot_each_data(dataset, values)

    for dayNum in range(7):

        p_it = pivot_day_data[dayNum]
        c_it = pivot_eachday_data[dayNum]
        date_list = day_data_date[dayNum]

        for itm in date_list:

            each_date = c_it.loc[itm]
            test = (p_it - each_date) - (p_it * 0.3)
            test = test.reset_index()

            for i in range(1, 5):

                for j in RADR_list:
                    funcTest = test.loc[test[i, j]>0][i,j].index
                    accident_point = contiueNum(funcTest.to_list(), 5)

                    if len(accident_point) > 0:

                        for acc_indexNum in accident_point:
                            radr_num = len(RADR_list)

                            if (acc_indexNum < 26)|(acc_indexNum >254):
                                continue 

                            accident = each_date.loc[chage_datetime(acc_indexNum - 25):chage_datetime(acc_indexNum +25), i]
                            pattern = p_it.loc[accident.index[0]:accident.index[-1]][i]

                            accident = missing_precess(accident, radr_num)

                            if accident.isnull().sum().sum() == 0:
                                create_heatmap(fig, gs, accident, pattern, radr_num, itm, i, j, accident_num)                        
                                create_heatmap_minus(fig, gs, accident, pattern, radr_num, itm, i, j, accident_num)                        

                            accident_num += 1
# 사고아닌 데이터 히트맵
def create_nonaccident_heatmap(dataset, values):

    fig = plt.figure(figsize=(21, 12))
    gs = gridspec.GridSpec(2, 2)

    RADR_list = dataset["레이더ID"].unique()
    nonaccident_num = 0

    dataset = holiday_remove(dataset)
    pivot_day_data = to_pivot_mean_data(dataset, values)
    pivot_eachday_data, day_data_date = to_pivot_each_data(dataset, values)

    for dayNum in range(7):

        p_it = pivot_day_data[dayNum]
        c_it = pivot_eachday_data[dayNum]
        date_list = day_data_date[dayNum]

        for itm in date_list:

            each_date = c_it.loc[itm]
            test = (p_it - each_date) - (p_it * 0.3)
            test = test.reset_index()

            for i in range(1, 5):

                for j in RADR_list:
                    funcTest = test.loc[test[i, j]<0][i,j].index
                    nonaccident_point = contiueNum(funcTest.to_list(), 51)

                    if len(nonaccident_point) > 0:
                        for nonacc_indexNum in nonaccident_point:
                            radr_num = len(RADR_list)

                            if (nonacc_indexNum < 26)|(nonacc_indexNum >254):
                                continue 

                            nonaccident = each_date.loc[chage_datetime(nonacc_indexNum - 25):chage_datetime(nonacc_indexNum +25), i]
                            pattern = p_it.loc[nonaccident.index[0]:nonaccident.index[-1]][i]

                            nonaccident = missing_precess(nonaccident, radr_num)

                            if nonaccident.isnull().sum().sum() == 0:
                                create_heatmap(fig, gs, nonaccident, pattern, radr_num, itm, i, j, nonaccident_num, isAccident = False)                        
                                create_heatmap_minus(fig, gs, nonaccident, pattern, radr_num, itm, i, j, nonaccident_num, isAccident = False)                        

                            nonaccident_num += 1
#사고 데이터 리스트
def create_accident_list(dataset, values):

    fig = plt.figure(figsize=(21, 12))
    gs = gridspec.GridSpec(2, 2)

    RADR_list = dataset["레이더ID"].unique()
    accident_num = 0
    setNum = 0

    dataset = holiday_remove(dataset)
    pivot_day_data = to_pivot_mean_data(dataset, values)
    pivot_eachday_data, day_data_date = to_pivot_each_data(dataset, values)

    for dayNum in range(7):

        p_it = pivot_day_data[dayNum]
        c_it = pivot_eachday_data[dayNum]
        date_list = day_data_date[dayNum]

        for itm in date_list:

            each_date = c_it.loc[itm]
            test = (p_it - each_date) - (p_it * 0.3)
            test = test.reset_index()

            for i in range(1, 5):

                for j in RADR_list:
                    funcTest = test.loc[test[i, j]>0][i,j].index
                    accident_point = contiueNum(funcTest.to_list(), 5)

                    if len(accident_point) > 0:
                        for acc_indexNum in accident_point:
                            radr_num = len(RADR_list)

                            if (acc_indexNum < 26)|(acc_indexNum >254):
                                continue 

                            accident = each_date.loc[chage_datetime(acc_indexNum - 25):chage_datetime(acc_indexNum +25), i]
                            pattern = p_it.loc[accident.index[0]:accident.index[-1]][i]

                            accident = missing_precess(accident, radr_num)
                            
                            if accident.isnull().sum().sum() == 0:
                                if setNum == 0:
                                    accData = create_data(fig, gs, accident, pattern, radr_num, itm, i, j, accident_num)
                                    setNum += 1
                                else:
                                    temp = create_data(fig, gs, accident, pattern, radr_num, itm, i, j, accident_num)
                                    accData = pd.concat([accData, temp], axis = 0)

                            accident_num += 1
    return accData
# 사고 아닌 데이터 리스트
def create_nonaccident_list(dataset, values):

    fig = plt.figure(figsize=(21, 12))
    gs = gridspec.GridSpec(2, 2)

    RADR_list = dataset["레이더ID"].unique()
    nonaccident_num = 0
    setNum = 0

    dataset = holiday_remove(dataset)
    pivot_day_data = to_pivot_mean_data(dataset, values)
    pivot_eachday_data, day_data_date = to_pivot_each_data(dataset, values)

    for dayNum in range(7):

        p_it = pivot_day_data[dayNum]
        c_it = pivot_eachday_data[dayNum]
        date_list = day_data_date[dayNum]

        for itm in date_list:

            each_date = c_it.loc[itm]
            test = (p_it - each_date) - (p_it * 0.3)
            test = test.reset_index()

            for i in range(1, 5):

                for j in RADR_list:
                    funcTest = test.loc[test[i, j]<0][i,j].index
                    nonaccident_point = contiueNum(funcTest.to_list(), 51)

                    if len(nonaccident_point) > 0:
                        for nonacc_indexNum in nonaccident_point:
                            radr_num = len(RADR_list)

                            if (nonacc_indexNum < 26)|(nonacc_indexNum >254):
                                continue 

                            nonaccident = each_date.loc[chage_datetime(nonacc_indexNum - 25):chage_datetime(nonacc_indexNum +25), i]
                            pattern = p_it.loc[nonaccident.index[0]:nonaccident.index[-1]][i]

                            nonaccident = missing_precess(nonaccident, radr_num)
                            
                            if nonaccident.isnull().sum().sum() == 0:
                                if setNum == 0:
                                    nonaccData = create_data(fig, gs, nonaccident, pattern, radr_num, itm, i, j, nonaccident_num, isAccident = False)
                                    setNum += 1
                                else:
                                    temp = create_data(fig, gs, nonaccident, pattern, radr_num, itm, i, j, nonaccident_num, isAccident = False)
                                    nonaccData = pd.concat([nonaccData, temp], axis = 0)

                            nonaccident_num += 1
    return nonaccData

#사고 + 패턴 데이터 리스트
def create_accident_pattern_list(dataset, values):

    fig = plt.figure(figsize=(21, 12))
    gs = gridspec.GridSpec(2, 2)

    RADR_list = dataset["레이더ID"].unique()
    accident_num = 0
    setNum = 0

    dataset = holiday_remove(dataset)
    pivot_day_data = to_pivot_mean_data(dataset, values)
    pivot_eachday_data, day_data_date = to_pivot_each_data(dataset, values)

    for dayNum in range(7):

        p_it = pivot_day_data[dayNum]
        c_it = pivot_eachday_data[dayNum]
        date_list = day_data_date[dayNum]

        for itm in date_list:

            each_date = c_it.loc[itm]
            test = (p_it - each_date) - (p_it * 0.3)
            test = test.reset_index()

            for i in range(1, 5):

                for j in RADR_list:
                    funcTest = test.loc[test[i, j]>0][i,j].index
                    accident_point = contiueNum(funcTest.to_list(), 5)

                    if len(accident_point) > 0:
                        for acc_indexNum in accident_point:
                            radr_num = len(RADR_list)

                            if (acc_indexNum < 26)|(acc_indexNum >254):
                                continue 

                            accident = each_date.loc[chage_datetime(acc_indexNum - 25):chage_datetime(acc_indexNum +25), i]
                            pattern = p_it.loc[accident.index[0]:accident.index[-1]][i]

                            accident = missing_precess(accident, radr_num)
                            
                            if accident.isnull().sum().sum() == 0:
                                if setNum == 0:
                                    accList, pattList = create_data(fig, gs, accident, pattern, radr_num, itm, i, j, accident_num, isDiff = False)
                                    setNum += 1
                                else:
                                    temp1, temp2 = create_data(fig, gs, accident, pattern, radr_num, itm, i, j, accident_num, isDiff = False)

                                    accList = pd.concat([accList, temp1], axis = 0)
                                    pattList = pd.concat([pattList, temp2], axis = 0)

                            accident_num += 1
    return accList, pattList

    #사고 + 패턴 데이터 리스트
def create_nonaccident_pattern_list(dataset, values):

    fig = plt.figure(figsize=(21, 12))
    gs = gridspec.GridSpec(2, 2)

    RADR_list = dataset["레이더ID"].unique()
    accident_num = 0
    setNum = 0

    dataset = holiday_remove(dataset)
    pivot_day_data = to_pivot_mean_data(dataset, values)
    pivot_eachday_data, day_data_date = to_pivot_each_data(dataset, values)

    for dayNum in range(7):

        p_it = pivot_day_data[dayNum]
        c_it = pivot_eachday_data[dayNum]
        date_list = day_data_date[dayNum]

        for itm in date_list:

            each_date = c_it.loc[itm]
            test = (p_it - each_date) - (p_it * 0.3)
            test = test.reset_index()

            for i in range(1, 5):

                for j in RADR_list:
                    funcTest = test.loc[test[i, j]<0][i,j].index
                    accident_point = contiueNum(funcTest.to_list(), 51)

                    if len(accident_point) > 0:
                        for acc_indexNum in accident_point:
                            radr_num = len(RADR_list)

                            if (acc_indexNum < 26)|(acc_indexNum >254):
                                continue 

                            accident = each_date.loc[chage_datetime(acc_indexNum - 25):chage_datetime(acc_indexNum +25), i]
                            pattern = p_it.loc[accident.index[0]:accident.index[-1]][i]

                            accident = missing_precess(accident, radr_num)
                            
                            if accident.isnull().sum().sum() == 0:
                                if setNum == 0:
                                    accList, pattList = create_data(fig, gs, accident, pattern, radr_num, itm, i, j, accident_num, isAccident = False, isDiff = False)
                                    setNum += 1
                                else:
                                    temp1, temp2 = create_data(fig, gs, accident, pattern, radr_num, itm, i, j, accident_num, isAccident = False, isDiff = False)

                                    accList = pd.concat([accList, temp1], axis = 0)
                                    pattList = pd.concat([pattList, temp2], axis = 0)

                            accident_num += 1
    return accList, pattList
# In[25]:
def create_data(fig, gs, accident, pattern, radr_num, itm, i, j, accident_num, isAccident = True, isDiff = True):
    if isDiff:
        result = pattern - accident
        result[result < 0] = 0
        result = np.array(result)
        result = np.ravel(result)
        if isAccident:
            result = pd.DataFrame(data=result, columns=["{} Line{} {} - accident#{}".format(itm, i, j,accident_num)])
        else:
            result = pd.DataFrame(data=result, columns=["{} Line{} {} - nonaccident#{}".format(itm, i, j,accident_num)])
        result = result.T
        return result
    else:
        accident = np.array(accident)
        accident = np.ravel(accident)
        pattern = np.array(pattern)
        pattern = np.ravel(pattern)
        if isAccident:
            accident = pd.DataFrame(data=accident, columns=["{} Line{} {} - accident#{}".format(itm, i, j,accident_num)])
            pattern = pd.DataFrame(data=pattern, columns=["{} Line{} {} - pattern#{}".format(itm, i, j,accident_num)])            
        else:
            accident = pd.DataFrame(data=accident, columns=["{} Line{} {} - nonaccident#{}".format(itm, i, j,accident_num)])
            pattern = pd.DataFrame(data=pattern, columns=["{} Line{} {} - pattern#{}".format(itm, i, j,accident_num)])
        accident = accident.T
        pattern = pattern.T
        return accident, pattern

def create_heatmap(fig, gs, accident, pattern, radr_num, itm, i, j, accident_num, isAccident = True):
    plt.rcParams['figure.figsize'] = [12, 8]
    
    plt.subplot(gs[0])
    sns.heatmap(accident, yticklabels = radr_num, vmin=0, vmax=100)
    if isAccident:
        plt.title("{} Line{} {} - accident#{}".format(itm, i, j,accident_num), fontsize=15)
    else:
        plt.title("{} Line{} {} - nonaccident#{}".format(itm, i, j,accident_num), fontsize=15)

    plt.subplot(gs[1])
    sns.heatmap(pattern, yticklabels = radr_num, vmin=0, vmax=100)
    plt.title("{} Line{} {} - Pattern".format(itm, i, j), fontsize=15)

    if isAccident:
        fig.savefig(path_h + "0.accident/0.히트맵/" + "{} Line{} {} - accident#{}".format(itm, i, j,accident_num) + ".jpg", dpi=400)
    else:
        fig.savefig(path_h + "1.nonaccident/0.히트맵/" + "{} Line{} {} - nonaccident#{}".format(itm, i, j,accident_num) + ".jpg", dpi=400)
    plt.cla()
    plt.clf()

def create_heatmap_minus(fig, gs, accident, pattern, radr_num, itm, i, j, accident_num, isAccident = True):
    plt.rcParams['figure.figsize'] = [12, 8]
    
    accident = pattern - accident

    plt.subplot(gs[2])
    sns.heatmap(accident, yticklabels = radr_num, vmin=0, vmax=50)
    if isAccident:
        plt.title("{} Line{} {} - accident#{}".format(itm, i, j,accident_num), fontsize=15)
        fig.savefig(path_h + "0.accident/1.사고_패턴_차이히트맵/" + "{} Line{} {} - accident#{}".format(itm, i, j,accident_num) + ".jpg", dpi=400)
    else:
        plt.title("{} Line{} {} - nonaccident#{}".format(itm, i, j,accident_num), fontsize=15)
        fig.savefig(path_h + "1.nonaccident/1.사고_패턴_차이히트맵/" + "{} Line{} {} - nonaccident#{}".format(itm, i, j,accident_num) + ".jpg", dpi=400)

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
        
# 5개 이상 숫자가 연속될 시 연속 구간의 중간 숫자를 리스트에 넣어서 리스트를 리턴

def contiueNum(queue, conNum): 
    
    packet = []
    turnNum = 0
    accident = 0
    
    if len(queue) == 0:
        return packet

    v = queue.pop(0)
    
    while len(queue)>0:
        vv = queue.pop(0)
        
        if v+1 == vv:
            v = vv
            turnNum = turnNum + 1
            if turnNum > conNum -2:
                accident = 1
            
        else:
            if accident == 0:
                v = vv
                turnNum = 0
            else:
                packet.append(v - int(turnNum/2))
                v = vv
                turnNum = 0
                accident = 0
            
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

def missing_precess(data, radr_num):
    if radr_num == 11:
        filln1 = {'RADR12' : (data['RADR11'] + data['RADR13'])/2, 'RADR13' : (data['RADR12'] + data['RADR14'])/2,
                  'RADR14' : (data['RADR13'] + data['RADR15'])/2, 'RADR15' : (data['RADR14'] + data['RADR16'])/2,
                  'RADR16' : (data['RADR15'] + data['RADR17'])/2, 'RADR17' : (data['RADR16'] + data['RADR18'])/2,
                  'RADR18' : (data['RADR17'] + data['RADR19'])/2, 'RADR19' : (data['RADR18'] + data['RADR20'])/2,
                  'RADR20' : (data['RADR19'] + data['RADR21'])/2}
        filln2 = {'RADR11' : data['RADR12'], 'RADR12' : data['RADR13'], 'RADR13' : data['RADR14'], 'RADR14' : data['RADR15'],
                  'RADR15' : data['RADR16'], 'RADR16' : data['RADR17'], 'RADR17' : data['RADR18'], 'RADR18' : data['RADR19'],
                  'RADR19' : data['RADR20'], 'RADR20' : data['RADR21']}
        filln3 = {'RADR12' : data['RADR11'], 'RADR13' : data['RADR12'], 'RADR14' : data['RADR13'], 'RADR15' : data['RADR14'],
                  'RADR16' : data['RADR15'], 'RADR17' : data['RADR16'], 'RADR18' : data['RADR17'], 'RADR19' : data['RADR18'],
                  'RADR20' : data['RADR19'], 'RADR21' : data['RADR20']}
    else:
        filln1 = {'RADR32' : (data['RADR31'] + data['RADR33'])/2, 'RADR33' : (data['RADR32'] + data['RADR34'])/2,
                  'RADR34' : (data['RADR33'] + data['RADR35'])/2, 'RADR35' : (data['RADR34'] + data['RADR36'])/2,
                  'RADR36' : (data['RADR35'] + data['RADR37'])/2, 'RADR37' : (data['RADR36'] + data['RADR38'])/2,
                  'RADR38' : (data['RADR37'] + data['RADR39'])/2, 'RADR39' : (data['RADR38'] + data['RADR40'])/2,
                  'RADR40' : (data['RADR39'] + data['RADR41'])/2, 'RADR41' : (data['RADR40'] + data['RADR42'])/2}
        filln2 = {'RADR31' : data['RADR32'], 'RADR32' : data['RADR33'], 'RADR33' : data['RADR34'], 'RADR34' : data['RADR35'],
                  'RADR35' : data['RADR36'], 'RADR36' : data['RADR37'], 'RADR37' : data['RADR38'], 'RADR38' : data['RADR39'],
                  'RADR39' : data['RADR40'], 'RADR40' : data['RADR41'], 'RADR41' : data['RADR42']}
        filln3 = {'RADR32' : data['RADR31'], 'RADR33' : data['RADR32'], 'RADR34' : data['RADR33'], 'RADR35' : data['RADR34'],
                  'RADR36' : data['RADR35'], 'RADR37' : data['RADR36'], 'RADR38' : data['RADR37'], 'RADR39' : data['RADR38'],
                  'RADR40' : data['RADR39'], 'RADR41' : data['RADR40'], 'RADR42' : data['RADR41']}
    data = data.fillna(filln1)
    data = data.fillna(filln1)
    data = data.fillna(filln1)
    data = data.fillna(method = 'ffill', limit=1)
    data = data.fillna(method = 'bfill', limit=1)
    
    return data