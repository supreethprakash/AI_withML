from collections import Counter
from collections import defaultdict
import os
import utils
import email
import random


def read_classification(prob):
    rand_val = random.random()
    return rand_val < prob

#
#
# def get_rand_topic(lst):
#     return random.choice(lst)
#
#
# def find_topic(word, model, topics):
#     most_common_count = model[word].most_common(1)
#
#     if len(most_common_count) == 0:
#         topic = get_rand_topic(topics)
#     else:
#         topic = most_common_count[0][0]
#     return topic


def update_model(data, words, prev, cur):
    for word in words:
        if prev != "None":
            data[word][prev] -= 1
        data[word][cur] += 1
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
    count = 0
    temp = model.data
    temp_topics = model.topics
    for key in unclassified.keys():
        item = unclassified[key]
        words = item[0]
        prev_topic = item[1]
        new_topic = find_topic(model, words)
        if prev_topic != new_topic:
            count += 1
            print("Topic changed: %s -> %s" % (prev_topic, new_topic))
            temp = update_model(temp, words, prev_topic, new_topic)
            temp_topics = update_topics(temp_topics, prev_topic, new_topic, len(words))
            unclassified[key] = (words, new_topic)
    model.update_data(temp, temp_topics)

    return model, count


def train_data(dataset_dir, fraction):
    unclassified = {}
    model = defaultdict(Counter)
    topics = Counter()
    for topic in os.listdir(dataset_dir):
        if topic.startswith('.'):
            continue
        utils.topics.append(topic)
        topic_dir = dataset_dir + "/" + topic

        for cur_file in os.listdir(topic_dir):
            file_path = topic_dir + "/" + cur_file
            f_ptr = open(file_path, "r")
            email_obj = email.message_from_file(f_ptr)
            f_ptr.close()
            content = email_obj.get_payload()
            words = utils.sanitize_content(content)
            if read_classification(fraction):
                topics[topic] += len(words)
                for word in words:
                    model[word][topic] += 1
            else:
                topics[topic] += 0
                unclassified[cur_file] = (words, 'None')
    model_obj = utils.Train(model, topics)
    for i in range(24):
        model_obj, count_changed = train_unclassified(unclassified, model_obj)
        if count_changed == 0:
            break

    return model_obj
