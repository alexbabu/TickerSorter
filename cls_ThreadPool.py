from concurrent.futures import ThreadPoolExecutor
import threading
import cls_PredictionGrabber as PG

class cls_ThreadPool:
    def __init__(self, objPM, objRK, objFH):
        self.__m_nNoofThreads__ = 25
        self.__m_Executer__ = ThreadPoolExecutor(self.__m_nNoofThreads__)
        self.__m_objPM__ = objPM
        self.__m_objRK__ = objRK
        self.__m_objFH__ = objFH
        self.__m_ThreadLock__ = threading.Lock()
        self.__m_EntryCnt__ = 0

    def __ExtractTickerandCP__(self):
        lstTemp = []
        self.__m_ThreadLock__.acquire()
        if(len(self.__m_objPM__.m_lst_RemainingData) > 0):
            lstTemp = self.__m_objPM__.m_lst_RemainingData.pop(0)
        self.__m_ThreadLock__.release()
        return lstTemp

    def __ProcessPredictedData(self, arr_nPredictions, lst_TickerCP):
        self.__m_ThreadLock__.acquire()
        self.__m_EntryCnt__ = self.__m_EntryCnt__ + 1
        if arr_nPredictions:
            self.__m_objRK__.AddEntry([lst_TickerCP[0], lst_TickerCP[1], arr_nPredictions[0],
                                       arr_nPredictions[1]])
        if self.__m_EntryCnt__ % self.__m_objPM__.m_nSkipVal == 0 and self.__m_EntryCnt__ != 0:
            self.__m_objFH__.SaveRecords(self.__m_objRK__.m_Record)
            self.__m_objPM__.RecordProgress()
            print('Analysed %d entries' % self.__m_EntryCnt__)
            # print('Found %d Valid Entries' % nValidEntries)
            nRemainingPerc = float(self.__m_EntryCnt__) / float(self.__m_objPM__.m_nTotalEntryNo) * 100
            print(str(nRemainingPerc) + '% Finished')
        # print(self.__m_EntryCnt__, lst_TickerCP[0], lst_TickerCP[1], arr_nPredictions)
        self.__m_ThreadLock__.release()

    def __StartProcessing__(self):
        objPG = PG.cls_PredictionGrabber()
        while(True):
            lst_TickerCP = self.__ExtractTickerandCP__()
            if len(lst_TickerCP):
                arr_nPredictions = objPG.GetPredictionData(str(lst_TickerCP[0]))
                self.__ProcessPredictedData(arr_nPredictions, lst_TickerCP)
            else:
                break

    def StartThreads(self):
        self.__m_Executer__.submit(self.__StartProcessing__(), )



