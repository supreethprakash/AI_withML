from sys import argv
import train
from utils import Train
import test
import pickle


def serialize_model(model,filename):
    try:
        pickle.dump(model,open(filename,"wb"))
    except Exception:
        print("Serialization Failed")
        return False


def deserialize_model(model_filename):
    return pickle.load(open(model_filename,"rb"))


if len(argv) < 4:
    print("USAGE: python topics.py mode dataset-directory model-file [fraction]")
    exit(1)

mode = argv[1]
dataset_dir = argv[2]
model_file = argv[3]
fraction = None
if mode == "train":
    if len(argv) != 5:
        print("USAGE: python topics.py mode dataset-directory model-file [fraction]")
        exit(1)
    fraction = float(argv[4])
    model = train.train_data(dataset_dir, fraction)
    serialize_model(model,model_file)
    print("Model File created")
    exit(0)
if mode == "test":
    model = deserialize_model(model_file)
    results = test.test_data(model, dataset_dir)
    print("Handle Results now")
    exit(0)

print("Operation not supported")
exit(1)
