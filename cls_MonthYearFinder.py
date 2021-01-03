from datetime import datetime

class cls_MonthYearFinder:
    def __init__(self):
        self.m_nYear = datetime.today().year
        self.m_nMonth = datetime.today().month