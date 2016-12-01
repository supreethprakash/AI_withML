from sys import argv
import train
from utils import Train
import test
import pickle
from os import linesep


def serialize_model(obj, filename):
    try:
        f_ptr = open(filename,"wb")
        pickle.dump(obj, f_ptr)
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
dataset_dir = argv[2].rstrip("/")
model_file = argv[3]
fraction = None


def write_top_words_to_file(obj, filename):
    data = obj.data
    fp = open(filename,"w")
    for topic in data.keys():
        string_formatter = [topic+":"]
        top_words = data[topic].most_common(10)
        for word in top_words:
            string_formatter.append(word[0])
        line = ' '.join(string_formatter)
        fp.write(line)
        fp.write(linesep)
    fp.close()

if mode == "train":
    if len(argv) != 5:
        print("USAGE: python topics.py mode dataset-directory model-file [fraction]")
        exit(1)
    fraction = float(argv[4])
    print("Training started...")
    print("Please wait as lower fraction rates could take a long time to execute")
    model = train.train_data(dataset_dir, fraction)
    write_top_words_to_file(model,"distinctive_words.txt")
    serialize_model(model,model_file)
    print("Model File created")
    exit(0)

if mode == "test":
    model = deserialize_model(model_file)
    result = test.test_data(model, dataset_dir)
    print(result)
    exit(0)

print("Operation not supported")
exit(1)
