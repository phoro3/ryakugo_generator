#coding:utf-8
import os
from tensorflow.models.rnn import rnn_cell
from tensorflow.models.rnn import rnn
import tensorflow as tf
from utils import make_input_vec_list, make_label_list, read_file

def inference(v_size, num_classes, inputs):
    lstm = rnn_cell.BasicLSTMCell(v_size)
    state = tf.zeros([1, lstm.state_size])
    w_ho = tf.get_variable("w_ho", [v_size, num_classes], initializer = tf.random_normal_initializer())

    h_outputs, states = rnn.rnn(lstm, inputs, dtype = tf.float32)

    outputs = []
    for h_output in h_outputs:
        output = tf.nn.softmax(tf.matmul(h_output, w_ho))
        outputs.append(output)

    return outputs


def calc_loss(outputs, labels):
    loss = tf.Variable(tf.zeros([1]))
    for i in range(len(outputs)):
        loss += -tf.reduce_sum(labels[:, i, :] * tf.log(outputs[i]))

    return loss


def train(loss):
    train_step = tf.train.AdamOptimizer().minimize(loss)
    return train_step


def accuracy(outputs, labels):
    accuracy = tf.Variable(tf.zeros([1]))
    for i in range(len(outputs)):
        correct_prediction = tf.equal(tf.argmax(outputs[i], 1), tf.argmax(labels[:, i, :], 1))
        accuracy = tf.add(accuracy, tf.reduce_mean(tf.cast(correct_prediction, tf.float32)))

    accuracy = tf.div(accuracy, tf.constant(len(outputs), dtype=tf.float32))
    return accuracy


if __name__ == "__main__":
    str_list, answer_list = read_file("dict.txt")
    max_num_step = max(map(len, str_list))

    inputs_list = convert_to_vector(str_list, max_num_step)
    #inputs_list = make_input_vec_list(str_list, max_num_step)
    label_list = make_label_list(str_list, answer_list, max_num_step)
    num_classes = len(label_list[0][0])
    v_size = len(inputs_list[0][0])

    inputs = tf.placeholder(tf.float32, shape = [None, max_num_step, v_size])
    labels = tf.placeholder(tf.float32, shape = [None, max_num_step, num_classes])
    input_tensor_list = []
    for i in range(max_num_step):
        input_tensor_list.append(inputs[:, i, :])
    with tf.variable_scope("lstm") as scope:
        outputs = inference(v_size, num_classes, input_tensor_list)
    loss = calc_loss(outputs, labels)
    train_step = train(loss)
    accuracy = accuracy(outputs, labels)

    saver = tf.train.Saver()
    sess = tf.Session()

    if os.path.isfile("lstm_model"):
        print "Load model"
        saver.restore(sess, "lstm_model")
    else:
        sess.run(tf.initialize_all_variables())

    for k in range(100):
        if k % 50 == 0:
            print "Step:" + str(k)
        sess.run(train_step, {inputs:inputs_list, labels:label_list})
