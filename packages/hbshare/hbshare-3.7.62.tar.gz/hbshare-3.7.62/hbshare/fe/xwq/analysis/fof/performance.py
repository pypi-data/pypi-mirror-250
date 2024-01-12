# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
import pandas as pd


class Performance:
    def __init__(self, start_date, end_date, data_path, fof_list, bmk_list):
        self.start_date = start_date
        self.end_date = end_date
        self.data_path = data_path
        self.fof_list = fof_list
        self.bmk_list = bmk_list
        self.load()

    def load(self):
        fof_nav_list = []
        for fof in self.fof_list:
            fof_nav = HBDB().read_private_fund_cumret_given_code(fof, self.start_date, self.end_date)
            fof_nav_list.append(fof_nav)
        self.fof_nav = pd.concat(fof_nav_list)
        self.fof_nav['FUND_CODE'] = self.fof_nav['FUND_CODE'].astype(str)
        self.fof_nav['TRADE_DATE'] = self.fof_nav['TRADE_DATE'].astype(str)
        self.fof_nav['ADJ_NAV'] = self.fof_nav['ADJ_NAV'].astype(float)
        self.fof_nav = self.fof_nav[['FUND_CODE', 'TRADE_DATE', 'ADJ_NAV']]
        self.fof_nav = self.fof_nav.sort_values(['FUND_CODE', 'TRADE_DATE'])

        self.bmk_nav = HBDB().read_private_index_daily_k_given_indexs(self.bmk_list, self.start_date, self.end_date)
        self.bmk_nav['INDEX_SYMBOL'] = self.bmk_nav['INDEX_SYMBOL'].astype(str)
        self.bmk_nav['TRADE_DATE'] = self.bmk_nav['TRADE_DATE'].astype(str)
        self.bmk_nav['CLOSE_INDEX'] = self.bmk_nav['CLOSE_INDEX'].astype(float)
        self.bmk_nav = self.bmk_nav[['INDEX_SYMBOL', 'TRADE_DATE', 'CLOSE_INDEX']]
        self.bmk_nav = self.bmk_nav.sort_values(['INDEX_SYMBOL', 'TRADE_DATE'])


        return


if __name__ == '__main__':
    start_date = '20200101'
    end_date = '20231130'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/fof/'
    fof_list = ['SSD164', 'STR813', 'STQ402']
    bmk_list = ['HB0011', 'HB0018', 'H11001.CSI']
    Performance(start_date, end_date, data_path, fof_list, bmk_list)