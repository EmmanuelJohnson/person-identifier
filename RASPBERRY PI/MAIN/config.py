# Threshold for the confidence of a recognized face
POSITIVE_THRESHOLD = 2300.0

# File to save and load face recognizer model.
TRAINING_FILE = 'training.xml'

# Size in pixels to resize images for training and prediction
FACE_WIDTH  = 92
FACE_HEIGHT = 112

# Face detection cascade classifier
HAAR_FACES         = 'haarcascade_frontalface_alt.xml'
HAAR_SCALE_FACTOR  = 1.3
HAAR_MIN_NEIGHBORS = 4
HAAR_MIN_SIZE      = (30, 30)

# Filename to use when saving the most recently captured image
DEBUG_IMAGE = 'capture.pgm'

def get_camera():
	# Camera to use for capturing images
	#import picam
	#return picam.OpenCVCapture()
	import webcam
	return webcam.OpenCVCapture(device_id=0)
