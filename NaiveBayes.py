# @Author: mingxiangchen
# @Date:   2017-12-07T20:36:52-08:00
# @Email:  ming1993@stanford.edu
# @Last modified by:   mingxiangchen
# @Last modified time: 2017-12-07T20:46:54-08:00



import pickle

words = []
with open('data/glove.6B.100d.txt', 'r') as f:
    for line in f:
        words.append(line.split()[0])
print words[:5]

review_size = 0
with open('data/reviews_Books_5.json', 'r') as f:
    for line in f:
        review_size+=1
print review_size

word_appearance = {}
good_appearnce = {}

for word in words:
    word_appearance[word] = 0
    good_appearnce[word] = 0

line_index = 0
with open('data/reviews_Books_5.json', 'r') as f:
    for line in f:
        line_index+=1
        # training set: 100000:
        # test set: :100000
        if line_index<100000:
            continue
        # this is for testing
        # if line_index>150000:
        #     break
        if line_index%10000==0:
            print "Reviews #"+str(line_index-100000)+"/"+str(review_size-100000)
        if "reviewText" not in line or "overall" not in line:
            continue
        review_start = line.index("\"reviewText\":")+15
        review_end = line.index("\"overall\":")-3
        if review_end-review_start<50:
            continue
        review = line[review_start:review_end]
        overall = int(line[review_end+14:review_end+15])

        for i in xrange(len(review)):
            if not review[i].isalpha():
                review = review[:i]+" "+review[i:]
        review = review.split()
        for word in review:
            word_l = word.lower()
            if word_l in word_appearance:
                word_appearance[word_l]+=1
                if overall>3.5:
                    good_appearnce[word_l]+=1

weights = {}
for word in word_appearance:
    if (word_appearance[word] > 5):
        weights[word] = float(good_appearnce[word])/float(word_appearance[word])

with open('weights.pickle', 'wb') as handle:
    pickle.dump(weights, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('weights.pickle', 'rb') as handle:
    temp = pickle.load(handle)

print temp == weights
