import cls_FileHandler as FH
import cls_RecordKeeper as RK
import cls_ProgressManager as PM
import cls_ThreadPool as TP


nMaxRecords = 100
nMinPercent = 200
nProgSkpVal = 100

objFH = FH.cls_FileHandler('Recommendations.xlsx', nMaxRecords)
objPM = PM.cls_ProgressManager(nProgSkpVal, objFH)
objRK = RK.cls_RecordKeeper(nMaxRecords, nMinPercent)
objTP = TP.cls_ThreadPool(objPM, objRK, objFH)

tempRecords = objFH.LoadRecords()
objRK.LoadRecord(tempRecords)
#objTP.StartThreads()

#objFH.SaveRecords(objRK.m_Record)
#del(objPM.m_lst_RemainingData[:])
#objPM.RecordProgress()

objTP.ProcessFailerList()