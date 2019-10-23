# Import Libraries
import pandas as pd
import numpy as np
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import os
from django.conf import settings


from dateutil.relativedelta import relativedelta
from calendar import monthrange
import datetime

import tensorflow as tf


# Convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)

def train_nn(data, data_date, look_back, neurons, epochs, time_delta, data_type, future):

    data_array = []
    for i in data:
        data_array.append([i])
    
    data = np.array(data_array)
    # Convert data frame into float arrays
    data = data.astype('float32')

    datos = data
    

    # Set seed for reproducibility
    np.random.seed(123)
    
    # Normalize the dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    data = scaler.fit_transform(data)

    # Split data into train and test sets
    # As sequence is important keeping data for the first 29 periods in training dataset
    # The reamining 07 periods are in the test dataset
    train_size = len(data)
    test_size = len(data) 
    train, test = data[0:train_size,:], data[0:len(data),:]
    
    
    # Reshape into X=t and Y=t+1
    X_train, y_train = create_dataset(train, look_back)
    X_test, y_test = create_dataset(test, look_back)

    # Reshape input to be [samples, time steps, features]
    X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    # Create and Fit the LSTM network
    model = Sequential()
    model.add(LSTM(neurons, input_shape=(1, look_back)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X_train, y_train, epochs=epochs, batch_size=1, verbose=2)


    # Make predictions
    trainPredict = model.predict(X_train)
    testPredict = model.predict(X_test)


    data = scaler.inverse_transform(data)
    trainPredict = scaler.inverse_transform(trainPredict)
    testPredict = scaler.inverse_transform(testPredict)

    if time_delta!='DIAS':
        data_date = [datetime.datetime.strptime(i, '%m/%d/%Y').date() for i in data_date]
        future = [datetime.datetime.strptime(i, '%m/%d/%Y').date() for i in future]
        
    # Plot baseline and predictions
    # Colors:
    # Blue-- Actual Data
    # Orange-- Forecasting on Training dataset
    # Gree-- Forecasting on Test dataset
    plt.figure(figsize=(20,10))
    plt.title('Evaluación')
    plt.xlabel('Fechas')
    plt.ylabel('Precios (Soles)')
    plt.plot(data_date, data, label="Histórico")
    plt.plot(data_date[look_back:len(data_date)-1], trainPredict, color='red', label="Entrenamiento")
    plt.legend(loc='upper center', shadow=True, fontsize='x-large')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gcf().autofmt_xdate() 
    #plt.plot(testPredictPlot, color='blue', linestyle='--')
    plt.savefig(os.path.join(settings.MEDIA_ROOT, data_type+'_'+time_delta+'_'+'evaluacion.png'), dpi=400)

    # Plot baseline and predictions
    # Colors:
    # Blue-- Actual Data
    # Orange-- Forecasting on Training dataset
    # Gree-- Forecasting on Test dataset

    plt.figure(figsize=(20,10))
    plt.title('Pronóstico')
    plt.xlabel('Fechas')
    plt.ylabel('Precios (Soles)')
    plt.plot(future[look_back:len(data_date)-1], testPredict)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gcf().autofmt_xdate() 
    plt.savefig(os.path.join(settings.MEDIA_ROOT, data_type+'_'+time_delta+'_'+'prediccion.png'), dpi=400)

    #RMSE
    rmse = math.sqrt(mean_squared_error(datos[look_back+1:], trainPredict))
    
    #DAM
    all_dam = []
    for i in range(len(trainPredict)):
        all_dam.append(abs(trainPredict[i]-datos[look_back+1+i]))

    plt.figure(figsize=(20,10))
    plt.title('DAM')
    plt.xlabel('Fechas')
    plt.ylabel('DAM (Soles)')
    plt.plot(data_date[look_back:len(data_date)-1], all_dam)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gcf().autofmt_xdate() 
    plt.savefig(os.path.join(settings.MEDIA_ROOT, data_type+'_'+time_delta+'_'+'dam.png'), dpi=400)

    dam = np.mean(np.array(all_dam))

    #RMSE
    all_rmse = []
    for i in range(len(trainPredict)):
        all_rmse.append((trainPredict[i]-datos[look_back+1+i])**2)

    plt.figure(figsize=(20,10))
    plt.title('RMSE')
    plt.xlabel('Fechas')
    plt.ylabel('DAM (${Soles}^2$)')
    plt.plot(data_date[look_back:len(data_date)-1], all_rmse)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gcf().autofmt_xdate() 
    plt.savefig(os.path.join(settings.MEDIA_ROOT, data_type+'_'+time_delta+'_'+'rmse.png'), dpi=400)

    #PEMA
    all_pema = []
    for i in range(len(all_dam)):
        all_pema.append(abs(all_dam[i]/datos[look_back+1+i]))

    plt.figure(figsize=(20,10))
    plt.title('PEMA')
    plt.xlabel('Fechas')
    plt.ylabel('Pema %')
    plt.plot(data_date[look_back:len(data_date)-1], all_pema)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gcf().autofmt_xdate()  
    plt.savefig(os.path.join(settings.MEDIA_ROOT, data_type+'_'+time_delta+'_'+'pema.png'), dpi=400)

    eval_dir = data_type+'_'+time_delta+'_'+'evaluacion.png'
    pred_dir = data_type+'_'+time_delta+'_'+'prediccion.png'
    dam_dir = data_type+'_'+time_delta+'_'+'dam.png'
    pema_dir = data_type+'_'+time_delta+'_'+'pema.png'
    rmse_dir = data_type+'_'+time_delta+'_'+'rmse.png'

    pema = dam / np.mean(np.array(datos[look_back+1:]))

    return rmse, dam , pema, eval_dir, pred_dir, dam_dir, pema_dir, rmse_dir

def populate_days(data_date, data_price):
    start_date = data_date[0]
    end_date = data_date[-1]
    delta = datetime.timedelta(days=1)

    nn_date = []
    nn_price = []

    nn_future_date = []
    days = 0

    while start_date <= end_date:
        if start_date in data_date:
            nn_date.append(start_date)
            nn_price.append(data_price[data_date.index(start_date)])
        else:
            nn_date.append(start_date)
            nn_price.append(0)
        start_date += delta
        nn_future_date.append(end_date + datetime.timedelta(days=days))
        days += 1

    return nn_date, nn_price, nn_future_date

def get_weeks(data_date, data_price):
    #Save for week
    weeks_date = []
    weeks_price = []
    week_day = 0
    week = []
    for i in range(len(data_date)):
        week.append(data_price[i])
        week_day += 1
        if week_day == 7:
            weeks_date.append(data_date[i].strftime('%m/%d/%Y'))
            weeks_price.append(np.sum(np.array(week)))
            week = []
            week_day = 0

    return weeks_date, weeks_price

def get_months(data_date, data_price):
    #All months
    all_months = []

    current = data_date[0]
    today = data_date[-1] 

    while current <= today:
        all_months.append(current)
        current += relativedelta(months=1)

    #Save for month

    months_date = []
    months_price = []
    current_i = 0
    current_month = all_months[current_i]
    month = []
    for i in range(len(data_date)):
        if current_month.month != data_date[i].month and current_i<len(all_months):
            months_date.append(current_month.strftime('%m/%d/%Y'))
            months_price.append(np.sum(np.array(month)))
            month = []
            current_month = all_months[current_i]
            current_i += 1
        month.append(data_price[i])

    return months_date, months_price

def get_nn_tipos(data_date, data_type):
    start_date = data_date[0]
    end_date = data_date[-1]
    delta = datetime.timedelta(days=1)

    nn_date = []
    nn_type = []

    while start_date <= end_date:
        if start_date in data_date:
            nn_date.append(start_date)
            nn_type.append(data_type[data_date.index(start_date)])
        else:
            nn_date.append(start_date)
            nn_type.append('NA')
        start_date += delta

    return nn_date, nn_type


