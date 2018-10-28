from pathlib import Path
from model.Param import *
from Preprocesser import Preprocesser
from model.visualizing import plot_loss, plot_prediction
from model.Model import Wavenet
import os
import warnings
from anomaly_detection import anomaly_detection
warnings.filterwarnings("ignore")

##### Initializing #####

# define paths
# use the Python3 Pathlib modul to create platform independent path
general_settings = Params.update(
    Path("C:/Users/zhouyuxuan/PycharmProjects/Masterarbeit/experiments/general_settings.json"))

# choose the channel for training
channel_name = 'p_0'

# remark: for prediction-based model, they only use the lagged data as feature and the original data as label,
# for reconstruction-based, they also include the original data as feature as well as label
# and the number of features should be even number(multiple of cpus), if it's odd number, then Keras will raise error message

# load the parameters for the experiment params.json file in model dir
model_dir = os.path.join(general_settings.experiments_path, general_settings.model_type)
json_path = Path(model_dir) / 'params.json'
params_train = Params.update(json_path)
##### handle the data #####
# preprocess the data
preprocesser = Preprocesser.from_tdm(general_settings.data_path, general_settings.channels, general_settings.time_index)
data_preprocessed_labeled = preprocesser.data

# save the preprocessed data in a numpy array
preprocesser.save(os.path.join(general_settings.processed_data_path, 'preprocessed data array'))

# select the channel out of the whole array
data_all_files = preprocesser.select_channel(channel_name)

# even if read just one file, indexing like e.g. 3:4 should be used in order to keep the outer []
train = data_all_files[4:8]

# train and evaluate the model setting
models, loss, predictions = Wavenet.train_and_predict(params_train, train, general_settings)
plot_loss(loss)
plot_prediction(train, predictions,general_settings.prediction_steps)
anomaly_detection(train, predictions, general_settings.detection_mode)