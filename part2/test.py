import os
import email
import utils
import operator


def test_data(model,dataset_dir):
    doc_count = 0
    count_correct_classification = 0
    for topic in os.listdir(dataset_dir):

        if topic.startswith('.'):
            continue
        topic_dir = dataset_dir + "/" + topic

        for file in os.listdir(topic_dir):
            topic_prob = {}
            doc_count += 1
            file_path = topic_dir + "/" + file
            f_ptr = open(file_path, "r")
            email_obj = email.message_from_file(f_ptr)
            f_ptr.close()
            content = email_obj.get_payload()
            words = utils.sanitize_content(content)

            for cur_topic in model.topics.keys():
                prob = 0.0
                for word in words:
                    prob *= model.find_prob(word,cur_topic)
                prob *= model.find_topic_prob(cur_topic)
                topic_prob[cur_topic] = prob

            classified_topic = max(topic_prob, key=topic_prob.get)

            if classified_topic == topic:
                count_correct_classification += 1
    print("Number of documents read = %d" %doc_count)
    print("Number of true classification = %d" %count_correct_classification)



