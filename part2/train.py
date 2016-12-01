import string
from collections import Counter
from collections import defaultdict
import os
import utils
import random
import copy


def read_classification(prob):
    rand_val = random.random()
    return rand_val < prob


def update_model(data, words, prev, cur):
    for word in words:
        if prev != "None":
            data[prev][word] -= 1
        data[cur][word] += 1
    return data


def update_topics(obj, prev, cur, count):
    if prev != "None":
        obj[prev] -= count
    obj[cur] += count
    return obj


def find_topic(model, words):
    if model.word_count == 0:
        topics = model.topics.keys()
        return random.choice(topics)
    return utils.find_topic(model, words)


def train_unclassified(unclassified, model):
    new_model = copy.deepcopy(model)
    count = 0
    for key in unclassified.keys():
        item = unclassified[key]
        words = item[0]
        prev_topic = item[1]
        new_topic = find_topic(model, words)
        if prev_topic != new_topic:
            count += 1
            if prev_topic == "None":
                for word in words:
                    new_model.word_counter[word] += 1

            new_model.data = update_model(new_model.data, words, prev_topic, new_topic)
            new_model.topics = update_topics(new_model.topics, prev_topic, new_topic, len(words))
            if prev_topic != "None":
                new_model.doc_topic_counter[prev_topic] -= 1
            new_model.doc_topic_counter[new_topic] += 1
            unclassified[key] = (words, new_topic)

    new_model.update_counts()

    return new_model, count


def random_name():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4))


def train_data(dataset_dir, fraction):
    unclassified = {}
    model = defaultdict(Counter)
    topics = Counter()
    word_counter = Counter()
    doc_topic_counter = Counter()
    for topic in os.listdir(dataset_dir):
        if topic.startswith('.'):
            continue
        topic_dir = dataset_dir + "/" + topic

        for cur_file in os.listdir(topic_dir):
            file_path = topic_dir + "/" + cur_file
            words = utils.get_file_content(file_path)
            if read_classification(fraction):
                topics[topic] += len(words)
                doc_topic_counter[topic] += 1
                for word in words:
                    model[topic][word] += 1
                    word_counter[word] += 1
            else:
                topics[topic] += 0
                doc_topic_counter[topic] += 0
                if cur_file not in unclassified:
                    unclassified[cur_file] = (words, 'None')
                else:
                    new_name = cur_file + random_name()
                    while new_name in unclassified:
                        print("Double duplicate found!")
                        new_name = cur_file + random_name()
                    unclassified[new_name] = (words, 'None')
    model_obj = utils.Train(model, topics, word_counter, doc_topic_counter)
    for i in range(24):
        print("Iteration %d" % i)
        model_obj, count_changed = train_unclassified(unclassified, model_obj)
        if count_changed == 0:
            break

    return model_obj
