import cls_DataGrabber as DG
import re

class cls_PredictionGrabber:
    def __init__(self):
        self.strYahooUrl = 'https://finance.yahoo.com/quote/'
        self.strCnnUrl = 'https://money.cnn.com/quote/forecast/forecast.html?symb='
        self.objDG = DG.cls_DataGrabber()

    def GetPredictionData(self, strTicker):
        arr_nYahooData = self.__GetYahooData__(strTicker)
        if arr_nYahooData and len(arr_nYahooData) > 0:
            arr_nCnnData = self.__GetCnnData__(strTicker)
            if arr_nCnnData and len(arr_nCnnData) > 0 and arr_nCnnData[0] > 3:
                return [arr_nCnnData[2], arr_nYahooData[1]]

    def __GetCnnData__(self, strTicker):
        strUrl = self.strCnnUrl + strTicker
        if self.objDG.GetData(strUrl):
            dict_Soup                           = self.objDG.m_dict_Soup
            tempText                            = dict_Soup.text
            lst_strCandidates                   = tempText.split('ForecastThe ')
            if len(lst_strCandidates) > 1:
                try:
                    strAnalystNo                        = lst_strCandidates[1].split(' ')[0]
                    nAnalystNo                          = int(strAnalystNo)
                    lst_strMedEstimateCandidates        = lst_strCandidates[1].split('a median target of ')
                    strMedEstimate                      = lst_strMedEstimateCandidates[1].split(',')[0]
                    nMedEstimate                        = float(re.findall("\d+(?:,\d+)?\.\d+", strMedEstimate)[0])
                    lst_strHighEstimateCandidates       = lst_strCandidates[1].split('a high estimate of ')
                    strHighEstimate                     = lst_strMedEstimateCandidates[1].split(' ')[0]
                    nHighEstimate                       = float(re.findall("\d+(?:,\d+)?\.\d+", strHighEstimate)[0])
                    lst_strLowEstimateCandidates        = lst_strCandidates[1].split('a low estimate of ')
                    strLowEstimate                      = lst_strLowEstimateCandidates[1].split(' ')[0]
                    nLowEstimate                        = float(re.findall("\d+(?:,\d+)?\.\d+", strLowEstimate)[0])
                except:
                    return []
                return [nAnalystNo, nLowEstimate, nMedEstimate, nHighEstimate]
            else:
                return []

    def __GetYahooData__(self, strTicker):
        strUrl = self.strYahooUrl + strTicker
        if self.objDG.GetData(strUrl):
            try:
                dict_Soup               = self.objDG.m_dict_Soup
                nYahooEstimatedPrice    = self.__CollectEstimatedPrice__(dict_Soup)
                nDividend               = self.__CollectDividendValue__(dict_Soup)
            except:
                return []
            return [nYahooEstimatedPrice, nDividend]
        else:
            return []

    def __CollectEstimatedPrice__(self, dict_Soup):
        try:
            lst_strCandidate        = dict_Soup.text.split('1y Target Est')
            lst_strConfCandidate    = lst_strCandidate[1].split('Fair Value')
            nEstimatedPrice         = float(re.findall("\d+(?:,\d+)?\.\d+", lst_strConfCandidate[0])[0])
        except:
            return 0
        return nEstimatedPrice

    def __CollectDividendValue__(self, dict_Soup):
        try:
            lst_strCandidate        = dict_Soup.text.split('Forward Dividend & Yield')
            lst_strConfCandidate    = lst_strCandidate[1].split('(')
            nDividend               = float(re.findall("\d+(?:,\d+)?\.\d+", lst_strConfCandidate[0])[0])
        except:
            return 0
        return nDividend