import openpyxl as xl
import cls_MonthYearFinder as MYF

class cls_FileHandler:
    def __init__(self, strFileName, nMaxRecords):
        self.strFileName = strFileName
        self.__m_fExcel__ = xl.load_workbook(strFileName)
        objMYF = MYF.cls_MonthYearFinder()
        strWorkSheetName = str(objMYF.m_nMonth) + '_' + str(objMYF.m_nYear)
        try:
            self.__m_xl_CurrentSheet__ = self.__m_fExcel__.get_sheet_by_name(strWorkSheetName)
        except:
            self.__m_fExcel__.create_sheet(strWorkSheetName)
            self.__m_xl_CurrentSheet__ = self.__m_fExcel__.get_sheet_by_name(strWorkSheetName)
        self.__m_nMaxRecords__ = nMaxRecords

    def SaveRecords(self, Record):
        for nRows in range(2, len(Record) + 1):
            nCnt = nRows - 2
            strCellName = "A%d" % (nRows)
            self.__m_xl_CurrentSheet__[strCellName].value = Record[nCnt][0]
            strCellName = "B%d" % (nRows)
            self.__m_xl_CurrentSheet__[strCellName].value = round(float(Record[nCnt][1]), 4)
            strCellName = "C%d" % (nRows)
            self.__m_xl_CurrentSheet__[strCellName].value = round(float(Record[nCnt][2]), 4)
            strCellName = "D%d" % (nRows)
            self.__m_xl_CurrentSheet__[strCellName].value = round(float(Record[nCnt][3]), 4)
            strCellName = "E%d" % (nRows)
            self.__m_xl_CurrentSheet__[strCellName].value = round(float(Record[nCnt][4]), 4)

        self.__m_fExcel__.save(self.strFileName)
        print('Successfully saved file...')

    def LoadRecords(self):
        Record = [([0] * 5) for rows in range(self.__m_nMaxRecords__)]
        for nRows in range(2, self.__m_nMaxRecords__ + 1):
            strCellName = "A%d" % (nRows)
            if self.__m_xl_CurrentSheet__[strCellName].value:
                Record[nRows - 2][0] = self.__m_xl_CurrentSheet__[strCellName].value
                strCellName = "B%d" % (nRows)
                Record[nRows - 2][1] = self.__m_xl_CurrentSheet__[strCellName].value
                strCellName = "C%d" % (nRows)
                Record[nRows - 2][2] = self.__m_xl_CurrentSheet__[strCellName].value
                strCellName = "D%d" % (nRows)
                Record[nRows - 2][3] = self.__m_xl_CurrentSheet__[strCellName].value
                strCellName = "E%d" % (nRows)
                Record[nRows - 2][4] = self.__m_xl_CurrentSheet__[strCellName].value
        return Record