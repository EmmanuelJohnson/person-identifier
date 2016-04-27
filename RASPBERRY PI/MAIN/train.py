import fnmatch
import os
import cv2
import numpy as np
import config
import face
import json
from pprint import pprint

MEAN_FILE = 'mean.png'

def walk_files(directory, match='*'):
	"""Generator function to iterate through all files in a directory recursively
	which match the given filename match parameter.
	"""
	for root, dirs, files in os.walk(directory):
		for filename in fnmatch.filter(files, match):
			yield os.path.join(root, filename)


def walk_folders(directory):
	for root, dirs, files in os.walk(directory):
		for foldername in dirs:
			yield os.path.join(root, foldername)

def prepare_image(filename):
	"""Read an image as grayscale and resize it to the appropriate size for
	training the face recognition model.
	"""
	return face.resize(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

def normalize(X, low, high, dtype=None):
	"""Normalizes a given array in X to a value between low and high.
	"""
	X = np.asarray(X)
	minX, maxX = np.min(X), np.max(X)
	# normalize to [0...1].
	X = X - float(minX)
	X = X / float((maxX - minX))
	# scale to [low...high].
	X = X * (high-low)
	X = X + low
	if dtype is None:
		return np.asarray(X)
	return np.asarray(X, dtype=dtype)

if __name__ == '__main__':
	print "Reading training images..."
	faces = []
	labels = []
	count = 0
	with open('training/info.json') as data_file:    
    		data = json.load(data_file)
	data_file.close()
	dic = len(data)
	dic = 0
	for foldername in walk_folders('./training'):
	# Read all images
		fdir = foldername
		with open('training/info.json') as data_file:    
    			data = json.load(data_file)
		data_file.close()
		lno = data[dic]['infoid']
		dic += 1
		print lno
		print fdir
		for filename in walk_files(fdir, '*.pgm'):
			faces.append(prepare_image(filename))
			labels.append(lno)
			count += 1
	print 'Read all the images.'
	# Train model
	print 'Training model...'
	model = cv2.createEigenFaceRecognizer()
	model.train(np.asarray(faces), np.asarray(labels))
	# Save model results
	model.save(config.TRAINING_FILE)
	print 'Training data saved to', config.TRAINING_FILE

	# Save mean and eignface images which summarize the face recognition model.
	mean = model.getMat("mean").reshape(faces[0].shape)
	cv2.imwrite(MEAN_FILE, normalize(mean, 0, 255, dtype=np.uint8))
	eigenvectors = model.getMat("eigenvectors")
	pos_eigenvector = eigenvectors[:,0].reshape(faces[0].shape)
	cv2.imwrite('meanp.png', normalize(pos_eigenvector, 0, 255, dtype=np.uint8))
	neg_eigenvector = eigenvectors[:,1].reshape(faces[0].shape)
	cv2.imwrite('meann.png', normalize(neg_eigenvector, 0, 255, dtype=np.uint8))
