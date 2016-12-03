n_epoch = 100 => #words in input
n_word = 50
n_vec = 300
n_unit = 32
n_hidden = 64
n_class = 30

INPUT = T.tensor3() <- 3D-array = numpy.ndarray
CELL = T.tensor3()
HIDDEN = T.tensor3()


lstm_wxi = init_weights((n_unit, n_vec, n_vec)) <- 3D-array with (n_unit,n_vec,n_vec) those will come from trained-weight
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

lstm_output = ...
# for loop:
#   do lstm(input, cell_state, hidden_state) from input[at 0 until end]
#   with initial cell_state and hidden_state [0, 0, ...] and use its as "old state" for next loop

model_fw = init_weights((n_unit * n_vec, n_class))
model_output = T.nnet.sigmoid(T.dot(lstm_output, model_fw))

# Just dot = fully connected NN