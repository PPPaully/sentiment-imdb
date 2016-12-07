import json
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize


class Model:
    def __init__(self):
        self.lstm_wxi = np.load('./model/lstm_wxi.npy')
        self.lstm_wxf = np.load('./model/lstm_wxf.npy')
        self.lstm_wxc = np.load('./model/lstm_wxc.npy')
        self.lstm_wxo = np.load('./model/lstm_wxo.npy')

        self.lstm_whi = np.load('./model/lstm_whi.npy')
        self.lstm_whf = np.load('./model/lstm_whf.npy')
        self.lstm_whc = np.load('./model/lstm_whc.npy')
        self.lstm_who = np.load('./model/lstm_who.npy')

        self.lstm_wci = np.load('./model/lstm_wci.npy')
        self.lstm_wcf = np.load('./model/lstm_wcf.npy')
        self.lstm_wco = np.load('./model/lstm_wco.npy')

        self.n_unit = self.lstm_wxi.shape[0]
        self.n_vec = self.lstm_wxi.shape[1]

        self.class_name = [c for c in np.load('./model/imdb_class.npy') if c.startswith('genre_')]
        self.n_class = len(self.class_name)
        self.fully_weight = np.load('./model/lstm_fw.npy')

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def batched_dot(a, b):
        out = []
        for i in range(a.shape[0]):
            out.append(np.dot(a[i], b[i]))
        return np.asarray(out)

    def lstm(self, x_t, c_tm1, h_tm1):
        x_t_repeat = np.repeat(x_t, self.n_unit, axis=0)
        i_t = Model.sigmoid(Model.batched_dot(x_t_repeat, self.lstm_wxi) + Model.batched_dot(h_tm1, self.lstm_whi) + Model.batched_dot(c_tm1, self.lstm_wci))
        f_t = Model.sigmoid(Model.batched_dot(x_t_repeat, self.lstm_wxf) + Model.batched_dot(h_tm1, self.lstm_whf) + Model.batched_dot(c_tm1, self.lstm_wcf))
        c_t = f_t * c_tm1 + i_t * np.tanh(Model.batched_dot(x_t_repeat, self.lstm_wxc) + Model.batched_dot(h_tm1, self.lstm_whc))
        o_t = Model.sigmoid(Model.batched_dot(x_t_repeat, self.lstm_wxo) + Model.batched_dot(h_tm1, self.lstm_who) + Model.batched_dot(c_t, self.lstm_wco))
        h_t = o_t * np.tanh(c_t)
        return c_t, h_t

    def run(self, vecs):
        cell_state = np.zeros((self.n_unit, 1, self.n_vec))
        hidden_state = np.zeros((self.n_unit, 1, self.n_vec))
        for vector in vecs:
            cell_new, hidden_new = self.lstm(vector.reshape(1, 1, -1), cell_state, hidden_state)
            lstm_output = np.concatenate(hidden_new, axis=1)
            cell_state, hidden_state = cell_new, hidden_new
        model_output = self.sigmoid(np.dot(lstm_output, self.fully_weight))
        return model_output.tolist()

    def predict(self, storyline):
        sentiment = []
        for sentence in sent_tokenize(storyline.lower()):
            words = word_tokenize(sentence)
            vecs = np.asarray([word2vec[word].copy() for word in words if word in word2vec])

            if len(vecs) > 0:
                predict = self.run(vecs)

            sentiment.append({
                'sentence': sentence,
                'valid': len(vecs) > 0,
                'predict': predict if len(vecs) > 0 else np.zeros(self.n_class)
            })

        words = word_tokenize(storyline.lower())
        vecs = np.asarray([word2vec[word].copy() for word in words if word in word2vec])
        overall = self.run(vecs) if len(vecs) > 0 else np.zeros(self.n_class)

        return {
            'class': model.class_name,
            'sentiment': sentiment,
            'overall': overall
        }


word2vec = np.load('./model/imdb_word2vec.npy').item()

plot = "I love you. Do you love me? No, we should be friend."
model = Model()
output = model.predict(plot)
print json.dumps(output)
