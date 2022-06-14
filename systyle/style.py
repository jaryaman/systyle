import pkgutil
import yaml
import matplotlib.pyplot as plt

class Style:
    def __init__(self, config: dict):
        self.config = config

    @classmethod
    def from_default(cls):
        mplrc = pkgutil.get_data(__package__, 'matplotlibrc/systyle.matplotlibrc')
        mplrc = mplrc.decode('utf-8')
        mplrc = yaml.safe_load(mplrc)
        return cls(mplrc)

    def apply(self):
        plt.style.use(self.config)
