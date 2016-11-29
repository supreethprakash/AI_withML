from sys import argv
import train
from utils import Train
import test
import pickle


def serialize_model(model,filename):
    try:
        f_ptr = open(filename,"wb")
        pickle.dump(model,f_ptr)
        f_ptr.close()
    except Exception:
        print("Serialization Failed")
        return False


def deserialize_model(model_filename):
    try:
        f_ptr = open(model_filename,"rb")
        obj = pickle.load(f_ptr)
        f_ptr.close()
        return obj
    except Exception:
        print("Deserialization Failed")
        return False


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
