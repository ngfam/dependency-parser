from TrainingHandler.distributor import sentences
from TrainingHandler.training import Parse
from TrainingHandler.extractor import extractor
from TrainingHandler.training import Trainer
from TrainingHandler.testing import Testing


a = Trainer()
ngram = a.process()

b = Testing(ngram)
b.process()

print(b.correct, b.total)
print(b.correct / b.total)
print(b.allCorrect, "/", b.countSentence)