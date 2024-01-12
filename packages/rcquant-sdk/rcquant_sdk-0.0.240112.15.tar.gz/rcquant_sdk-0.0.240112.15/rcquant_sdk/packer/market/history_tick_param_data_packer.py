from ...interface import IPacker


class HistoryTickParamDataPacker(IPacker):
    def __init__(self, obj) -> None:
        super().__init__(obj)

    def obj_to_tuple(self):
        return [str(self._obj.MarketName), str(self._obj.ExchangeID), str(self._obj.InstrumentID), str(self._obj.Date),
                list(self._obj.TickList)]

    def tuple_to_obj(self, t):
        if len(t) >= 5:
            self._obj.MarketName = t[0]
            self._obj.ExchangeID = t[1]
            self._obj.InstrumentID = t[2]
            self._obj.Date = t[3]
            self._obj.TickList = t[4]

            return True
        return False
