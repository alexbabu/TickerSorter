from urllib.request import urlopen
import json

class cls_TickerandPCGrabber:
    def __init__(self):
        url = ("https://financialmodelingprep.com/api/v3/stock/list?apikey=6d3203b2908499244cfaf893209b3985")
        response = urlopen(url)
        tempunicodedata = response.read()
        self.data = self.__json_loads_byteified__(tempunicodedata)

    def __json_load_byteified__(self, file_handle):
        return self.__byteify__(
            json.load(file_handle, object_hook=self.__byteify__),
            ignore_dicts=True
        )

    def __json_loads_byteified__(self, json_text):
        return self.__byteify__(
            json.loads(json_text, object_hook=self.__byteify__),
            ignore_dicts=True
        )

    def __byteify__(self, data, ignore_dicts=False):
        # if this is a unicode string, return its string representation
        if isinstance(data, str):
            return data
        # if this is a list of values, return list of byteified values
        if isinstance(data, list):
            return [self.__byteify__(item, ignore_dicts=True) for item in data]
        # if this is a dictionary, return dictionary of byteified keys and values
        # but only if we haven't already byteified it
        if isinstance(data, dict) and not ignore_dicts:
            return {
                self.__byteify__(key, ignore_dicts=True): self.__byteify__(value, ignore_dicts=True)
                for key, value in data.items()
            }
        # if it's anything else, return it in its original form
        return data