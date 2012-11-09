from glob import glob
import mahotas
import mahotas.features
import milk
import numpy as np
from jug import TaskGenerator
import pickle

#@TaskGenerator
def features_for(imname):
    img = mahotas.imread(imname, as_grey=False)
    features = mahotas.features.haralick(img).mean(0)
    #features = mahotas.features.lbp(img, 1, 8)
    #features = mahotas.features.tas(img)
    #features =mahotas.features.zernike_moments(img, 2, degree=8)
    #print 'features:', features, len(features), type(features[0])
    return features
    #return 

#@TaskGenerator
def learn_model(features, labels):
    learner = milk.defaultclassifier()
    return learner.train(features, labels)

#@TaskGenerator
def classify(model, features):
     return model.apply(features)

positives = glob('/home/lforet/images/class1/*.jpg')
negatives = glob('/home/lforet/images/class2/*.jpg')
unlabeled = glob('../../images/*.jpg')

#print positives

features = map(features_for, negatives + positives)
labels = [0] * len(negatives) + [1] * len(positives)

model = learn_model(features, labels)
print type(features), labels
#pickle.dump( model, open( "ai_model.mdl", "wb" ) )
#model = pickle.load( open( "ai_model.mdl", "rb" ) )

#labeled = [classify(model, features_for(u)) for u in unlabeled]

for u in unlabeled:
	print "image: ", u, " = ", classify(model, features_for(u))
	

#print len(labeled)
#print labeled
