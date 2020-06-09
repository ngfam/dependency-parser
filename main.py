from TrainingHandler.distributor import sentences
from TrainingHandler.training import Parse
from TrainingHandler.extractor import extractor
from TrainingHandler.training import Trainer
from TrainingHandler.testing import Testing
from sklearn.preprocessing import MinMaxScaler

# data = [[-1, 1], [-0.5, 2], [-3, 3]]

# scaler = MinMaxScaler()
# print(scaler.fit(data))
# print(scaler.transform(data))

a = Trainer()
ngram, weights = a.process()

b = Testing(ngram, weights)
b.process()

print(b.correct, b.total)
print(b.correct / b.total)
print(b.allCorrect, "/", b.countSentence)