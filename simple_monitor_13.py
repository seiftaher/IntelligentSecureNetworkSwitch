import pickle
from simple_switch_13 import SimpleSwitch13
from ryu.lib import hub
import numpy as np
from Transformation import dataTransformation
    
class SimpleMonitor13(SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)
        self.ml = pickle.load(open('finalized_model.sav','rb'))

    def _monitor(self):
        while True:
            self._send_to_ml()
            hub.sleep(10)

    def _send_to_ml(self):
        packets = self.packets
        self.packets=[]
        arr = dataTransformation(packets)
        if arr:
            keys = list(arr.keys())
            data = np.array(list(arr.values()))
            results = self.ml.predict(data)
            for i in range(len(results)):
                self.logger.info(f'{keys[i]} : {results[i]}')
                



