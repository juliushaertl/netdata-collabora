from bases.FrameworkServices.SimpleService import SimpleService

import requests
import csv

# Netdata 
priority = 90000

ORDER = [
    'times',
    'documents',
    'threads',
    'all',
]

CHARTS = {
    'documents': {
        'options': [None, 'Documents', 'documents', 'Documents', 'documents', 'line'],
        'lines': [
            ['document_active_views_active_count_total'],
            ['document_active_views_expired_count_total'],
            ['document_active_views_expired_count_total'],
            ['document_expired_views_all_count_total']
        ]
    },
    'times': {
        'options': [None, 'times', 'Times', 'WOPI', 'times', 'line'],
        'lines': [
            ['document_active_wopi_upload_duration_total_milliseconds'],
            ['document_active_wopi_download_duration_total_milliseconds'],
        ]
    },
    'threads': {
        'options': [None, 'Threads', 'threads', 'Collabora', 'threads', 'line'],
        'lines': [
            ['loolwsd_thread_count', 'forkit_thread_count', 'kit_thread_count_total']
        ]
    }
}

class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        try:
            self.baseurl = str(self.configuration['baseurl'])
            self.user = str(self.configuration['user'])
            self.password = str(self.configuration['password'])
        except (KeyError, TypeError):
            self.baseurl = "http://localhost:9980"
            self.user = ''
            self.password = ''
        self.order = ORDER
        self.definitions = CHARTS

    @staticmethod
    def check():
        return True

    def get_data(self):
        url = self.baseurl + "/lool/getMetrics"

        r = requests.get(url = url, auth=requests.auth.HTTPBasicAuth(self.user, self.password))

        data = dict()
        for line in r.text.splitlines():
            if line != "": # add other needed checks to skip titles
                cols = line.split(" ")
                #if cols[0] not in self.charts['all']:
                #    self.charts['all'].add_dimension([cols[0]])

                data[cols[0]] = cols[1]
        
        return data


