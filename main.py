import cls_FileHandler as FH
import cls_RecordKeeper as RK
import cls_ProgressManager as PM
import cls_ThreadPool as TP
import cls_FailerList as FL

nMaxRecords = 100
nMinPercent = 100
nProgSkpVal = 100

objFL = FL.cls_FailerList()
objFH = FH.cls_FileHandler('Recommendations.xlsx', nMaxRecords)
objPM = PM.cls_ProgressManager(nProgSkpVal, objFH, objFL)
objRK = RK.cls_RecordKeeper(nMaxRecords, nMinPercent)
objTP = TP.cls_ThreadPool(objPM, objRK, objFH, objFL)

tempRecords = objFH.LoadRecords()
objRK.LoadRecord(tempRecords)
objTP.StartThreads()

objFH.SaveRecords(objRK.m_Record)
del(objPM.m_lst_RemainingData[:])
objPM.RecordProgress()

objTP.ProcessFailerList()