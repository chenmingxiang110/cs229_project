# @Author: mingxiangchen
# @Date:   2017-11-19T01:47:00-08:00
# @Email:  ming1993@stanford.edu
# @Last modified by:   mingxiangchen
# @Last modified time: 2017-11-19T02:50:55-08:00



import numpy as np
import random

word_vectors = {}

glove_size = 0
with open('data/glove.6B.100d.txt', 'r') as f:
    for line in f:
        glove_size+=1
print glove_size

review_size = 0
with open('data/reviews_Books_5.json', 'r') as f:
    for line in f:
        review_size+=1
print review_size

line_index = 0
with open('data/glove.6B.100d.txt', 'r') as f:
    for line in f:
        line_index+=1
        if line_index%100000==0:
            print "Reading word_vectors... "+str(line_index)+"/"+str(glove_size)
        line_list = line.split()
        word = line_list[0]
        vec = [float(v) for v in line_list[1:]]
        assert len(vec) == 100
        word_vectors[word] = vec

print len(word_vectors)

x_data_all = []
y_data_all = []
y_onehot_all = []
x_data = []
y_data = []

padding_vec = np.zeros(100)

line_index = 0
with open('data/reviews_Books_5.json', 'r') as f:
    for line in f:
        line_index+=1
        if line_index%10000==0:
            x_data = np.array(x_data)
            y_data = np.array(y_data)
            y_onehot = np.zeros((len(y_data), 5))
            y_onehot[np.arange(len(y_data)), y_data-1] = 1
            y_stats = np.sum(y_onehot, axis = 0)
            print y_stats
            num_in_class = min(y_stats)
            nums = [0,0,0,0,0]
            for i in xrange(len(y_data)):
                index = y_data[i]-1
                if nums[index]<num_in_class:
                    nums[index] += 1
                    x_data_all.append(x_data[i])
                    y_data_all.append(y_data[i])
                    y_onehot_all.append(y_onehot[i])
            x_data = []
            y_data = []
            y_onehot = []
            print "Valid reviews: "+str(len(y_data_all))
        if len(y_data_all)>=100000:break
        if "reviewText" not in line or "overall" not in line:
            continue
        review_start = line.index("\"reviewText\":")+15
        review_end = line.index("\"overall\":")-3
        if review_end-review_start<50:
            continue
        review = line[review_start:review_end]
        overall = line[review_end+14:review_end+15]

        for i in xrange(len(review)):
            if not review[i].isalpha():
                review = review[:i]+" "+review[i:]
        review = review.split()

        word_sequence = []
        for i in xrange(50):
            if i>=len(review):
                word_vec = padding_vec
            else:
                word = review[i].lower()
                if word in word_vectors:
                    word_vec = np.array(word_vectors[word])
                else:
                    word_vec = np.random.rand(100)
            word_sequence.append(word_vec)
        x_data.append(word_sequence)
        overall = int(overall)
        y_data.append(overall)

x_data_all = np.array(x_data_all)
y_data_all = np.array(y_data_all)
y_onehot_all = np.array(y_onehot_all)
y_stats = np.sum(y_onehot_all, axis = 0)
print y_stats

print x_data_all.shape
print y_data_all.shape
print y_onehot_all.shape

np.save("x_data_lstm", x_data_all)
np.save("y_data_lstm", y_data_all)
np.save("y_onehot_lstm", y_onehot_all)
