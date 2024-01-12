import uunet.multinet as ml

from enum import Enum

class NetworkType(Enum):
    PURE = 0,
    OTHER = 0


class TemporalTextNetwork(object):
    def __init__(self):
        self._network = ml.empty()

        ml.add_layers(n = self._network, layers = ['U', 'M'], directed = [True, True])

        layers = {
            'layer1': ['U'],
            'layer2': ['M'],
            'dir': [True]
        }

        ml.set_directed(self._network, layers)


    def is_directed(self) -> bool:
        return ml.is_directed(self._network)
