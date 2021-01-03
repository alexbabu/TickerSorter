from enum import IntEnum

class enum_ROrder(IntEnum):
    QUERRY = 0
    CPRICE = 1
    EPRICE = 2
    DIVDND = 3
    GRPERC = 4


class cls_RecordKeeper:
    def __init__(self, nMaxRecords, nMinPercent):
        self.__m_nMaxRecords__ = nMaxRecords
        self.__m_nMinPercent__ = nMinPercent

    def LoadRecord(self, Record):
        self.m_Record = Record

    def AddEntry(self, Record):
        if len(Record) != 4:
            return False
        else:
            nGPerc = self.__CalculateGPerc__(Record)
            if nGPerc >= self.__m_nMinPercent__:
                Record.append(nGPerc)
                if len(self.m_Record) == 0:
                    self.m_Record.append(Record)
                    return True
                for nCnt, entry in enumerate(self.m_Record):
                    if nGPerc > entry[enum_ROrder.GRPERC]:
                        self.m_Record.insert(nCnt, Record)
                        self.__RecordLengthCheck__()
                        return True
            return False

    def __CalculateGPerc__(self, Record):
        if Record[enum_ROrder.CPRICE] > 0:
            nNumerator = Record[enum_ROrder.EPRICE] + Record[enum_ROrder.DIVDND]- Record[enum_ROrder.CPRICE]
            return nNumerator/Record[enum_ROrder.CPRICE] * 100
        else:
            return 0

    def __RecordLengthCheck__(self):
        if len(self.m_Record) > self.__m_nMaxRecords__:
            self.m_Record.pop()
            return True
        else:
            return False