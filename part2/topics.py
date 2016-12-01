from sys import argv
import pickle
from os import linesep

import train
from utils import Model
import test


# Serializes the model object into a file using pickle
def serialize_model(obj, filename):
    try:
        print("Serializing the model to %s" % filename)
        f_ptr = open(filename, "wb")
        pickle.dump(obj, f_ptr)
        f_ptr.close()
    except pickle.PickleError as p:
        print("Serialization Failed")
        print("Error: %s" % p.message)
        exit(1)
    except Exception as e:
        print("Something went wrong during serialization")
        print("Error: %s" % e.message)
        exit(1)

# De-serializes the file into Model object.
def deserialize_model(model_filename):
    try:
        print("Deserializing from file %s" % model_filename)
        f_ptr = open(model_filename, "rb")
        obj = pickle.load(f_ptr)
        f_ptr.close()
        return obj
    except pickle.PickleError as p:
        print("Deserialization Failed")
        print("Error: %s" % p.message)
        exit(1)
    except Exception as e:
        print("Something went wrong during deserialization")
        print("Error: %s" % e.message)
        exit(1)


if len(argv) < 4:
    print("USAGE: python topics.py mode dataset-directory model-file [fraction]")
    exit(1)

# mode - test/train
mode = argv[1]
# directory where the dataset is present
dataset_dir = argv[2].rstrip("/")
# Name of the model file
model_file = argv[3]
# Fraction of classified data available for training
fraction = None


# Handles writing the top ten words into the file after training
def write_top_words_to_file(obj, filename):
    data = obj.data
    fp = open(filename, "w")
    for topic in data.keys():
        string_formatter = [topic + ":"]
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
    print("Training started.")
    print("Please wait as it could take a while to create model...")
    model = train.train_data(dataset_dir, fraction)
    write_top_words_to_file(model, "distinctive_words.txt")
    print("Top 10 words at each topic is written into distinctive_words.txt.")
    serialize_model(model, model_file)
    print("Model File created")
    exit(0)

if mode == "test":
    model = deserialize_model(model_file)
    print("Model loaded successfully.")
    result = test.test_data(model, dataset_dir)
    print(result)
    exit(0)

print("Operation not supported")
exit(1)
