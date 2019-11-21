import tweepy
import os
import numpy


def make_pairs(_corpus):
    for _i in range(len(_corpus) - 1):
        yield (_corpus[_i], _corpus[_i + 1])


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    _last_seen_id = int(f_read.read().strip())
    f_read.close()
    return _last_seen_id


def store_last_seen_id(_last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(_last_seen_id))
    f_write.close()
    return


auth = tweepy.OAuthHandler("2rv8quSAGzIWFrnJYQHVWpjjE", "Nl95hApe0FcovNkpjoZLjT5pMzoQiwglMGeHarDtaoSLXduxvd")
auth.set_access_token("1196697448648830976-Kc5zhNuUcHi5OA76OCJvhlB8GKDqUW", "t69KFABoyjjOAHClG4JzUB92vAlPEFmMh5B4kHQ1HSiwW")
api = tweepy.API(auth)

dwight = open('dwightquotes.txt', encoding='utf8').read()
corpus = dwight.split()
pairs = make_pairs(corpus)
word_dict = {}
first_words_list = []

for word_1, word_2 in pairs:
    if word_1 in word_dict.keys():
        word_dict[word_1].append(word_2)
    else:
        word_dict[word_1] = [word_2]

for i in word_dict:
    if i in word_dict.keys() and "." in i:
        for j in word_dict[i]:
            first_words_list.append(j)

first_word = numpy.random.choice(first_words_list)
chain = [first_word]
n_sentences = numpy.random.randint(2, 4)
current_num_sentences = 0
result = ""


while current_num_sentences in range(n_sentences):
    chain.append(numpy.random.choice(word_dict[chain[-1]]))
    if "." in chain[len(chain) - 1]:
        current_num_sentences += 1


for i in range(len(chain)):
    result += chain[i] + " "

if os.stat('last_seen_id.txt').st_size != 0:
    last_seen_id = retrieve_last_seen_id('last_seen_id.txt')
    mentions = api.mentions_timeline(last_seen_id)
else:
    mentions = api.mentions_timeline()

for mention in reversed(mentions):
    store_last_seen_id(mention.id, 'last_seen_id.txt')
    if "#dwigtschrudequote" in mention.text.lower():
        print("found #")
        api.update_status('@' + mention.user.screen_name + ' ' + result, mention.id)
    else:
        print('didnt contain #')
