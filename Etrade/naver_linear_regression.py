'''
A linear regression learning algorithm example using TensorFlow library.

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import print_function

import tensorflow as tf
import numpy
import matplotlib.pyplot as plt
import re
import random
rng = numpy.random

# data structure
FORIGN_IDX = 1
UPDOWN_IDX = 4

# number of using privous data
CHK_DATE_SIZE = 8

# Parameters
learning_rate = 0.01
training_epochs = 500
display_step = 50

# Training Data
f = open("forigndata.txt", 'r')
line = f.readline()
line.replace(",", "")
print(line)
line.replace("%%", "")
print(line)
d1 = line.split()
forign_buy = float(d1[FORIGN_IDX].replace(",","")) / 1000
updown_ratio = float(d1[UPDOWN_IDX].replace("%",""))

print("forign is ", forign_buy)
print("up down is ", updown_ratio)

while True:
    line = f.readline()
    if not line: break
    d1 = line.split()
    forign_buy = numpy.insert(forign_buy, 0, float(d1[FORIGN_IDX].replace(",","") )/1000)
    updown_ratio = numpy.insert(updown_ratio, 0,  float(d1[UPDOWN_IDX].replace("%","")))


'''train_X = numpy.asarray([[3.3,3.3], [4.4,4,4] ,[5.5,5.5], [6.71, 6],[6.93,6,9],
                         [4.168,4.1], [9.779,9.7], [6.182,6], [7.59,7.5], [2.167,2.1],
                         7.042,10.791,5.313,7.997,5.654,9.27,3.1])'''
'''
train_X_b = numpy.asarray([3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167,
                         7.042,10.791,5.313,7.997,5.654,9.27,3.1])
train_X = numpy.array([[3.3, 3]])
for a in train_X_b:
    train_X = numpy.append(train_X, [[a, a]], axis = 0)

train_Y = numpy.asarray([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221,
                         2.827,3.465,1.65,2.904,2.42,2.94,1.3])
n_samples = train_Y.shape[0]
'''

n_samples = forign_buy.shape[0] - CHK_DATE_SIZE -1

def get_arryed_data(input, start, size):
    res = []
    for a in range(0, CHK_DATE_SIZE):
        res = numpy.append(res, [input[start + a]], axis=0)

    res = [res]
    for i in range(1, size - 1):
        sub1 = []
        for a in range(0, CHK_DATE_SIZE):
            sub1 = numpy.append(sub1, [input[start + i + a]], axis=0)
        #print(sub1)
        res = numpy.append(res, numpy.array([sub1]), axis=0)

    return res

TRAINING_SIZE = int(n_samples * 0.75)
TESTING_SIZE = n_samples - TRAINING_SIZE + CHK_DATE_SIZE
train_X = get_arryed_data(forign_buy, 0,  TRAINING_SIZE)
#del forign_buy[0:TRAINING_SIZE]
test_X = get_arryed_data(forign_buy, TRAINING_SIZE - CHK_DATE_SIZE,  TESTING_SIZE)

updown_ratio = updown_ratio[CHK_DATE_SIZE:]
#updown_ratio = numpy.delete(updown_ratio, CHK_DATE_SIZE, axis = 0)
train_Y = updown_ratio[0:TRAINING_SIZE]
#del updown_ratio[0:TRAINING_SIZE]
test_Y = updown_ratio[TRAINING_SIZE - CHK_DATE_SIZE:]

# '''
print(train_X)
print(train_Y)
print(test_X)
print(test_Y)
# exit()
# '''
#train_X = numpy.array([[]])
'''
train_X = []
for a in range(0, CHK_DATE_SIZE):
    train_X = numpy.append(train_X, [forign_buy[a]], axis=0)

train_X = [train_X]
print(train_X)
# print (train_X.shape)
# train_X = [[ forign_buy[0], forign_buy[1], forign_buy[2], forign_buy[3] ]]
for i in range( 1,n_samples-1):
    sub1 = []
    for a in range(0, CHK_DATE_SIZE):
        sub1 = numpy.append(sub1,  [forign_buy[i+a]], axis = 0)
    # sub1 = [[ forign_buy[i], forign_buy[i+1], forign_buy[i+2], forign_buy[i+3] ]]
    print(sub1)
    train_X = numpy.append(train_X, numpy.array([sub1]), axis = 0 )

train_Y = numpy.delete(updown_ratio, 0, axis = 0)
print(train_X)
print(train_Y)
exit()
'''
# tf Graph Input
X = tf.placeholder("float64")
Y = tf.placeholder("float64")

# Set model weights
#W = tf.Variable(tf.zeros([ CHK_DATE_SIZE, 1], dtype=tf.float64), name = "weight", dtype = tf.float64)

W = tf.Variable(numpy.ones((CHK_DATE_SIZE, 1)), name="weight",  dtype=tf.float64)
# W = tf.Variable([[rng.randn()],[rng.randn()], [rng.randn()], [rng.randn()]], name="weight",  dtype=tf.float64)
#W = tf.Variable([[rng.randn()],[rng.randn()]], name="weight",  dtype=tf.float64)

b = tf.Variable(rng.randn(), name="bias", dtype = tf.float64)

# Construct a linear model
pred = tf.add(tf.matmul(X, W), b)
#pred = tf.add(tf.multiply(X, W), b)

# Mean squared error
cost = tf.reduce_sum(tf.pow(pred-Y, 2))/(2* TRAINING_SIZE) #n_samples)
# Gradient descent
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# Initializing the variables
init = tf.global_variables_initializer()


# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    # Fit all training data
    for epoch in range(training_epochs):
        avg_cost = 0

        for (x, y) in zip(train_X, train_Y):
            # {X: x, Y:y} cause crash
            # print({X:[x], Y:y})
            _, c = sess.run([optimizer, cost], feed_dict={X: [x], Y: y})
            # sess.run(optimizer, feed_dict={X: [x], Y: y})
            avg_cost += c / n_samples

        # Display logs per epoch step
        if (epoch+1) % display_step == 0:
            # c = sess.run(cost, feed_dict={X: train_X, Y:train_Y})
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost), \
                "W=", sess.run(W), "b=", sess.run(b))
            #print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(c), \
            #    "W=", sess.run(W), "b=", sess.run(b))

# testing
    print("start testing")
    predicted = []

    money = 1000
    depot_only = money
    random_result = money
    owned = 0
    owned_rand = 0
    for i in range(TESTING_SIZE -1):
        x = test_X[i:i+1,]
        y = test_Y[i]
        # print(x)
        # print(y)
        res = sess.run(pred, feed_dict={X: x, Y: y})
        updown_pred = res[0][0]
        if (updown_pred > 0.5) and (0 == owned):
            owned = money
            money -= money * 0.0033 # charge and tax

        elif (updown_pred < -0.5) and ( 0 != owned):
            owned = 0
            money -= money * 0.0033 # charge and tax

        if 0 != owned :
            money *= (1 + y /100)

        depot_only *= (1 + y / 100)

        ranv = random.random()
        if (ranv > 0.5) and (0 == owned_rand):
            owned_rand = random_result
            random_result -= random_result * 0.0033
        elif (ranv <= 0.5) and (0 != owned_rand):
            owned_rand = 0;
            random_result -= random_result * 0.0033

        if 0 != owned_rand:
            random_result *= ( 1 + y/100)

        predicted.append(updown_pred)
        # _, c = sess.run([optimizer, cost], feed_dict={X: x, Y: y})
        print("Pred: ", updown_pred, ", actual: ", y,
              ", money: ", money, ", depot: ", depot_only, ", rand: ", ranv, ", rand res: ", random_result)

    day = [xx for xx in range(TESTING_SIZE -1)]

    print(day)
    print(predicted)

    # Graphic display
    plt.plot(day, test_Y[:TESTING_SIZE-1], 'ro', label='Original data')
    plt.plot(day, predicted, 'bo', label='predicted data')

    #plt.plot(day, sess.run(W) * train_X + sess.run(b), label='Fitted line')
    plt.legend()
    plt.show()



'''
    c = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
    print("Epoch:", '%04d' % (0 ), "cost=", "{:.9f}".format(c), \
          "W=", sess.run(W), "b=", sess.run(b))

#    c = sess.run([optimizer, cost], feed_dict={X: train_X, Y: train_Y})
#    print(c)

#    result = sess.run(pred, feed_dict={X: train_X})
#    cos = sess.run(cost, feed_dict={X: train_X, Y:train_Y})
#    print(cos)
#    print(result)
#    exit()
#

    # Fit all training data
    for epoch in range(training_epochs):
        for (x, y) in zip(train_X, train_Y):
            # {X: x, Y:y} cause crash
            sess.run(optimizer, feed_dict={X: [x], Y: y})

        # Display logs per epoch step
        if (epoch+1) % display_step == 0:
            c = sess.run(cost, feed_dict={X: train_X, Y:train_Y})
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(c), \
                "W=", sess.run(W), "b=", sess.run(b))

    print("Optimization Finished!")
    training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
    print("Training cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n')

    # Graphic display
    plt.plot(train_X, train_Y, 'ro', label='Original data')
    plt.plot(train_X, sess.run(W) * train_X + sess.run(b), label='Fitted line')
    plt.legend()
    plt.show()

    # Testing example, as requested (Issue #2)

    test_X_b = numpy.asarray([6.83, 4.668, 8.9, 7.91, 5.7, 8.7, 3.1, 2.1])
    test_X = numpy.array([[3.3, 3]])
    for a in test_X_b:
        test_X = numpy.append(test_X, [[a, a]], axis=0)

    test_Y = numpy.asarray([1.84, 2.273, 3.2, 2.831, 2.92, 3.24, 1.35, 1.03])

    print("Testing... (Mean square loss Comparison)")
    testing_cost = sess.run(
        tf.reduce_sum(tf.pow(pred - Y, 2)) / (2 * test_X.shape[0]),
        feed_dict={X: test_X, Y: test_Y})  # same function as cost above
    print("Testing cost=", testing_cost)
    print("Absolute mean square loss difference:", abs(
        training_cost - testing_cost))

    plt.plot(test_X, test_Y, 'bo', label='Testing data')
    plt.plot(train_X, sess.run(W) * train_X + sess.run(b), label='Fitted line')
    plt.legend()
    plt.show()

'''
