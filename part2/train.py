from collections import Counter
from collections import defaultdict
import os
import utils
import email



def train_data(dataset_dir,fraction):
    model = defaultdict(Counter)
    topics = {}
    for topic in os.listdir(dataset_dir):
        if topic.startswith('.'):
            continue
        utils.topics.append(topic)
        topic_dir = dataset_dir+"/"+topic

        for file in os.listdir(topic_dir):
            file_path = topic_dir+"/"+file
            f_ptr = open(file_path,"r")
            email_obj = email.message_from_file(f_ptr)
            f_ptr.close()
            content = email_obj.get_payload()
            words = utils.sanitize_content(content)
            topics[topic] = len(words)
            for word in words:
                model[word][topic] += 1

    return utils.Train(model,topics)