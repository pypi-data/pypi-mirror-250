
import os

import pandas as pd
import pandas_ta as ta
import yfinance as yf

from datetime import time, date, datetime, timedelta
from pytz import timezone

import pymannkendall as mk
import math
import numpy as np

from option_trader.consts import asset as at

from option_trader.utils.data_getter import get_price_history
from option_trader.utils.data_getter import get_next_earning_date
from option_trader.utils.data_getter import get_support_resistence_levels
from option_trader.utils.data_getter import get_option_exp_date
from option_trader.utils.data_getter import get_option_leg_details
from option_trader.utils.data_getter import get_option_leg_IV_delta
from option_trader.utils.data_getter import afterHours


from option_trader.backtest.stock.bollingerBands import BB_strategy, plot_BB
from option_trader.backtest.stock.macd import MACD_strategy, plot_MACD
from option_trader.backtest.stock.mfi import MFI_strategy, plot_MFI
from option_trader.backtest.stock.rsi import RSI_strategy, plot_RSI

from option_trader.utils.predictor  import predict_price_range
from option_trader.admin import quote
         

from option_trader.settings.ta_strategy import CustomStrategy
from  option_trader.settings import app_settings


import logging


import warnings
warnings.filterwarnings( "ignore", module = "matplotlib\..*" )

from option_trader.settings import app_settings  as settings    

def refresh_monitor_list(df, filter=[], check_afterhour=True):
    logger = logging.getLogger(__name__)
    for i, r in df.iterrows(): 

        if len(filter) > 0 and r['symbol'] not in filter:
             continue                       

        if len(filter) > 0:
            refresh_ta = True
        elif df.at[i, 'last_update_time'] != None:
            
            last_update_time = datetime.strptime(df.at[i, 'last_update_time'], "%a %b %d %H:%M:%S %Y")

            minutes_diff = (datetime.now() - last_update_time).total_seconds() / 60.0    

            if check_afterhour and afterHours():
                if minutes_diff < 60:
                    continue
            else:
                if minutes_diff < 60:
                    continue

            refresh_ta = True if minutes_diff > 60 * 24 else False 
        else:
            refresh_ta = True

        try: 
            refresh_asset_info(i, df, refresh_ta=refresh_ta, check_afterhour=check_afterhour)   
            #df.at[i, 'last_update_time'] = ctime()
            #logger.info('Refresh %s' % r['symbol'])            
        except Exception as ex:
            logger.exception(ex)
            pass 

    return df

def refresh_asset_info(i, df, refresh_ta=True, check_afterhour=True):

    logger = logging.getLogger(__name__)

    symbol = df.at[i, 'symbol']
    data = get_price_history(symbol, period='1y')
    if data.shape[0] <= 15:
        logger.error('Cannot get history for %s' % symbol)
        return 
    refresh_asset_basic_info(i, df, data, check_afterhour)   
    if refresh_ta:
        
        data.ta.cores = 2
        customStrateg = ta.Strategy(
            name="Option Trader",
            description="BBANDS, RSI, MACD, MFI, TREND",
            ta=[
                {"kind": "rsi"},
                {"kind": "macd", "fast": 12, "slow": 26},
                {"kind": "bbands", "length": 20},          
                {"kind": "mfi", "period": 14}     
            ]
        )
        data.ta.strategy(customStrateg)
        if "BBL_20_2.0" not in data.columns:
            logger.error('data ta failed for %s' % symbol)    
            return
        data.dropna(subset=["BBL_20_2.0"])    

        refresh_BB(i, df, data)
        refresh_RSI(i, df, data)        
        refresh_MFI(i, df, data)        
        refresh_MACD(i, df, data)        

    from time import ctime                
    df.at[i, 'last_update_time'] = ctime()
    logger.info('Refresh %s' % symbol)   
    #logger.debug('%s refreshed' %symbol)
     
def refresh_asset_basic_info(i, df, price_history, check_afterhour=True):        

    logger = logging.getLogger(__name__)

    from option_trader.utils.data_getter import afterHours

    logger = logging.getLogger(__name__)
    
    symbol = df.at[i, 'symbol']        

    df.at[i, 'quote_time'] = datetime.now(timezone(app_settings.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S %Z")

    last_price = price_history['Close'][-1]

    try:
        q = yf.Ticker(symbol).get_info()   
        if afterHours():
            day_high =  q['regularMarketDayHigh']
            day_low  =  q['regularMarketDayLow']         
            volume = q['regularMarketVolume']        
        else:
            day_high =  q['dayHigh']
            day_low  =  q['dayLow'] 
            volume = q['volume']    

        fifty_two_weeks_low =  q['fiftyTwoWeekLow']
        fifty_two_weeks_high = q['fiftyTwoWeekHigh']
        fifty_two_weeks_range_pos = ((last_price - fifty_two_weeks_low)/(fifty_two_weeks_high-fifty_two_weeks_low))*100 

        avg_volume = float(q['averageVolume'])

        volume_range_pos = (volume/avg_volume)*100   if avg_volume > 0 else np.nan         
    
        df.at[i, 'forward_PE'] = round(q['forwardPE'],2) if 'forwardPE' in q else np.nan       

        df.at[i, 'rating'] = float(q['recommendationMean']) if 'recommendationMean' in q else 0

    except Exception as ex:
        #logger.exception(ex)
        day_high =  price_history['High'][-1]
        day_low  =  price_history['Low'][-1] 
        volume = float(price_history['Volume'][-1])           

        fifty_two_weeks_low =  price_history['Close'].min()
        fifty_two_weeks_high = price_history['Close'].max()
        fifty_two_weeks_range_pos = ((last_price - fifty_two_weeks_low)/(fifty_two_weeks_high-fifty_two_weeks_low))*100
        avg_volume = price_history['Volume'].mean()
        volume_range_pos = (volume/avg_volume)*100  if avg_volume > 0 else np.nan         
        #df.at[i, 'forward_PE'] =  np.nan 

    day_range_pos = ((last_price - day_low)/(day_high-day_low)) * 100
        
    report_date = get_next_earning_date(symbol)        

    df.at[i, 'earning'] = '' if report_date == None else report_date.strftime('%m-%d-%Y')  
    #df.at[i, 'days to earning']  =np.nan if report_date == None else (report_date - today).days 

    ed = get_option_exp_date(symbol, min_days_to_expire=app_settings.STOCK_RANGE_PREDICT_DAYS, max_days_to_expire=np.nan)
    if len(ed) == 0:
        return
    
    target_date_list = [ed[0]]

    target_date_list = [get_option_exp_date(symbol, min_days_to_expire=app_settings.STOCK_RANGE_PREDICT_DAYS, max_days_to_expire=np.nan)[0]]
    predictlist = predict_price_range(symbol, target_date_list=target_date_list)
    exp_date_list = predictlist['exp_date_list']
    if len(exp_date_list) > 0:
        df.at[i, '90d target low'] = predictlist[exp_date_list[0]][quote.LOW]      
        df.at[i, '90d target high'] = predictlist[exp_date_list[0]][quote.HIGH]  
                    
    df.at[i, 'last price'] = round(last_price,2)       
    df.at[i, 'day range pos'] =  round(day_range_pos,2)
    df.at[i, 'fifty weeks range_pos'] = round(fifty_two_weeks_range_pos,2)
    df.at[i, 'volume range pos'] = round(volume_range_pos,2)                      
    support, resistence = get_support_resistence_levels(symbol, price_history)
    df.at[i, 'support'] = round(support,2) if support != None else np.nan
    df.at[i, 'resistence'] = round(resistence,2) if resistence != None else np.nan                    

    df.at[i, '10d change%'] = round((((last_price-price_history['Close'][-11])/last_price)*100),2)
    df.at[i, '10d high'] = round(price_history['High'].rolling(window=10).max().shift(1)[-1],2)
    df.at[i, '10d low'] = round(price_history['Low'].rolling(window=10).min().shift(1)[-1],2)   

    TRADING_DAYS =252
    returns = np.log(price_history['Close']/price_history['Close'].shift(1))
    returns.fillna(0, inplace=True)
    volatility = returns.rolling(window=20).std()*np.sqrt(TRADING_DAYS)
    hv = round(volatility[-1],2)    

    df.at[i, 'HV'] = hv #"{:.2f}".format(hv*100)

    def get_iv_list(symbol, data, count):     
        exp_tbl = get_option_exp_date(symbol)               
        iv = []
        delta=[]
        
        for exp_date in exp_tbl:    
            eiv, edelta = get_option_leg_IV_delta(symbol, exp_date, at.CALL)           
            iv.append(eiv)
            delta.append(edelta)
            count -= 1
            if count == 0:
                return iv, delta            
        return iv, delta 

    if check_afterhour and afterHours() == False: # After option qiote not avaialbe

        iv, delta = get_iv_list(symbol, price_history, 4)
            
        if len(iv) > 0:        
            df.at[i, 'IV1']  = round(iv[0],3) # "{:.2f}".format(iv[0]*100)
            df.at[i, 'IV1%']  = round(100 * ((df.at[i, 'IV1']-df.at[i, 'HV'])/df.at[i, 'HV']),2)        
            df.at[i, 'delta1'] = round(delta[0],3) #"{:.2f}".format(delta[0])    

        if len(iv) > 1:            
            df.at[i, 'IV2']  = round(iv[1],3) #"{:.2f}".format(iv[1]*100)
            df.at[i, 'IV2%']  = round(100 * ((df.at[i, 'IV2']-df.at[i, 'HV'])/df.at[i, 'HV']),2)           
            df.at[i, 'delta2'] = round(delta[1],3) #"{:.2f}".format(delta[1])

        if len(iv) > 2:                  
            df.at[i, 'IV3']  =  round(iv[2],3) #"{:.2f}".format(iv[2]*100)
            df.at[i, 'IV3%']  = round(100 * ((df.at[i, 'IV3']-df.at[i, 'HV'])/df.at[i, 'HV']),2)             
            df.at[i, 'delta3'] = round(delta[2],3) #"{:.2f}".format(delta[2])
        
        if len(iv) > 3:
            df.at[i, 'IV4']  =  round(iv[3],3) #"{:.2f}".format(iv[3]*100)       
            df.at[i, 'IV4%']  = round(100 * ((df.at[i, 'IV4']-df.at[i, 'HV'])/df.at[i, 'HV']),2)             
            df.at[i, 'delta4'] = round(delta[2],3) #"{:.2f}".format(delta[3])
                                        
def refresh_BB(i, df, data):            
    bb_pos = data['BBP_20_2.0'][-1]        
    last_action, last_action_price, recent, total_profit = BB_strategy(data, settings.TREND_WINDOW_SIZE)  
    #BB_display = last_action + " {:.2f}".format(last_action_price) if (last_action != '' and recent) else "{:.2f}".format(bb_pos)                  
    BB_display = "{:.2f}".format(bb_pos)                  
    address = plot_BB(df.at[i, 'symbol'], data)
    df.at[i, 'bb_pos'] =  round(bb_pos,2) # BB_display
    df.at[i, 'bb_link'] = address 
    s = settings.TREND_WINDOW_SIZE
    gfg_data = [0] * s
    # perform Mann-Kendall Trend Test   
    last_date_index = len(data.index)-1        
    for j in range(s):        
        gfg_data[j] = data['BBM_20_2.0'][last_date_index-s+1+j]    
    x = mk.original_test(gfg_data)            

    df.at[i, 'trend'] = x.trend
    df.at[i, 'slope'] = round(x.slope,2)    

def refresh_RSI(i, df, data):     
    last_action, last_action_price, recent, total_profit = RSI_strategy(data)          
    rsi = data['RSI_14'][-1]
    #RSI_display = last_action + " {:.2f}".format(last_action_price) if (recent and last_action != '') else "{:.2f}".format(rsi)      
    RSI_display = "{:.2f}".format(rsi)      
    address =  plot_RSI(df.at[i, 'symbol'], data)                 
    df.at[i, 'rsi'] =  round(rsi,2) #RSI_display
    df.at[i, 'rsi_link'] = address                  

def refresh_MFI(i, df, data):           
    last_action, last_action_price, recent, total_profit = MFI_strategy(data)  
    mfi = data['MFI_14'][-1]
    address =  plot_MFI(df.at[i, 'symbol'], data) 
    #MFI_display = last_action + " {:.2f}".format(last_action_price) if (recent and last_action != '') else "{:.2f}".format(mfi)          
    MFI_display = "{:.2f}".format(mfi)          
    df.at[i, 'mfi'] =  round(mfi,2) #MFI_display
    df.at[i, 'mfi_link'] = address    
    
def refresh_MACD(i, df, data):                
    last_action, last_action_price, recent, total_profit = MACD_strategy(data)  
    macd = data['MACD_12_26_9'][-1]
    address = plot_MACD(df.at[i, 'symbol'], data)
    #MACD_display = last_action + " {:.2f}".format(last_action_price) if (recent and last_action != '') else"{:.2f}".format(macd)          
    MACD_display = "{:.2f}".format(macd)          
    df.at[i, 'macd'] =  round(macd,2)#MACD_display
    df.at[i, 'macd_link'] = address                             


if __name__ == '__main__':

    import sys

    sys.path.append(r'\Users\jimhu\option_trader\src')
    
    from option_trader.admin.site import site

    site_name = 'mysite'

    mysite = site(site_name)

    mysite.refresh_site_monitor_list()