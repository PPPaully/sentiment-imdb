# coding=utf-8
n_word = 50   #<- See lstm example pic
n_vec = 300
n_unit = 32
n_hidden = 64
n_class = 30
import numpy as np
#INPUT = np.ndarray(n_word, n_vec) #T.fmatrix() <- 2D-array = numpy.ndarray shape likes (n_word, n_vec)
#CELL = np.ndarray(n_unit, n_vec) #T.fmatrix() #<- shape likes (n_unit, n_vec)
#HIDDEN = np.ndarray(n_unit, n_vec) #T.fmatrix() #<- shape likes (n_unit, n_vec)
lstm_wxi = np.random.rand(n_unit,n_vec,n_vec)   #init_weights((n_unit, n_vec, n_vec)) <- 3D-array with (n_unit,n_vec,n_vec). Those will come from pretrained-weight
lstm_wxf = np.random.rand(n_unit,n_vec,n_vec)   #init_weights((n_unit, n_vec, n_vec))
lstm_wxc = np.random.rand(n_unit,n_vec,n_vec)   #init_weights((n_unit, n_vec, n_vec))
lstm_wxo = np.random.rand(n_unit,n_vec,n_vec)   #init_weights((n_unit, n_vec, n_vec))

lstm_whi = np.random.rand(n_unit,n_vec,n_vec)#init_weights((n_unit, n_vec, n_vec))
lstm_whf = np.random.rand(n_unit,n_vec,n_vec)#init_weights((n_unit, n_vec, n_vec))
lstm_whc = np.random.rand(n_unit,n_vec,n_vec) #init_weights((n_unit, n_vec, n_vec))
lstm_who = np.random.rand(n_unit,n_vec,n_vec)#init_weights((n_unit, n_vec, n_vec))

lstm_wci = np.random.rand(n_unit,n_vec,n_vec)#init_weights((n_unit, n_vec, n_vec))
lstm_wcf = np.random.rand(n_unit,n_vec,n_vec) #init_weights((n_unit, n_vec, n_vec))
lstm_wco = np.random.rand(n_unit,n_vec,n_vec)  #init_weights((n_unit, n_vec, n_vec))

def sigmoid(x):
    return 1/(1+pow(2.7182818284590452353602874713527,-x))

def batched_dot(a,b):
    out = np.zero(len(a),len(a[1]),len(b[1][1]))
    for i in range(len(a)):
        out[i] = np.dot(a[i],b[i])
    return out

def lstm(x_t, c_tm1, h_tm1):
    x_t_repeat = np.repeat(x_t, n_unit, axis=0)
    i_t = sigmoid(batched_dot(x_t_repeat, lstm_wxi) + batched_dot(h_tm1, lstm_whi) + batched_dot(c_tm1, lstm_wci))
    f_t = sigmoid(batched_dot(x_t_repeat, lstm_wxf) + batched_dot(h_tm1, lstm_whf) + batched_dot(c_tm1, lstm_wcf))
    c_t = np.dot(f_t, c_tm1) + i_t*np.tanh(batched_dot(x_t_repeat, lstm_wxc) + batched_dot(h_tm1, lstm_whc))
    o_t = sigmoid(batched_dot(x_t_repeat, lstm_wxo) + batched_dot(h_tm1, lstm_who) + batched_dot(c_t, lstm_wco))
    h_t = o_t*np.tanh(c_t)
    return c_t, h_t

# funtion:
#   T.repeat likes numpy.repeat (repeat ND-Array at axis-0 from (a,b,c) to (a*n_unit),b,c)
#   T.sigmoid - sigmoid function have to declare by yourself
#   T.batched_dot(A,B):
#     A – 3D (dim1, dim3, dim2)
#     B – 3D (dim1, dim2, dim4)
#     OUTPUT - 3D (dim1, dim3, dim4)
#        for loop at (dim1) do dot-product (dim3,dim2) dot (dim2,dim4) = (dim3,dim4) USE DOT-PRODUCT FROM numpy.dot
#   T.mul - Hadamard product A*B at ij = Aij*Bij
#   T.tanh - Hyper-tangent function

#####lstm_layer = ...
# for loop in INPUT:
#   do lstm(input_one_word, CELL, HIDDEN)
#   with input_one_word = INPUT[i] shape likes (1, 1-word, n_vec) - see numpy.reshape
#   with initial CELL and HIDDEN by numpy.zeros() and use its as "old state" for next loop
# OUTPUT - lstm_layer = each HIDDEN state [HIDDEN at 1, HIDDEN at 2, HIDDEN at 3, ..., HIDDEN at n_word]
#    so output's shape must be (n_word, n_unit, n_vec)

#####lstm_output = T.flatten(lstm_layer, 2) <- 2 mean 2-dims
# see numpy.flatten
# make sure that lstm_output's shape must be (n_word, n_unit * n_vec)

#model_fw = init_weights((n_unit * n_vec, n_class))
#model_output = T.nnet.sigmoid(T.dot(lstm_output, model_fw))
# Just dot = fully connected NN