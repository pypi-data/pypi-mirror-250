from typing import List
from ...interface import IData
from .tick_data import TickData
from ...packer.market.history_tick_param_data_packer import HistoryTickParamDataPacker


class HistoryTickParamData(IData):
    def __init__(self, market_name: str = '', exchange_id: str = '', instrument_id: str = '', date: str = '', tick_list: List[TickData] = [], is_return_list: bool = False):
        super().__init__(HistoryTickParamDataPacker(self))
        self._MarketName: str = market_name
        self._ExchangeID: str = exchange_id
        self._InstrumentID: str = instrument_id
        self._Date: str = date
        self._TickList: list = tick_list
        self._IsReturnList: bool = is_return_list

    @property
    def MarketName(self):
        return self._MarketName

    @MarketName.setter
    def MarketName(self, value: str):
        self._MarketName = value

    @property
    def ExchangeID(self):
        return self._ExchangeID

    @ExchangeID.setter
    def ExchangeID(self, value: str):
        self._ExchangeID = value

    @property
    def InstrumentID(self):
        return self._InstrumentID

    @InstrumentID.setter
    def InstrumentID(self, value: str):
        self._InstrumentID = value

    @property
    def Date(self):
        return self._Date

    @Date.setter
    def Date(self, value: str):
        self._Date = value

    @property
    def TickList(self):
        return self._TickList

    @TickList.setter
    def TickList(self, value: List[TickData]):
        self._TickList = value

    @property
    def IsReturnList(self):
        return self._IsReturnList

    @IsReturnList.setter
    def IsReturnList(self, value: bool):
        self._IsReturnList = value
