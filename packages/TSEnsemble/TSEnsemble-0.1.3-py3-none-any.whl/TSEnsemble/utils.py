import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose, STL
from statsmodels.tsa.arima.model import ARIMAResultsWrapper, ARIMA, ARIMAResults
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.graphics.tsaplots import plot_acf as statsmodel_plot_acf
import re

def ts_from_csv(dataset_path, column = 1, index = 0):
    """
    Converts .csv file to pandas DataFrame, dropping all columns besides index and column.
    Args:
        dataset_path (str): path to .csv file.
        column (int, str, iterable): column index or name of time series values. Multivariate time series not fully supported yet.
        index (int, str): column index or name of time series timestamps.
    Returns:
        DataFrame.
    """
    if isinstance(column, int) or isinstance(column, str):
        df = pd.read_csv(dataset_path, parse_dates = True, index_col = index, usecols = [index, column])
    else:
        df = pd.read_csv(dataset_path, parse_dates = True, index_col = index, usecols = [index, *column])
    df.astype(float)
    df = df.interpolate()
    return df

def get_arima_model_S(model):
    """
    Gets seasonality of arima model
    Args:
        model (obj): ARIMA model.
    Returns:
        int: season value
    """
    if isinstance(model, ARIMA):
        return model.seasonal_order[3]

    summary_string = str(model.summary())
    param = re.findall('\(x\(([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+)',summary_string)

    if param == []:
        return 0
    return int(param[0][3])

def get_arima_model_order(model):
    """
    Gets order of arima model
    Args:
        model (obj): ARIMA model.
    Returns:
        (int, int, int) : p, d, q values
    """
    if isinstance(model, ARIMA):
        return [int(x) for x in model.order]

    summary_string = str(model.summary())
    param = re.findall('ARIMA\([^)]*\)',summary_string)
    param = eval(param[0][5:].replace('[]', '0'))
    if param == []:
        return 0
    return [int(x) for x in param]

def get_arima_model_seasonal_order(model):
    """
    Gets seasonal order of arima model
    Args:
        model (obj): ARIMA model.
    Returns:
        (int, int, int, int) : P, D, Q, S values
    """
    if isinstance(model, ARIMA):
        return [int(x) for x in model.seasonal_order]

    summary_string = str(model.summary())
    param = re.findall('x\([^)]*\)',summary_string)
    param[0] = eval(param[0][1:].replace("[]", "0"))
    if param == []:
        return 0
    return [int(x) for x in param[0]]
    

def get_seasonality(model):
    """
    Gets seasonality of created model
    Args:
        model (obj): ARIMA or keras model.
    Returns:
        (int) : season value
    """
    if hasattr(model, 'input_shape'):
        return model.input_shape[1]
    if isinstance(model, ARIMAResultsWrapper) or isinstance(model, ARIMA) or isinstance(model, ARIMAResults): # for ARIMA model
        return get_arima_model_S(model)

def get_coeff_determination(predictions, test):
    """
    Gets the determination coefficient by comparing the test data and predictions
    Args:
        predictions (ndarray): prediction values.
        test (ndarray): observed values.
    Returns:
        (float) : Determination coefficient value. 
    """
    res =  np.sum(np.square(test - predictions ))
    tot = np.sum(np.square(test - np.mean(test)))
    return (1 - res/(tot + np.epsilon()))

def get_rmse(predictions, test):
    """
    Gets the RMSE by comparing the test data and predictions
    Args:
        predictions (ndarray): prediction values.
        test (ndarray): observed values.
    Returns:
        (float) : RMSE value. 
    """
    return np.sqrt(((np.asanyarray(test) - np.asanyarray(predictions)) ** 2).mean())

def get_mse(predictions, test):
    """
    Gets the MSE by comparing the test data and predictions
    Args:
        predictions (ndarray): prediction values.
        test (ndarray): observed values.
    Returns:
        (float) : MSE value. 
    """
    return ((np.asanyarray(test) - np.asanyarray(predictions)) ** 2).mean()

def get_mae(predictions, test):
    """
    Gets the MAE by comparing the test data and predictions
    Args:
        predictions (ndarray): prediction values.
        test (ndarray): observed values.
    Returns:
        (float) : MAE value. 
    """
    return np.abs(np.asanyarray(test) - np.asanyarray(predictions)).mean()

def get_mape(predictions, test):
    """
    Gets the MAPE by comparing the test data and predictions
    Args:
        predictions (ndarray): prediction values.
        test (ndarray): observed values.
    Returns:
        (float) : MAPE value. 
    """
    return np.abs((np.asanyarray(test) - np.asanyarray(predictions))/np.asanyarray(test)).mean()

def create_dataset(dataset, look_back = 0):
    """
    Converts an array of values into a dataset matrix.
    Args:
        dataset (DataFrame, ndarray): dataset to use.
        look_back (int): amount of values in a single X.
    Returns:
        (ndarray), (ndarray) : X, y
    """
    dataX, dataY = [], []

    if look_back == 0:
        look_back = 1

    for i in range(len(dataset) - look_back):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)

def plot_decompose(dataset_path, period = None, column = 1, index = 0, max_plot = 10000, model = "additive", method = "stl", seasonal = 7, trend = None):
    """
    Take path of dataset and plot a decompose on trend and seasonality
    
    Args:
        dataset_path (str): path to .csv file.
        period (int, None): period of the series.
        column (int, str, iterable): column index or name of time series values. Multivariate time series not fully supported yet.
        index (int, str): column index or name of time series timestamps.
        max_plot(int): maximum number of values to plot.
        model ("additive", "multiplicative"): seasonal decompose model.
        method ("stl", "ma", "naive", "seasonal_decompose"): method of decomposition. "ma" and "naive" refer to seasonal_decompose
        seasonal (int): required for Seasonal ARIMA. Seasonality of time series.
        trend (int, None): length of the trend smoother.
    """
    dataset = pd.read_csv(dataset_path, parse_dates=True, index_col=index, usecols = [index, column])
    dataset = dataset.interpolate()
    if method.lower() == "stl":
        result = STL(dataset[-max_plot:].squeeze(), period = period, seasonal = seasonal, trend = trend).fit()
    elif method is None or method.lower() == "ma" or method.lower() == "naive" or method.lower() == "seasonal_decompose":
        result = seasonal_decompose(dataset[-max_plot:], model=model, period=period)
    else:
        raise Exception("method cant be identified")
    
    result.plot()
    plt.show()

def plot_acf(dataset_path, lags = 12, column = 1, index = 0):
    """
    Take path of dataset and plot a decompose on trend and seasonality
    
    Args:
        dataset_path (str): path to .csv file.
        lags (int): amount of lags to plot.
        column (int, str, iterable): column index or name of time series values. Multivariate time series not fully supported yet.
        index (int, str): column index or name of time series timestamps.
    """
    dataset = pd.read_csv(dataset_path, parse_dates=True, index_col=index, usecols = [index, column])
    dataset = dataset.interpolate()
    statsmodel_plot_acf(dataset, lags = lags)

def isStationary(dataset_path, window = None, column = 1, index = 0, alpha = 0.05, plot = True, fig_size = (15, 5), verbose = True, test = "both"):
    """
    Take path of dataset and make a conclusion on stationarity by using Dickey-Fuller Test
    
    Args:
        dataset_path (str): path to .csv file.
        window (int, None): window for means and stddevs calculation.
        column (int, str, iterable): column index or name of time series values. Multivariate time series not fully supported yet.
        index (int, str): column index or name of time series timestamps.
        alpha (float): alpha value. Recommended values: 0.05, 0.01, 0.1.
        plot (bool): print a plot.
        fig_size ((int, int)): size of a plot.
        verbose(int): print additional information.
        test ("both", "kpss", "adf"): tests to use. Default: "both"
        
    Returns:
        (bool) : test result.
    """

    # Read data to DataFrame
    ts = pd.read_csv(dataset_path, parse_dates=True, index_col=index, usecols = [index, column])
    # Interpolate missing values
    ts = ts.interpolate()

    # Automatically choose a window for plot
    if window is None:
        window = round(ts.shape[0]/50)

    ts = ts.squeeze()

    if plot:
        # Plot rolling means and variances
        pd.DataFrame({'Actual': ts,
                    'Means': ts.rolling(window=window).mean(),
                    'Stddevs': ts.rolling(window=window).std()
                    }, index=ts.index).plot(figsize = fig_size)

    # Run the tests
    if test.lower() == "both":
        test_df = adfuller(ts, autolag='AIC')
        test_kpss = kpss(ts)
    
        if verbose:
            result = pd.concat([pd.Series(test_df[:4],
                                    index=['stat', 'pval', 'lags', 'numobs']),
                                pd.Series(test_df[4])])
            result2 = pd.concat([pd.Series(test_kpss[:3],
                                    index=['stat', 'pval', 'lags']),
                                pd.Series(test_kpss[3])])
            print("ADF test: \n", result)
            print("KPSS test: ", result2)

        # if p-value is less than alpha  return True
        if test_df[1] < alpha and test_kpss[1] > alpha: 
            return True
        else:
            return False
        
    # Run the tests
    elif test.lower() == "adf":
        test_df = adfuller(ts, autolag='AIC')
    
        if verbose:
            result = pd.concat([pd.Series(test_df[:4],
                                    index=['stat', 'pval', 'lags', 'numobs']),
                                pd.Series(test_df[4])])
            print("ADF test: \n", result)

        # if p-value is less than alpha  return True
        if test_df[1] < alpha: 
            return True
        else:
            return False

    # Run the tests
    elif test.lower() == "kpss":
        test_kpss = kpss(ts)
    
        if verbose:
            result = pd.concat([pd.Series(test_kpss[:3],
                                    index=['stat', 'pval', 'lags']),
                                pd.Series(test_kpss[3])])
            print("KPSS test: ", result)

        # if p-value is less than alpha  return True
        if test_kpss[1] > alpha: 
            return True
        else:
            return False
        

    
def isStationaryArray(ts, window = None, alpha = 0.05, plot = True, fig_size = (15, 5), verbose = True, test = "both"):
    """
    Take numpy array and make a conclusion on stationarity by using Dickey-Fuller Test
    
    Args:
        ts (ndarray): time series.
        window (int, None): window for means and stddevs calculation.
        alpha (float): alpha value. Recommended values: 0.05, 0.01, 0.1.
        plot (bool): print a plot.
        fig_size ((int, int)): size of a plot.
        verbose(int): print additional information.
        test ("both", "kpss", "adf"): tests to use. Default: "both"
        
    Returns:
        (bool) : test result.
    """

    if not(isinstance(ts, np.ndarray)):
        if hasattr(ts, 'values'):
            ts = ts.values
        ts = np.array(ts)
        ts = ts.astype('float64')

    ts = pd.DataFrame(ts)
    ts = ts.interpolate()
    ts = ts.squeeze()

    window = round(ts.shape[0]/95)

    if plot:
        # Plot rolling means and variances
        pd.DataFrame({'Actual': ts,
                    'Means': ts.rolling(window=window).mean(),
                    'Stddevs': ts.rolling(window=window).std()
                    }, index=ts.index).plot(figsize = fig_size)

    # Run the tests
    if test.lower() == "both":
        test_df = adfuller(ts, autolag='AIC')
        test_kpss = kpss(ts)
    
        if verbose:
            result = pd.concat([pd.Series(test_df[:4],
                                    index=['stat', 'pval', 'lags', 'numobs']),
                                pd.Series(test_df[4])])
            result2 = pd.concat([pd.Series(test_kpss[:3],
                                    index=['stat', 'pval', 'lags']),
                                pd.Series(test_kpss[3])])
            print("ADF test: \n", result)
            print("KPSS test: ", result2)

        # if p-value is less than alpha  return True
        if test_df[1] < alpha and test_kpss[1] > alpha: 
            return True
        else:
            return False
        
    # Run the tests
    elif test.lower() == "adf":
        test_df = adfuller(ts, autolag='AIC')
    
        if verbose:
            result = pd.concat([pd.Series(test_df[:4],
                                    index=['stat', 'pval', 'lags', 'numobs']),
                                pd.Series(test_df[4])])
            print("ADF test: \n", result)

        # if p-value is less than alpha  return True
        if test_df[1] < alpha: 
            return True
        else:
            return False

    # Run the tests
    elif test.lower() == "kpss":
        test_kpss = kpss(ts)
    
        if verbose:
            result = pd.concat([pd.Series(test_kpss[:3],
                                    index=['stat', 'pval', 'lags']),
                                pd.Series(test_kpss[3])])
            print("KPSS test: ", result)

        # if p-value is less than alpha  return True
        if test_kpss[1] > alpha: 
            return True
        else:
            return False

def interpolate_nan(array_like):
    """
    Take numpy array and fill all NaNs using interpolation method.
    
    Args:
        array_like (DataFrame, ndarray): dataset.
        
    Returns:
        (ndarray) : interpolated dataset
    """
    array = array_like.copy()

    nans = np.isnan(array)

    def get_x(a):
        return a.nonzero()[0]

    array[nans] = np.interp(get_x(nans), get_x(~nans), array[~nans])

    return array


def prepare_dataset(dataset, train_size = None, test_size = None, look_back = 12, val_size = None, n_features = 1):
    """
    Split dataset on training, validation and testing arrays, scale data.
    
    Args:
        dataset (DataFrame, ndarray): time series dataset.
        train_size (float): Value from 0 to 1 to specify fraction of train dataset. Default value : 0.9.
        test_size (float): Value from 0 to 1 to specify fraction of test dataset. Not needed if train_size is specified. Default value : 1 - train_size
        look_back (int): amount of values in a single X.
        val_size (float): Value from 0 to 1 to specify fraction of val dataset inside of a train dataset. Default value : 0.1.
        n_features (int): dimensions of time series. Multivariate time series not fully supported.
        
    Returns:train_x_stf, train_y, val_x_stf, val_y, test_x_stf, test_y, trainScaler, valScaler, testScaler
        (ndarray, ndarray, ndarray, ndarray, ndarray, ndarray, obj, obj, obj) : train X, train y, val X, val y, test X, test y, trainScaler object, valScaler object, testScaler object.
    """
    if not(isinstance(dataset, np.ndarray)):
        dataset = dataset.values
        dataset = dataset.astype('float64')

    if (np.isnan(dataset).any()):
        dataset = interpolate_nan(dataset)

    if train_size is None: 
        if test_size is None:
            train_size = 0.9
        elif test_size < 1:
            train_size = 1 - test_size
        else:
            train_size = test_size/len(dataset)

    if val_size is None:
        val_size = (train_size)/10
    else:
        val_size = (train_size * val_size)

    # split into train and test sets
    train_size = train_size - val_size
    train_num = int(len(dataset) * train_size)
    val_num = train_num + int(len(dataset) * val_size)
    train, val, test = dataset[:train_num, :], dataset[train_num:val_num, :], dataset[val_num:, :]

    # normalize dataset separately
    trainScaler = MinMaxScaler(feature_range=(-1, 1))
    train = trainScaler.fit_transform(train)

    valScaler = MinMaxScaler(feature_range=(-1, 1))
    val = valScaler.fit_transform(val)

    testScaler = MinMaxScaler(feature_range=(-1, 1))
    test = testScaler.fit_transform(test)   

    # reshape into X=t and Y=t+1
    scaled_dataset = np.array(train.tolist() + val.tolist() + test.tolist())
    scaled_x, scaled_y = create_dataset(scaled_dataset, look_back)
    train_x = scaled_x[:train_num - look_back]
    train_y = scaled_y[:train_num - look_back]
    val_x = scaled_x[train_num - look_back:val_num - look_back]
    val_y = scaled_y[train_num - look_back:val_num - look_back]
    test_x = scaled_x[val_num - look_back:]
    test_y = scaled_y[val_num - look_back:]

    # reshape input to be [samples, time steps, features]
    train_x_stf = np.reshape(train_x, (train_x.shape[0], train_x.shape[1], n_features))
    test_x_stf = np.reshape(test_x, (test_x.shape[0], test_x.shape[1], n_features))
    val_x_stf = np.reshape(val_x, (val_x.shape[0], val_x.shape[1], n_features))

    return train_x_stf, train_y, val_x_stf, val_y, test_x_stf, test_y, trainScaler, valScaler, testScaler

def predict_array(model, 
                  dataset, 
                  look_back, 
                  scaler = None, 
                  plot = True, 
                  get = "mape", 
                  print_values = True, 
                  verbose = True, 
                  fig_size = (15, 5)):
    """
    Show fitted model predictions on a given data
    
    Args:
        model (obj): model used for predictions.
        dataset (DataFrame, ndarray): time series dataset.
        look_back (int): amount of values in a single X.
        scaler (obj): scaler object.
        plot (bool): plot predictions.
        get (str): error metric to return. Supports rmse, mse, mae, mape, all.
        print_values (bool): prints predictions and actuals DataFrame.
        verbose(int): print additional information.
        fig_size ((int, int)): size of a plot.
    Returns:
        (float, dict of floats) : error metric.
    """
    # if look_back is None:
    #     print("Look_back not set, setting to 12...")
    #     look_back = 12

    if scaler is None:
        scaler = MinMaxScaler(feature_range=(-1, 1))
        data = Scaler.fit_transform(dataset)

    # extract X and y values from data
    data_x, data_y = create_dataset(data, look_back)
    x_stf = np.reshape(data_x, (data_x.shape[0], data_x.shape[1], 1))

    return eval_model(model, 
                    x_stf, 
                    data_y, 
                    scaler, 
                    max_plot = 100, 
                    plot = plot, 
                    get = get, 
                    print_values = print_values, 
                    verbose = verbose, 
                    fig_size = fig_size)

def model_forecast(model, dataset, n = 1, plot = True, fig_size = (15, 5), datePlot = "date", dateStep = 1, n_features = 1):
    """
    Out-of-sample forecast of a fitted model, based on a given dataset.
    Plots Predictions, Actuals (with data, if index is datetime64).

    Args:
        model (obj): model used for predictions.
        dataset (DataFrame, ndarray): time series dataset.
        n (int): amount of values to predict.
        fig_size ((int, int)): size of a plot.
        datePlot ("date", "time"): format of date. Date example : 09.01.2024, time example: 21:10
        dateStep (int): prints each n date. 
        n_features (int): dimensions of time series. Multivariate time series not fully supported.
    Returns:
        (DataFrame) : predictions and actuals DataFrame.
    """   
    if isinstance(dataset, str):
        dataset = ts_from_csv(dataset)

    # Create date indices for predictions
    if isinstance(dataset, pd.DataFrame) and dataset.index.inferred_type == 'datetime64':
        if dataset.index.inferred_type == 'datetime64':
            last_date = dataset.index[-1]
            delta = last_date - dataset.index[-2]
            if delta.days >= 28 and delta.days <=31:
                delta = pd.DateOffset(months=1)
            offset = pd.tseries.frequencies.to_offset(delta)
            dateIndex = pd.date_range(last_date + delta, last_date + delta*n, freq=offset)

    dataset = np.array(dataset)
    scaler = MinMaxScaler(feature_range=(-1, 1))
    dataset = scaler.fit_transform(dataset)
    dataset = dataset.tolist()
    s = get_seasonality(model)
    if isinstance(model, ARIMA) or isinstance(model, ARIMAResultsWrapper)  or isinstance(model, ARIMAResults): 
        model = ARIMA(scaler.inverse_transform(dataset), 
                    order = get_arima_model_order(model), 
                    seasonal_order = get_arima_model_seasonal_order(model))
        model = model.fit()
        predictions = model.forecast(n).reshape((-1, 1))
    else:
    # Generate n predictions, use last look_back values
        X = dataset[-s:]
        predictions = []
        for i in range(n):
            fromX = s - i
            a = X[-fromX:] if fromX > 0 else []
            fromPredictions = min(i,s)
            a = a + predictions[-fromPredictions:]
            a = np.array(a).reshape(1, -1, n_features)
            prediction = model.predict(a, verbose = 0).tolist()
            predictions = predictions + prediction

        predictions = scaler.inverse_transform(predictions)
    
    df = pd.DataFrame({'predictions': predictions.flatten()}, index = dateIndex)
    if plot:
        # Get indices for plotting
        if datePlot == "date":
            date = [str(d)[:10] for d in df.index.values]
        elif datePlot == "time": 
            date = [str(d)[11:16] for d in df.index.values]
        
        x = date
        y = df["predictions"].values.tolist()

        # plot predictions
        plt.figure(figsize=fig_size)
        plt.plot(x,y)
        plt.xticks(rotation = 75)
        plt.xticks(np.arange(0, len(x)+1, dateStep))
        plt.show()

    return df

def eval_model(model, test_x, test_y, testScaler = None, get = "mape", plot = True, max_plot = 100, print_values = True, verbose = True, fig_size = (15, 5)):
    """
    Use model to forecast values based on test X and y, if data is scaled it requires a Scaler.
    Returns single chosen error metric from RMSE MSE MAE MAPE. Use "all" for a dictionary. 
    If verbose = True, prints all errors.
    If plot = True plots Predictions, Actual plot.
    If print_values = True, prints Predictions, Actual DataFrame.
    
    Args:
        model (obj): model used for predictions.
        test_x (ndarray): test X values.
        test_y (ndarray): test y values.
        testScaler (obj): scaler object.
        get (str): error metric to return. Supports rmse, mse, mae, mape, all.
        plot (bool): plot predictions.
        max_plot(int): maximum number of values to plot.
        print_values (bool): prints predictions and actuals DataFrame.
        verbose(int): print additional information.
        fig_size ((int, int)): size of a plot.
    Returns:
        (float, dict of floats) : error metric.
    """   

    predictions = model.predict(test_x).flatten()
    if not(testScaler is None):
        [predictions, test_y] = testScaler.inverse_transform([predictions, test_y])

    if plot:
            plt.figure(figsize=fig_size)
            if max_plot<len(test_y):
                plt.plot(test_y[-max_plot:], label = "Actual")
                plt.plot(predictions[-max_plot:], label = "Prediction")
            else:
                plt.plot(test_y, label = "Actual")
                plt.plot(predictions, label = "Prediction")               
            plt.ylabel('Values', fontsize=15)
            plt.legend()
            plt.show()

    if print_values:
        predicts = pd.DataFrame({'prediction' : predictions, 'actual' : test_y})
        print(predicts)

    if verbose == False:
        return pd.DataFrame({'prediction' : predictions, 'actual' : test_y})

    # get metrics
    rmse = get_rmse(predictions, test_y)
    mse = get_mse(predictions, test_y)
    mae = get_mae(predictions, test_y)
    mape = get_mape(predictions, test_y)
    print("RMSE = {}, MSE = {}, MAE = {}, MAPE = {}".format(rmse, mse, mae, mape))

    if get == "rmse" or get == "RMSE":
        return rmse
    if get == "mse" or get == "MSE":
        return mse
    if get == "mae" or get == "MAE":
        return mae
    if get == "mape" or get == "MAPE":
        return mape
    if get == "all" or get == "ALL":
        return {'RMSE' : rmse, 'MSE' : mse, 'MAE' : mae, 'MAPE' : mape}
    return 