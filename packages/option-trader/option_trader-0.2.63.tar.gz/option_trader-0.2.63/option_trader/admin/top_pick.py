

from option_trader.consts   import strategy as st
from option_trader.tools.trade_factory   import get_trade_targets, get_watchlist_trade_targets 
from option_trader.settings.trade_config import entryCrit, riskManager, runtimeConfig, marketCondition
#from option_trader.admin import position_summary
#from option_trader.admin import position
from option_trader.admin.position_summary import position_summary_col_name as pscl
from option_trader.admin.position         import position_col_name as pcl
from option_trader.admin import quote
from datetime import time, date, datetime, timedelta
from pytz import timezone

import logging

top_pick_schema =  "symbol TEXT,strategy TEXT,exp_date TEXT,spread REAL,open_price REAL,\
                    breakeven_l REAL,breakeven_h REAL,max_profit REAL,max_loss REAL,margin REAL,\
                    pnl REAL,win_prob REAL, trade_stock_price REAL, legs_desc TEXT,\
                    target_low REAL,target_high REAL,pick_date,\
                    PRIMARY KEY (symbol, strategy, exp_date)"       

class top_pick_col_name():
    SYMBOL           = 'symbol'
    STRATEGY         = 'strategy' 
    EXP_DATE         = 'exp_date'    
    SPREAD           = 'spread' 
    OPEN_PRICE       = 'open_price'     

    BREAKEVEN_L      = 'breakeven_l'
    BREAKEVEN_H      = 'breakeven_h'        
    MAX_PROFIT       = 'max_profit'  
    MAX_LOSS         = 'max_loss'
    MARGIN           = 'margin'
    
    PNL              = 'pnl'         
    WIN_PROB         = 'win_prob'              
    TRADE_STOCK_PRICE= 'trade_stock_price'                 
    LEGS_DESC        = 'legs_desc'
    
    TARGET_LOW       = 'target_low'
    TARGET_HIGH      = 'target_high'
    PICK_DATE        = 'pick_date'      

import logging
from option_trader.settings import app_settings
from option_trader.consts import asset
from option_trader.admin import site
import pandas as pd  

class top_pick_mgr():

    def __init__(self, this_site):
        self.this_site = this_site 
        self.logger = logging.getLogger(__name__)

    def get_top_pick_df(self, filter=[]):
        if app_settings.DATABASES == 'sqlite3':                 
            try:                  
                df = pd.read_sql_query("SELECT * FROM top_pick_table", self.this_site.top_pick_db_conn)                           
                df = df[df[asset.SYMBOL].isin(filter)] if len(filter)>0 else df           
                return df
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")        

    def refresh_top_picks(self, symbol_list):                 
        cursor = self.this_site.top_pick_db_conn.cursor()          
        cursor.execute("DELETE FROM top_pick_table")
        for symbol in symbol_list:
            df = get_watchlist_trade_targets([symbol], st.ALL_STRATEGY)             
            if df.shape[0] == 0:
                continue
            exp_date_list = df[pscl.EXP_DATE].unique()
            for exp_date in exp_date_list:
                de = df[df[pscl.EXP_DATE]==exp_date]            
                strategy_list = de[pscl.STRATEGY].unique()
                for strategy in strategy_list:
                    pick = de[de[pscl.STRATEGY]==strategy]            
                    if pick.shape[0] > 0:
                        pick.sort_values([pscl.WIN_PROB, pscl.PNL], ascending=False, inplace = True)
                        self.write_to_db(pick.head(1).to_dict('records')[0])                         

        self.this_site.top_pick_db_conn.commit()    

    class optionLegDesc():
        def __init__(self, leg):
            self.strike             = leg[pcl.STRIKE]
            self.otype              = leg[pcl.OTYPE] 
            self.open_action        = leg[pcl.OPEN_ACTION]
            self.exp_date           = leg[pcl.EXP_DATE]
            self.scale              = leg[pcl.SCALE]
            self.price              = leg[quote.PRICE]
            self.impliedVolatility  = leg[quote.IMPLIED_VOLATILITY]
            self.delta              = leg[quote.DELTA]     
            self.gamma              = leg[quote.GAMMA]
            self.theta              = leg[quote.THETA]
            self.vega               = leg[quote.VEGA]
            self.volume             = leg[quote.VOLUME]  
            self.openInterest       = leg[quote.OPEN_INTEREST]
            
    def write_to_db(self, s):

        cl = top_pick_col_name
        import json

        legdesc = []
        exp_date =s[cl.EXP_DATE]
        legs = s[cl.LEGS_DESC]
        for leg in legs:
            legdesc.append(json.dumps(vars(self.optionLegDesc(leg))))            

        legs_dump = json.dumps(legdesc)

        pick_date = str(datetime.now().astimezone(timezone(app_settings.TIMEZONE)))  

        field_names =  "'symbol', 'strategy', 'exp_date', 'spread', 'open_price',\
                        'breakeven_l','breakeven_h','max_profit','max_loss','margin',\
                        'pnl','win_prob', 'trade_stock_price','legs_desc',\
                        'target_low', 'target_high', 'pick_date'"   

        values =  '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?' 


        fields = [s[cl.SYMBOL], s[cl.STRATEGY], s[cl.EXP_DATE], s[cl.SPREAD], s[cl.OPEN_PRICE],\
                  s[cl.BREAKEVEN_L], s[cl.BREAKEVEN_H], s[cl.MAX_PROFIT], s[cl.MAX_LOSS], s[cl.MARGIN],\
                  s[cl.PNL], s[cl.WIN_PROB], s[cl.TRADE_STOCK_PRICE], legs_dump,\
                  s[cl.TARGET_LOW], s[cl.TARGET_HIGH], pick_date] 
        
        sql = "INSERT OR REPLACE INTO  top_pick_table ("+field_names+") VALUES("+values+")" 
        cursor = self.this_site.top_pick_db_conn.cursor()       
        cursor.execute(sql, fields)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        #self.this_site.top_pick_db_conn.commit()    


if __name__ == '__main__':

    import sys
    
    from option_trader.admin.site import site

    sys.path.append(r'\Users\jimhu\option_trader\src')

    mysite = site('mysite')

    tp =  top_pick_mgr(mysite)

    tp.refresh_top_picks(mysite.get_monitor_list())

    df = tp.get_top_pick_df()

    print(df)
