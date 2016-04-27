import cv2
import os
import config
import face
import json
import subprocess

def walk_folders(directory):
	for root, dirs, files in os.walk(directory):
		for foldername in dirs:
			yield os.path.join(root, foldername)

with open('training/info.json') as data_file:    
    	data = json.load(data_file)
data_file.close()

if __name__ == '__main__':
	# Load training data into model
	print 'Loading training data...'
	model = cv2.createEigenFaceRecognizer()
	model.load(config.TRAINING_FILE)
	print 'Training data loaded!'
	camera = config.get_camera()
	print 'Running face recognizer...'
	lcount = 0
	dic = 0
	while True:
		print 'looking for face...'
		image = camera.read()
		# Convert image to grayscale.
		image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		# Get coordinates of single face in captured image.
		result = face.detect_single(image)
		if result is None:
			print 'Could not detect a single face!'
			continue
		x, y, w, h = result
		# Crop and resize image to face.
		crop = face.resize(face.crop(image, x, y, w, h))
		# Test face against model.
		label, confidence = model.predict(crop)
		print label
		x = 0
		y=len(data)
		while x < y:
			lno = data[dic]['infoid']
			lname = data[dic]['fname']
			labout = data[dic]['relationship']
			if label == lno:
				lcount += 1
				if lcount > 5:
					cmd = '"The person before you, is, "'
					cmd1 = str(lname)
					cmd2 = '", He is your, "'
					cmd3 = str(labout)
					subprocess.call('echo '+cmd+cmd1+cmd2+cmd3+'| festival --tts', shell=True)
					print 'PREDICTED',lname,'face'
					if label == lno and confidence < config.POSITIVE_THRESHOLD:
						print 'RECOGNIZED',lname,'face! with ',lno,'label number'
						break
					if lcount == 10:
						break
			x += 1
			dic += 1
			if dic == len(data):
				dic = 0
		if lcount == 10:
			break
		if label == lno and confidence < config.POSITIVE_THRESHOLD:
			break
