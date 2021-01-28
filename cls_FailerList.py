class cls_FailerList:
    def __init__(self):
        self.m_arr_strFailerTickers = []
        with open('FailerList.txt', 'r') as fp:
            arr_strFailedTickers = fp.readlines()
            fp.close()
        self.m_arr_strFailerTickers = [entry.strip('\n') for entry in arr_strFailedTickers]

    def SaveFailerList(self):
        with open('FailerList.txt', 'w') as fp:
            fp.writelines([entry + '\n' for entry in self.m_arr_strFailerTickers])
            fp.close()

    def AddEntrytoFailerList(self, strTicker):
        self.m_arr_strFailerTickers.append(strTicker)

    def EraseEntryfromFailerList(self, strTicker):
        self.m_arr_strFailerTickers.remove(strTicker)

    def CheckifTickerFailedBefore(self, strTicker):
        if strTicker in self.m_arr_strFailerTickers:
            return True
        else:
            return False

