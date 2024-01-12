import uunet.multinet as ml

class TemporalTextNetwork(object):

    def __init__(self):
        self.network = ml.empty()

        ml.add_layers(n = self.network, layers = ['U', 'M'], directed = [True, True])

        layers = {
            'layer1': ['U'],
            'layer2': ['M'],
            'dir': [True]
        }

        ml.set_directed(self.network, layers)
