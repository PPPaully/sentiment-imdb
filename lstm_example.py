n_word = 50 <- See lstm example pic
n_vec = 300
n_unit = 32
n_hidden = 64
n_class = 30

INPUT = T.fmatrix() <- 2D-array = numpy.ndarray shape likes (n_word, n_vec)
CELL = T.fmatrix() <- shape likes (n_unit, n_vec)
HIDDEN = T.fmatrix() <- shape likes (n_unit, n_vec)


lstm_wxi = init_weights((n_unit, n_vec, n_vec)) <- 3D-array with (n_unit,n_vec,n_vec). Those will come from pretrained-weight
lstm_wxf = init_weights((n_unit, n_vec, n_vec))
lstm_wxc = init_weights((n_unit, n_vec, n_vec))
lstm_wxo = init_weights((n_unit, n_vec, n_vec))

lstm_whi = init_weights((n_unit, n_vec, n_vec))
lstm_whf = init_weights((n_unit, n_vec, n_vec))
lstm_whc = init_weights((n_unit, n_vec, n_vec))
lstm_who = init_weights((n_unit, n_vec, n_vec))

lstm_wci = init_weights((n_unit, n_vec, n_vec))
lstm_wcf = init_weights((n_unit, n_vec, n_vec))
lstm_wco = init_weights((n_unit, n_vec, n_vec))


def lstm(x_t, c_tm1, h_tm1):
    x_t_repeat = T.repeat(x_t, n_unit, axis=0)
    i_t = T.nnet.sigmoid(T.batched_dot(x_t_repeat, lstm_wxi) + T.batched_dot(h_tm1, lstm_whi) + T.batched_dot(c_tm1, lstm_wci))
    f_t = T.nnet.sigmoid(T.batched_dot(x_t_repeat, lstm_wxf) + T.batched_dot(h_tm1, lstm_whf) + T.batched_dot(c_tm1, lstm_wcf))
    c_t = T.mul(f_t, c_tm1) + i_t*T.tanh(T.batched_dot(x_t_repeat, lstm_wxc) + T.batched_dot(h_tm1, lstm_whc))
    o_t = T.nnet.sigmoid(T.batched_dot(x_t_repeat, lstm_wxo) + T.batched_dot(h_tm1, lstm_who) + T.batched_dot(c_t, lstm_wco))
    h_t = o_t*T.tanh(c_t)
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

lstm_layer = ...
# for loop in INPUT:
#   do lstm(input_one_word, CELL, HIDDEN)
#   with input_one_word = INPUT[i] shape likes (1, 1-word, n_vec) - see numpy.reshape
#   with initial CELL and HIDDEN by numpy.zeros() and use its as "old state" for next loop
# OUTPUT - lstm_layer = each HIDDEN state [HIDDEN at 1, HIDDEN at 2, HIDDEN at 3, ..., HIDDEN at n_word]
#    so output's shape must be (n_word, n_unit, n_vec)

lstm_output = T.flatten(lstm_layer, 2) <- 2 mean 2-dims
# see numpy.flatten
# make sure that lstm_output's shape must be (n_word, n_unit * n_vec)

model_fw = init_weights((n_unit * n_vec, n_class))
model_output = T.nnet.sigmoid(T.dot(lstm_output, model_fw))
# Just dot = fully connected NN