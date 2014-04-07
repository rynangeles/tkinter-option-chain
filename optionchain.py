import requests
import demjson

OPTION_CHAIN_URL = "https://www.google.com/finance/option_chain"

class OptionChain:

    retrieve_success = False
    __options = {}

    def __init__(self, query, *args, **kwargs):
        self.__request_url = OPTION_CHAIN_URL
        self.__params = {
            'q' : query,
            'output' : kwargs.get('output','json')
        }
        self.__options_expirations = self.__request_option().get('expirations')
        self.__options['puts'] = []
        self.__options['calls'] = []
        self.request_option_chain()
    
    def __request_option(self, expiration=None):
        if expiration is not None:
            self.__params['expd'] = expiration['d']
            self.__params['expm'] = expiration['m']
            self.__params['expy'] = expiration['y']

        request = requests.get(self.__request_url, params=self.__params)

        if request.status_code == 200:
            return demjson.decode(request.text) 

        else:
            raise Exception("Unable to retrieve data")

    def request_option_chain(self):
        data_percentage = 0
        each_percentage = 100.0 / len(self.__options_expirations) 
        for index, expiry in enumerate(self.__options_expirations):
            data = self.__request_option(expiry)
            self.__options['puts'] += data.get('puts')
            self.__options['calls'] += data.get('calls')
            data_percentage += each_percentage
            print "%.1f%s" % (float(data_percentage), "%")
            
            if (index+1) == len(self.__options_expirations):
                self.retrieve_success = True

    def get_all_options(self, key=None):
        if not key:
            return self.__options

        else:
            try:
                return self.__options[key]

            except KeyError:
                raise Exception("Unable to retrieve data with key '%s'" % key)

