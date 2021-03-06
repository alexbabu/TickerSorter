import cls_TickerandCPGrabber as TCPG
import json


class cls_ProgressManager:
    def __init__(self, nProgSkpVal, objFH, objFL):
        self.__m_objFL__ = objFL
        self.__m_objFH__ = objFH
        self.m_nSkipVal = nProgSkpVal
        self.m_lst_RemainingData = []
        self.__GetRemainingDataEntries__()

    def RecordProgress(self):
        with open('Remaining_data.txt', 'w') as fp:
            for entry in self.m_lst_RemainingData:
                strToWrite = entry[0] + ' ' + str(entry[1]) + '\n'
                fp.write(strToWrite)
        fp.close()

    def __GetTickerandCP__(self):
        objTCPGrabber = TCPG.cls_TickerandPCGrabber()
        with open('data.json', 'w') as fp:
            json.dump(objTCPGrabber.data, fp)
            fp.close()
        self.__GetDataEntries__()

    def __GetDataEntries__(self):
        with open('data.json', 'r') as fp:
            self.m_dict_data = json.load(fp)
            # self.m_nTotalEntryNo = len(self.m_dict_data)
            fp.close()

    def __GetRemainingDataEntries__(self):
        with open('Remaining_data.txt', 'r') as fp:
            lst_strTempRemainingData = fp.readlines()
        for entry in lst_strTempRemainingData:
            strData = entry.strip('\n')
            lst_strSymbolCP = strData.split(' ')
            self.m_lst_RemainingData.append([lst_strSymbolCP[0], float(lst_strSymbolCP[1])])
        if len(self.m_lst_RemainingData) == 0:
            self.__m_objFH__.__ClearRecords__()
            self.__GetTickerandCP__()
            self.__GetDataEntries__()
            self.__FormDataEntriesToProcess__()
        else:
            self.__GetDataEntries__()
            self.m_nTotalEntryNo = len(self.m_lst_RemainingData)

    def __FormDataEntriesToProcess__(self):
        lst_strExchanges = ['NYSE', 'Nasdaq', 'New York Stock Exchange', 'NASDAQ', 'BATS']
        for entry in self.m_dict_data:
            bExchangeFlag = False
            bNeverFailed = False
            if 'exchange' in entry:
                strExchange = entry['exchange']
                for Exchange in lst_strExchanges:
                    if Exchange in strExchange:
                        bExchangeFlag = True
                        break
            strSymbol = entry['symbol']
            bNeverFailed = False
            if not self.__m_objFL__.CheckifTickerFailedBefore(strSymbol):
                bNeverFailed = True
            if bNeverFailed and bExchangeFlag:
                self.m_lst_RemainingData.append([entry['symbol'], entry['price']])
        self.m_nTotalEntryNo = len(self.m_lst_RemainingData)