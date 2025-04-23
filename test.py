from pyes.neural_networks.dataset_manager import DatasetManager

path_1 = 'test_resources/TEST_DATA_1.txt'
path_2 = 'test_resources/TEST_DATA_2.txt'

paths = [path_1, path_2]

manager = DatasetManager(paths, file_type='text')
manager.load_data()
print(manager.raw_data)