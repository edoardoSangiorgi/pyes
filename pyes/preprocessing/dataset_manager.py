from ..data_io import loaders

class DatasetLoader():

    def __init__(self):
        
        self.data_path = None
        self.dataset = None

        ## in case of a labeled dataset (very common)
        self.labels = None
        self.data_classes = None


    