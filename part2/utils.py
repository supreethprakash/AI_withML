import string


class Train:

    def __init__(self,data,topics):
        self.data = data
        self.topics = topics
        self.word_count = len(data)

    def find_prob(self,word,topic):
        if self.data[word][topic] == 0:
            return 0.000000001
        return float(self.data[word][topic])/sum(self.data[word].values())

    def find_topic_prob(self,topic):
        return float(self.topics[topic]/self.word_count)

stopWords = ['a','about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'arent', 'as',
			 'at', 'because', 'be', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'cant', 'cannot',
			 'couldnt', 'did', 'didnt', 'do', 'does','doesnt', 'doing', 'dont', 'down', 'during', 'each', 'few', 'for', 'from',
			 'further', 'had', 'hadnt', 'has', 'hasnt', 'have', 'havent', 'having', 'he', 'hed','hell','hes', 'her', 'hers', 'here',
			 'heres', 'herself', 'him', 'himself', 'his', 'how', 'hows', 'i', 'id', 'ill', 'im', 'ive', 'if', 'in', 'into', 'is', 'isnt',
			 'it', 'its', 'itself', 'lets', 'more', 'me', 'most', 'mustnt', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once',
			 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shant', 'she', 'shell','shed', 'shes',
			 'should', 'shouldnt', 'so', 'some', 'such', 'than', 'that', 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then',
			 'there', 'theres', 'they', 'theyd', 'theyll','theyre', 'theyve', 'this', 'those', 'though', 'through', 'to', 'too', 'under',
			 'until', 'up', 'very', 'was', 'wasnt', 'we', 'wed', 'well', 'were', 'weve', 'werent', 'what', 'whats', 'when', 'whens', 'where',
			 'wheres', 'which', 'while', 'who', 'whos', 'whom', 'why', 'whys', 'with', 'wont', 'would', 'wouldnt', 'you', 'youd', 'youll',
			 'youre', 'youve', 'your', 'yours', 'yourself', 'yourselves', 'font', 'html', 'table', 'br', 'will']


def translate_content(content,trans_table):
    return content.translate(trans_table)

def sanitize_content(content):
    content = content.lower()
    trans_table = content.maketrans(string.punctuation," " * len(string.punctuation))
    content = translate_content(content,trans_table)
    trans_table = content.maketrans(string.digits," "* len(string.digits))
    content = translate_content(content, trans_table)
    sanitized_content = [word for word in content.split() if word not in stopWords and len(word) > 1]
    return sanitized_content

specialCharacters = ['\n','\t', ' ', '\r', ',', '']

topics = []