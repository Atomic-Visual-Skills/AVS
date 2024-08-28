from abc import ABC, abstractmethod

class ModelInterface(ABC):
    @abstractmethod
    def run(self, image_path, prompt):
        pass