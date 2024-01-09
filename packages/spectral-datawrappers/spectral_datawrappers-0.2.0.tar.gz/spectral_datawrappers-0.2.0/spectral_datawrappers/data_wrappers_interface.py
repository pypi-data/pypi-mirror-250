from abc import ABC, abstractmethod


class DataWrapperInterface(ABC):

    @staticmethod
    @abstractmethod
    def _exported_features(self):
        """List of features that are exported by the data wrapper."""
        pass

    @staticmethod
    @abstractmethod
    def _config_keys(self, query):
        """List of config keys that are required by the data wrapper."""
        pass

    @abstractmethod
    def request(self, input: str) -> list:
        """Returns a map of features and their values."""
        pass
