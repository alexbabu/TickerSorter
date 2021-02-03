from datetime import datetime
import copy
import threading
import cls_PredictionGrabber as PG

class cls_ThreadPool:
    def __init__(self, objPM, objRK, objFH, objFL):
        self.__m_nNoofThreads__ = 1
        self.__m_objPM__ = objPM
        self.__m_objRK__ = objRK
        self.__m_objFH__ = objFH
        self.__m_ThreadLock__ = threading.Lock()
        self.__m_EntryCnt__ = 0
        self.__m_objFL__ = objFL

    def __ExtractTickerandCP__(self):
        lstTemp = []
        self.__m_ThreadLock__.acquire()
        if(len(self.__m_objPM__.m_lst_RemainingData) > 0):
            lstTemp = self.__m_objPM__.m_lst_RemainingData.pop(0)
            self.__m_EntryCnt__ = self.__m_EntryCnt__ + 1
        self.__m_ThreadLock__.release()
        return lstTemp

    def __ProcessPredictedData__(self, arr_nPredictions, lst_TickerCP):
        self.__m_ThreadLock__.acquire()
        if arr_nPredictions:
            self.__m_objRK__.AddEntry([lst_TickerCP[0], lst_TickerCP[1], arr_nPredictions[0],
                                       arr_nPredictions[1]])
        if self.__m_EntryCnt__ % self.__m_objPM__.m_nSkipVal == 0 and self.__m_EntryCnt__ != 0:
            self.__m_objFH__.SaveRecords(self.__m_objRK__.m_Record)
            self.__m_objPM__.RecordProgress()
            self.__m_objFL__.SaveFailerList()
            print('Analysed %d entries' % self.__m_EntryCnt__)
            nRemainingPerc = float(self.__m_EntryCnt__) / float(self.__m_objPM__.m_nTotalEntryNo) * 100
            time_now = datetime.now()
            print(str(nRemainingPerc) + '% Finished at ' + time_now.strftime("%d/%m/%Y %H:%M:%S"))
        self.__m_ThreadLock__.release()

    def __StartProcessing__(self):
        objPG = PG.cls_PredictionGrabber()
        while(True):
            lst_TickerCP = self.__ExtractTickerandCP__()
            if len(lst_TickerCP):
                arr_nPredictions = objPG.GetPredictionData(str(lst_TickerCP[0]))
                if len(arr_nPredictions):
                    self.__ProcessPredictedData__(arr_nPredictions, lst_TickerCP)
                else:
                    self.__m_ThreadLock__.acquire()
                    self.__m_objFL__.AddEntrytoFailerList(lst_TickerCP[0])
                    self.__m_ThreadLock__.release()
            else:
                break

    def StartThreads(self):
        self.__m_threads__ = [threading.Thread(target= self.__StartProcessing__(), args=(self,))] * \
                             self.__m_nNoofThreads__
        [thread.start() for thread in self.__m_threads__]
        [thread.join() for thread in self.__m_threads__]
        self.__m_objFL__.SaveFailerList()

    def __GetFailerTicker__(self):
        if len(self.__m_arr_strDeepCopiedFailedTickers):
            return self.__m_arr_strDeepCopiedFailedTickers.pop(0)
        else:
            return ''

    def __SartFailerListProcessing__(self):
        objPG = PG.cls_PredictionGrabber()
        while(True):
            self.__m_ThreadLock__.acquire()
            strTicker = self.__GetFailerTicker__()
            self.__m_nCurrentFailerCnt__ = self.__m_nCurrentFailerCnt__ + 1
            self.__m_ThreadLock__.release()
            if len(strTicker) == 0:
                break
            arr_nPredictions = objPG.GetPredictionData(strTicker)
            if len(arr_nPredictions):
                self.__m_ThreadLock__.acquire()
                self.__m_objFL__.EraseEntryfromFailerList(strTicker)
                print('Removed ' + strTicker + ' from Failer List...')
                self.__m_ThreadLock__.release()
            self.__m_ThreadLock__.acquire()
            if self.__m_nCurrentFailerCnt__ % self.__m_objPM__.m_nSkipVal == 0 and self.__m_nCurrentFailerCnt__ != 0:
                print('Analysed %d entries' % self.__m_nCurrentFailerCnt__)
                nRemainingPerc = float(self.__m_nCurrentFailerCnt__) / float(self.__m_nTotalFailerCnt__) * 100
                time_now = datetime.now()
                print(str(nRemainingPerc) + '% Finished at ' + time_now.strftime("%d/%m/%Y %H:%M:%S"))
                self.__m_objFL__.SaveFailerList()
            self.__m_ThreadLock__.release()

    def ProcessFailerList(self):
        print('Processing Failer List...')
        self.__m_arr_strDeepCopiedFailedTickers = copy.deepcopy(self.__m_objFL__.m_arr_strFailerTickers)
        self.__m_nTotalFailerCnt__              = len(self.__m_arr_strDeepCopiedFailedTickers)
        self.__m_nCurrentFailerCnt__            = 0
        self.__m_FailerProcessingThreads__ = [threading.Thread(target=self.__SartFailerListProcessing__(), args=(self,))] * \
                             self.__m_nNoofThreads__
        [thread.start() for thread in self.__m_FailerProcessingThreads__]
        [thread.join() for thread in self.__m_FailerProcessingThreads__]
        self.__m_objFL__.SaveFailerList()
        print('Finished Processing Failer List...')



