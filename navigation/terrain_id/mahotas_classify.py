from glob import glob
import mahotas
import mahotas.features
import milk
from jug import TaskGenerator


#@TaskGenerator
def features_for(imname):
    img = mahotas.imread(imname)
    return mahotas.features.haralick(img).mean(0)

#@TaskGenerator
def learn_model(features, labels):
    learner = milk.defaultclassifier()
    return learner.train(features, labels)

#@TaskGenerator
def classify(model, features):
     return model.apply(features)

positives = glob('../../../images/class1/*.jpg')
negatives = glob('../../../images/class2/*.jpg')
unlabeled = glob('../images/*.jpg')


features = map(features_for, negatives + positives)
labels = [0] * len(negatives) + [1] * len(positives)

model = learn_model(features, labels)
#print features, labels

#labeled = [classify(model, features_for(u)) for u in unlabeled]

for u in unlabeled:
	print "image: ", u, " = ", classify(model, features_for(u))
	

#print len(labeled)
#print labeled
