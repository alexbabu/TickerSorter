import requests
from bs4 import BeautifulSoup

class cls_DataGrabber:
    def __init__(self):
        self.__m_strUSER_AGENT__ = \
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        self.__m_dict_Headers__ = {'user-agent': self.__m_strUSER_AGENT__}
        self.__InitializeWithZero__()

    def GetData(self, strUrl):
        self.__m_strUrl__ = strUrl
        try:
            self.__m_dict_Response__ = requests.get(self.__m_strUrl__, headers=self.__m_dict_Headers__, verify=True)
        except:
            self.__InitializeWithZero__()
            return False
        self.__strResonseDoc__ = self.__m_dict_Response__.text
        if self.__m_dict_Response__.status_code == 200:
            self.m_dict_Soup = BeautifulSoup(self.__strResonseDoc__, 'html.parser')
        else:
            self.__InitializeWithZero__()
            return False
        return True

    def __InitializeWithZero__(self):
        self.__m_strUrl__ = ''
        self.m_dict_Soup = ''
        self.__m_dict_Response__ = ''