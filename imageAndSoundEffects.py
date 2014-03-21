from Tkinter import *
from ttk import Frame, Style
from PIL import Image, ImageTk
from numpy import *
from scipy.misc import imread
from scipy.misc import imsave
from scipy.misc import lena
from scipy.io import wavfile
from scipy.signal import convolve2d
from scipy.ndimage.filters import convolve as convolve2
import scipy.ndimage as ndimage
import pylab as pl

#Sound
import pyaudio
import wave
import sys
import os.path

#Debugging
import pdb

#import random
centerImageLabel = None
img = None
_img = None
sound = None
red = None
green = None
blue = None
isSoundUpdated = None
soundName = None
imname = None

class App(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		global img, _img
		img = ImageTk.PhotoImage(Image.open('/Users/NatalyMoreno/Documents/Code/MAT201A/final/final/jpgs/yeyito.jpg'))
		_img = imread('/Users/NatalyMoreno/Documents/Code/MAT201A/final/final/jpgs/yeyito.jpg')
		setGlobals()
		self.initUI()
		
	def initUI(self):
		self.parent.title("Image and Sound Effects") #, background = "#2c2825")
		#self.parent.minsize(800,500)
		
		x = 14
		y = 4
		b = 10
		wl = 60
		h = 2
		
		#Set Default Styles for GUI Components
		#Style().configure("TFrame", background = "white")
		Style().configure("TButton", padding=(0, 5, 0, 5), font = 'serif 12', background = "#F5DEB3")
		#frame = Frame(self, relief=RAISED, borderwidth=1)
		#frame.pack(fill=BOTH, expand=1)
		#Title Bar and Buttons: #2c2825
		#Clickable Text Color: #edbc6f
		#Unclickable Text Color: #fbf9f9
		#Background Color: #050505
		
		#Create 20x20 Grid
		for columns in range(0, 20):
			self.columnconfigure(columns, pad = 14)
		for rows in range(0, 20):
			self.rowconfigure(rows, pad = 14)

		#Buttons for Image Filters
		imageFiltersLabel = Label(self, text = "Image Filters", font = 'serif 14', padx = 4, pady = 17)
		imageFiltersLabel.grid(row = 1, column = 1, columnspan = 3)
		
		#Convolution, Gaussian Blur, Gaussian Filter, Sharpening, Uniform Filter, Median Filter, Add Noise, Binary Erosion, Binary Dilation, Pixel Mapping, Dynamic Range Processing
		convolve		= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Convolve", command = self.convolveClicked)
		gaussianBlur	= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Gaussian Blur", command = self.gaussianBlurClicked)
		gaussianFilter  = Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Gaussian Filter", command = self.gaussianFilterClicked)
		sharpen			= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Sharpen", command = self.sharpenClicked)
		uniformFilter	= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Uniform Filter", command = self.uniformClicked)
		medianFilter	= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Median Filter", command = self.medianClicked)
		binaryErosion	= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Binary Erosion", command = self.binaryErosionClicked)
		binaryDilation	= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Binary Dilation", command = self.binaryDilationClicked)
		pixelMapping	= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Pixel Mapping", command = self.pixelMappingClicked)
		dynamicRange	= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Dynamic Range Process", command = self.dynamicRangeClicked)
		addNoise		= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Add Noise", command = self.addNoiseClicked)
		grayscale		= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Black & White", command = self.grayscaleClicked)
		
		convolve.grid(		row = 2, column = 1, padx = x, pady = y, sticky = 'w')
		gaussianBlur.grid(	row = 2, column = 3, padx = x, pady = y, sticky = 'w')
		gaussianFilter.grid(row = 3, column = 1, padx = x, pady = y, sticky = 'w')
		sharpen.grid(		row = 3, column = 3, padx = x, pady = y, sticky = 'w')
		uniformFilter.grid(	row = 4, column = 1, padx = x, pady = y, sticky = 'w')
		medianFilter.grid(	row = 4, column = 3, padx = x, pady = y, sticky = 'w')
		binaryErosion.grid(	row = 5, column = 1, padx = x, pady = y, sticky = 'w')
		binaryDilation.grid(row = 5, column = 3, padx = x, pady = y, sticky = 'w')
		pixelMapping.grid(	row = 6, column = 1, padx = x, pady = y, sticky = 'w')
		dynamicRange.grid(	row = 6, column = 3, padx = x, pady = y, sticky = 'w')
		addNoise.grid(		row = 7, column = 1, padx = x, pady = y, sticky = 'w')
		grayscale.grid(		row = 7, column = 3, padx = x, pady = y, sticky = 'w')
		
		#Label for Image in Center
		global centerImageLabel
		centerImageLabel = Label(self, image = img, borderwidth = 5, highlightthickness = 5, highlightcolor = 'black', highlightbackground = 'black', background = 'yellow', padx = 4, pady = 4, width = 500, height = 500)
		centerImageLabel.grid(row = 1, column = 5, rowspan = 10, columnspan = 10)

		#Buttons for Sound Windows and Filters
		soundWindow = Label(self, text = "Windows", font = 'serif 14', padx = 4, pady = 17)
		soundWindow.grid(row = 1, column = 16, columnspan = 3)
		
		#Hamming, Hann, Welch, Rectangle, Nyquist, Blackman Harris, Bartlett
		hamming		= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Hamming", command = self.hammingClicked)
		hann		= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Hann", command = self.hannClicked)
		#welch		= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Welch")
		rectangle	= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Rectangle", command = self.rectangleClicked)
		#nyquist		= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Nyquist")
		blackHarris	= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Blackman-Harris", command = self.blackmanHarrisClicked)
		bartlett	= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Bartlett", command = self.bartlettClicked)
		kaiser	= Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Kaiser", command = self.kaiserClicked)

		hamming.grid(	 row = 2, column = 16, padx = x, pady = y, sticky = 'e')
		hann.grid(		 row = 2, column = 18, padx = x, pady = y, sticky = 'e')
		#welch.grid(		 row = 3, column = 16, padx = x, pady = y, sticky = 'e')
		rectangle.grid(	 row = 3, column = 16, padx = x, pady = y, sticky = 'e')
		#nyquist.grid(	 row = 4, column = 16, padx = x, pady = y, sticky = 'e')
		blackHarris.grid(row = 3, column = 18, padx = x, pady = y, sticky = 'e')
		bartlett.grid(	 row = 4, column = 16, padx = x, pady = y, sticky = 'e')
		kaiser.grid(	 row = 4, column = 18, padx = x, pady = y, sticky = 'e')
		
		#Buttons for Saving and Loading and Playing
		saveImage = Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Save Image", command = self.saveImageClicked)
		loadImage = Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Load Image or Sound", command = self.loadImageClicked)
		saveSound = Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Save Sound", command = self.saveSoundClicked)
		playSound = Button(self, width = b, height = h, padx = b, pady = b, wraplength = wl, text = "Play Sound", command = self.playSoundClicked)
		
		saveImage.grid(row = 13, column = 9,  padx = x, pady = y, sticky = 'w')
		loadImage.grid(row = 13, column = 1,  padx = x, pady = y, sticky = 'w')
		saveSound.grid(row = 13, column = 10, padx = x, pady = y, sticky = 'e')
		playSound.grid(row = 13, column = 18, padx = x, pady = y, sticky = 'e')

		self.pack()

	#Play Sound Button Listener
	def playSoundClicked(self):
		saveSound()
		playSound()
		
	#Load Image Button Listener
	def loadImageClicked(self):
		self.loadImageWindow = Toplevel(self.parent)
		self.app = loadImageApp(self.loadImageWindow)

	#Convolve Button Listener
	def convolveClicked(self):
		self.convolveWindow = Toplevel(self.parent)
		self.app = convolveApp(self.convolveWindow)
	
	#Black & White (grayscale) Button Listener
	def grayscaleClicked(self):
		global _img, red, green, blue
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] =  (red[a, b] + green[a,b] + blue[a,b]) / 3
				_img[a, b, 1] =	 (red[a, b] + green[a,b] + blue[a,b]) / 3
				_img[a, b, 2] =  (red[a, b] + green[a,b] + blue[a,b]) / 3
		
		updateImage()

	#Gaussian Blur Button Listener
	def gaussianBlurClicked(self):
		single_dot = zeros((101, 101))
		single_dot[50, 50] = 1.0
		gauss_kernel = ndimage.gaussian_filter(single_dot, 5)
		
		global _img, red, green, blue
		red   = convolve2(red.astype(float), gauss_kernel.astype(float))
		green = convolve2(green.astype(float), gauss_kernel.astype(float))
		blue  = convolve2(blue.astype(float), gauss_kernel.astype(float))
		
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = red[a, b]
				_img[a, b, 1] = green[a, b]
				_img[a, b, 2] = blue[a, b]
		updateImage()
	
	#Gaussian Filter Button Listener
	def gaussianFilterClicked(self):
		global _img, red, green, blue
		
		red   = ndimage.gaussian_filter(red, 5)
		green = ndimage.gaussian_filter(green, 5)
		blue  = ndimage.gaussian_filter(blue, 5)
		
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = red[a, b]
				_img[a, b, 1] = green[a, b]
				_img[a, b, 2] = blue[a, b]
		
		updateImage()
	
	#Sharpen Button Listener
	def sharpenClicked(self):
		self.sharpenWindow = Toplevel(self.parent)
		self.app = sharpenApp(self.sharpenWindow)
	
	#Uniform Filter Button Listener
	def uniformClicked(self):
		global _img, red, green, blue
		
		red = ndimage.uniform_filter(red, 15)
		green = ndimage.uniform_filter(green, 15)
		blue = ndimage.uniform_filter(blue, 15)
		
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = red[a, b]
				_img[a, b, 1] = green[a, b]
				_img[a, b, 2] = blue[a, b]
		updateImage()
	
	#Median Filter Button Listener
	def medianClicked(self):
		global _img, red, green, blue
		
		red = ndimage.median_filter(red, size = 15)
		green = ndimage.median_filter(green, size = 15)
		blue = ndimage.median_filter(blue, size =15)
		
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = red[a, b]
				_img[a, b, 1] = green[a, b]
				_img[a, b, 2] = blue[a, b]
		updateImage()
				
	#Binary Erosion Button Listener
	def binaryErosionClicked(self):
		self.binaryErosionWindow = Toplevel(self.parent)
		self.app = binaryErosionApp(self.binaryErosionWindow)
	
	#Binary Dilation Button Listener
	def binaryDilationClicked(self):
		self.binaryDilationWindow = Toplevel(self.parent)
		self.app = binaryDilationApp(self.binaryDilationWindow)
	
	#Pixel Mapping Button Listener
	def pixelMappingClicked(self):
		global _img, red, green, blue

		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				red[a, b]   = warp(red[a, b], 127)
				green[a, b] = warp(green[a, b], 127)
				blue[a, b]  = warp(blue[a, b], 127)

		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = red[a, b]
				_img[a, b, 1] = green[a, b]
				_img[a, b, 2] = blue[a, b]
		updateImage()

	#Dynamic Range Button Listener
	def dynamicRangeClicked(self):
		global _img, red, green, blue
		
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				red[a, b]   = dynaRange(red[a, b], 128, 2.0)
				green[a, b] = dynaRange(green[a, b], 128, 2.0)
				blue[a, b]  = dynaRange(blue[a, b], 128, 2.0)
			
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = red[a, b]
				_img[a, b, 1] = green[a, b]
				_img[a, b, 2] = blue[a, b]
		updateImage()
		
	#Add Noise Button Listener
	def addNoiseClicked(self):
		self.addNoiseWindow = Toplevel(self.parent)
		self.app = addNoiseApp(self.addNoiseWindow)
	
	#Hamming Button Listener
	def hammingClicked(self):
		global sound
		
		imMod = 0
		if sound == None:
			imageToSound()
			soundToImage()
			imMod = 1

		window = hamming(sound.shape[0])
		sound = sound * window

		if imMod == 0:
			soundToImage()
				
	#Hann Button Listener
	def hannClicked(self):
		global sound

		imMod = 0
		if sound == None:
			imageToSound()
			soundToImage()
			imMod = 1

		window = hanning(sound.shape[0])
		sound = sound * window
		
		if imMod == 0:
			soundToImage()

	#Rectangle Button Listener
	def rectangleClicked(self):
		global sound
		
		imMod = 0
		if sound == None:
			imageToSound()
			soundToImage()
			imMode = 1
		
		window = kaiser(sound.shape[0], 0)
		sound = sound * window
		
		if imMod == 0:
			soundToImage()

	#Blackman-Harris Button Listener
	def blackmanHarrisClicked(self):
		global sound

		imMod = 0
		if sound == None:
			imageToSound()
			soundToImage()
			imMod = 1

		window = blackman(sound.shape[0])
		sound = sound * window

		if imMod == 0:
			soundToImage()

	#Welch Button Listener
	#Nyquist Button Listener
	#Bartlett Button Listener
	def bartlettClicked(self):
		global sound

		imMod = 0
		if sound == None:
			imageToSound()
			soundToImage()
			imMod = 1

		window = bartlett(sound.shape[0])
		sound = sound * window

		if imMod == 0:
			soundToImage()
	#Kaiser Button Listener
	def kaiserClicked(self):
		global sound
		
		imMod = 0
		if sound == None:
			imageToSound()
			soundToImage()
			imMode = 1
				
		window = kaiser(sound.shape[0], 14)
		sound = sound * window

		if imMod == 0:
			soundToImage()
				
	#Save Image Button Listener
	def saveImageClicked(self):
		global _img, imname
		count = 0
		imname = 'myImage%i.jpg'%count
		
		while os.path.isfile(imname):
			count += 1
			imname = 'myImage%i.jpg'%count
		
		
		imsave(imname, _img)
		print "Image Saved as %s"%imname

	#Save Sound Button Listener
	def saveSoundClicked(self):
		#global isSoundUpdated, sound
		
		#if isSoundUpdated == 0:
		#	imageToSound()
		
		saveSound()
		#wavfile.write('/Users/NatalyMoreno/Documents/Code/MAT201A/final/final/mySounds/sound.wav', 44100, sound)
		print "Image Saved as sound.wav"
#############################################
###############Binary Dilation###############
#############################################
class binaryDilationApp:
	def __init__(self, parent):
		self.parent = parent
		self.frame = Frame(self.parent)
		self.parent.title("Binary Dilation")
		self.initUI()
	
	def initUI(self):
		#Create 3x3 Grid
		for columns in range(0, 3):
			self.parent.columnconfigure(columns, pad = 14)
		for rows in range(0, 3):
			self.parent.rowconfigure(rows, pad = 14)
		
		#Add Noise Options
		binaryDilation1 = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Binary Dilation 1", command = self.binaryDilation1Clicked)
		binaryDilation2 = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Binary Dilation 2", command = self.binaryDilation2Clicked)
		
		binaryDilation1.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'w')
		binaryDilation2.grid(row = 1, column = 2, padx = 10, pady = 10, sticky = 'w')
		
		self.frame.pack()

	def binaryDilation1Clicked(self):
		global _img, red, green, blue
		
		structure = zeros((20,20))
		structure[range(20), range(20)] = 1.0
		
		red   = where(red   > 255.0 * 0.7, 1.0, 0.0)
		green = where(green > 255.0 * 0.7, 1.0, 0.0)
		blue  = where(blue  > 255.0 * 0.7, 1.0, 0.0)
		
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = (red[a, b] * 255.0).astype('uint8')
				_img[a, b, 1] = (green[a, b] * 255.0).astype('uint8')
				_img[a, b, 2] = (blue[a, b] * 255.0).astype('uint8')
		updateImage()
		
	def binaryDilation2Clicked(self):
		global _img, red, green, blue
			
		structure = zeros((20,20))
		structure[range(20), range(20)] = 1.0
		
		red   = where(red   > 255.0 * 0.7, 1.0, 0.0)
		green = where(green > 255.0 * 0.7, 1.0, 0.0)
		blue  = where(blue  > 255.0 * 0.7, 1.0, 0.0)
		
		red   = ndimage.binary_dilation(red, structure)
		green = ndimage.binary_dilation(green, structure)
		blue  = ndimage.binary_dilation(blue, structure)
		
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = (red[a, b] * 255.0).astype('uint8')
				_img[a, b, 1] = (green[a, b] * 255.0).astype('uint8')
				_img[a, b, 2] = (blue[a, b] * 255.0).astype('uint8')
		updateImage()

#############################################
###############Binary Erosion################
#############################################
class binaryErosionApp:
	def __init__(self, parent):
		self.parent = parent
		self.frame = Frame(self.parent)
		self.parent.title("Binary Erosion")
		self.initUI()
	
	def initUI(self):
		#Create 3x3 Grid
		for columns in range(0, 3):
			self.parent.columnconfigure(columns, pad = 14)
		for rows in range(0, 3):
			self.parent.rowconfigure(rows, pad = 14)
		
		#Add Noise Options
		binaryErosion1 = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Binary Erosion 1", command = self.binaryErosion1Clicked)
		binaryErosion2 = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Binary Erosion 2", command = self.binaryErosion2Clicked)
		
		binaryErosion1.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'w')
		binaryErosion2.grid(row = 1, column = 2, padx = 10, pady = 10, sticky = 'w')
		
		self.frame.pack()

	def binaryErosion1Clicked(self):
		global _img, red, green, blue
			
		structure = zeros((20, 20))
		structure[range(20), range(20)] = 1.0
		
		red = where(red[:,:] > 255.0 * 0.6, 1.0, 0.0)
		green = where(green[:,:] > 255.0 * 0.6, 1.0, 0.0)
		blue = where(blue[:,:] > 255.0 * 0.6, 1.0, 0.0)
			
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = (red[a, b] * 255.0).astype('uint8')
				_img[a, b, 1] = (green[a, b] * 255.0).astype('uint8')
				_img[a, b, 2] = (blue[a, b] * 255.0).astype('uint8')
		updateImage()
		
	def binaryErosion2Clicked(self):
		global _img, red, green, blue
		
		structure = zeros((20, 20))
		structure[range(20), range(20)] = 1.0
		
		red = where(red[:,:] > 255.0 * 0.6, 1.0, 0.0)
		green = where(green[:,:] > 255.0 * 0.6, 1.0, 0.0)
		blue = where(blue[:,:] > 255.0 * 0.6, 1.0, 0.0)
		
		red   = ndimage.binary_erosion(red, structure)
		green = ndimage.binary_erosion(green, structure)
		blue  = ndimage.binary_erosion(blue, structure)
		
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = (red[a, b] * 255.0).astype('uint8')
				_img[a, b, 1] = (green[a, b] * 255.0).astype('uint8')
				_img[a, b, 2] = (blue[a, b] * 255.0).astype('uint8')
		updateImage()

#############################################
#################Add Noise###################
#############################################
#import pdb
class addNoiseApp:
	def __init__(self, parent):
		self.parent = parent
		self.frame = Frame(self.parent)
		self.parent.title("Add Noise")
		self.initUI()

	def initUI(self):
		#Create 3x3 Grid
		for columns in range(0, 3):
			self.parent.columnconfigure(columns, pad = 14)
		for rows in range(0, 3):
			self.parent.rowconfigure(rows, pad = 14)

		#Add Noise Options
		noise = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Noise", command = self.noiseClicked)
		colorNoise = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Color Noise", command = self.colorNoiseClicked)

		noise.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'w')
		colorNoise.grid(row = 1, column = 2, padx = 10, pady = 10, sticky = 'w')
			
		self.frame.pack()

	def noiseClicked(self):
		global _img

		whiteNoise = where(random.random(_img.shape) > 0.9, 1.0, 0.0)

		#Turn into black and white
		nred   = zeros((whiteNoise.shape[0], whiteNoise.shape[1]))
		ngreen = zeros((whiteNoise.shape[0], whiteNoise.shape[1]))
		nblue  = zeros((whiteNoise.shape[0], whiteNoise.shape[1]))

		for a in range(whiteNoise.shape[0]):
			for b in range(whiteNoise.shape[1]):
				nred[a, b]   = whiteNoise[a, b, 0]
				ngreen[a, b] = whiteNoise[a, b, 1]
				nblue[a, b]  = whiteNoise[a, b, 2]

		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				whiteNoise[a, b, 0] =  (nred[a, b] + ngreen[a,b] + nblue[a,b]) / 3.0
				whiteNoise[a, b, 1] =  (nred[a, b] + ngreen[a,b] + nblue[a,b]) / 3.0
				whiteNoise[a, b, 2] =  (nred[a, b] + ngreen[a,b] + nblue[a,b]) / 3.0

		_img = (((_img/255.0) + whiteNoise) * 255.0).astype('uint8')
		updateImage()
	
	def colorNoiseClicked(self):
		global _img

		colorNoise = (where(random.random(_img.shape) > 0.9, 0.5, 0.0))
		_img = (((_img/255.0) + colorNoise) * 255.0).astype('uint8')
		updateImage()

#############################################
##################Sharpen####################
#############################################
class sharpenApp:
	def __init__(self, parent):
		self.parent = parent
		self.frame = Frame(self.parent)
		self.parent.title("Sharpen")
		self.initUI()

	def initUI(self):
		#Create 7x7 Grid
		for columns in range(0, 7):
			self.parent.columnconfigure(columns, pad = 14)
		for rows in range(0, 7):
			self.parent.rowconfigure(rows, pad = 14)

		#Sharpen Options
		sharpen1 = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Sharpen 1", command = self.sharpen1Clicked)
		sharpen2 = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Sharpen 2", command = self.sharpen2Clicked)
		sharpen3 = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Sharpen 3", command = self.sharpen3Clicked)
		sharpen4 = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Color Sharpen 1", command = self.sharpen4Clicked)
		sharpen5 = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Color Sharpen 2", command = self.sharpen5Clicked)
		sharpen6 = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Color Sharpen 3", command = self.sharpen5Clicked)

		sharpen1.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'w')
		sharpen2.grid(row = 1, column = 2, padx = 10, pady = 10, sticky = 'w')
		sharpen3.grid(row = 1, column = 3, padx = 10, pady = 10, sticky = 'w')
		sharpen4.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = 'w')
		sharpen5.grid(row = 2, column = 2, padx = 10, pady = 10, sticky = 'w')
		sharpen6.grid(row = 2, column = 3, padx = 10, pady = 10, sticky = 'w')

		self.frame.pack()

	def sharpen1Clicked(self):
		global _img
		c = ndimage.gaussian_filter(_img, 1)
		c = _img - c * 0.5 #fades
		#c = _img - c #fun one
		_img = c
		updateImage()
	
	def sharpen2Clicked(self):
		global _img
		c = ndimage.gaussian_filter(_img, 2)
		c = _img - c * 0.5 #fades
		#c = _img - c #fun one
		_img = c
		updateImage()

	def sharpen3Clicked(self):
		global _img
		c = ndimage.gaussian_filter(_img, 3)
		c = _img - c * 0.5 #fades
		#c = _img - c #fun one
		_img = c
		updateImage()

	def sharpen4Clicked(self):
		global _img, red, green, blue
		
		tred = ndimage.gaussian_filter(red, 1)
		tgreen = ndimage.gaussian_filter(green, 1)
		tblue = ndimage.gaussian_filter(blue, 1)
		
		red = red - tred * 0.5
		green = green - tgreen * 0.5
		blue = blue - tblue * 0.5
		
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = red[a, b]
				_img[a, b, 1] = green[a, b]
				_img[a, b, 2] = blue[a, b]
		updateImage()
	
	def sharpen5Clicked(self):
		global _img, red, green, blue
		
		tred = ndimage.gaussian_filter(red, 2)
		tgreen = ndimage.gaussian_filter(green, 2)
		tblue = ndimage.gaussian_filter(blue, 2)
		
		red = red - tred * 0.5
		green = green - tgreen * 0.5
		blue = blue - tblue * 0.5
		
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = red[a, b]
				_img[a, b, 1] = green[a, b]
				_img[a, b, 2] = blue[a, b]
		updateImage()

	def sharpen6Clicked(self):
		global _img, red, green, blue

		tred = ndimage.gaussian_filter(red, 3)
		tgreen = ndimage.gaussian_filter(green, 3)
		tblue = ndimage.gaussian_filter(blue, 3)

		red = red - tred * 0.5
		green = green - tgreen * 0.5
		blue = blue - tblue * 0.5
		
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = red[a, b]
				_img[a, b, 1] = green[a, b]
				_img[a, b, 2] = blue[a, b]
		updateImage()

#############################################
##################Convolve###################
#############################################
class convolveApp:
	def __init__(self, parent):
		self.parent = parent
		self.frame = Frame(self.parent)
		self.parent.title("Convolve")
		self.initUI()
			
	def initUI(self):
		#Create 5x5 Grid
		for columns in range(0, 5):
			self.parent.columnconfigure(columns, pad = 14)
		for rows in range(0, 5):
			self.parent.rowconfigure(rows, pad = 14)
		
		#Convolve Options
		ghost3DRGB = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Ghost 3D Convolve R,G,B", command = self.ghost3DClickedRGB)
		ghost3DTogether = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Ghost 3D Convolve Together", command = self.ghost3DTogetherClicked)
		ghostFun1  = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Ghost Fun1", command = self.ghostFun1Clicked)
		ghostFun2  = Button(self.frame, width = 10, height = 3, padx = 10, pady = 10, wraplength = 60, text = "Ghost Fun2", command = self.ghostFun2Clicked)
		
		ghost3DRGB.grid(  row = 1, column = 1, padx = 10, pady = 10, sticky = 'w')
		ghost3DTogether.grid(row = 1, column = 2, padx = 10, pady = 10, sticky = 'w')
		ghostFun1.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = 'w')
		ghostFun2.grid(row = 2, column = 2, padx = 10, pady = 10, sticky = 'w')

		self.frame.pack()

	def ghost3DClickedRGB(self):
		#Create 3D Ghost Kernel
		kernel_ghost = zeros((31, 31))
		kernel_ghost[15, 15] = 0.588
		kernel_ghost[25, 25] = 0.411

		global _img, red, green, blue
		red   = convolve2(red.astype(float), kernel_ghost.astype(float))
		green = convolve2(green.astype(float), kernel_ghost.astype(float))
		blue  = convolve2(blue.astype(float), kernel_ghost.astype(float))
		
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = red[a, b]
				_img[a, b, 1] = green[a, b]
				_img[a, b, 2] = blue[a, b]
		updateImage()

	def ghost3DTogetherClicked(self):
		#Create Ghost Kernel
		kernel_ghost = zeros((31, 31, 3))
		
		#1 + .7 + 1 + .7 + 1 + .7 = 3 + (.7 * 3) = 5.1
		kernel_ghost[15, 15, 0] = 0.196
		kernel_ghost[25, 25, 0] = 0.137
		kernel_ghost[15, 15, 1] = 0.196
		kernel_ghost[25, 25, 1] = 0.137
		kernel_ghost[15, 15, 2] = 0.196
		kernel_ghost[25, 25, 2] = 0.137

		global _img
		_img = convolve2(_img, kernel_ghost)
		updateImage()

	def ghostFun1Clicked(self):
		kernel_ghost = zeros((31, 31))
		kernel_ghost[15, 15] = 1
		kernel_ghost[25, 25] = 0.7

		global _img, red, green, blue
		red   = convolve2(red, kernel_ghost)
		green = convolve2(green, kernel_ghost)
		blue  = convolve2(blue, kernel_ghost)
			
		for a in range(0, _img.shape[0]):
			for b in range(0, _img.shape[1]):
				_img[a, b, 0] = red[a, b]
				_img[a, b, 1] = green[a, b]
				_img[a, b, 2] = blue[a, b]
		
		updateImage()

	def ghostFun2Clicked(self):
		kernel_ghost = zeros((31, 31, 3))
		kernel_ghost[15, 15, 0] = 1
		kernel_ghost[25, 25, 0] = 0.7
		kernel_ghost[15, 15, 1] = 1
		kernel_ghost[25, 25, 1] = 0.7
		kernel_ghost[15, 15, 2] = 1
		kernel_ghost[25, 25, 2] = 0.7
		
		global _img
		_img = convolve2(_img, kernel_ghost)
		updateImage()

#############################################
#################Load Image##################
#############################################
fileNameEntry = None
v = None

class loadImageApp:
	def __init__(self, parent):
		self.parent = parent
		self.frame = Frame(self.parent)
		self.initUI()
		
	def initUI(self):
		self.parent.title("Load an Image or Sound File")
		self.parent.minsize(314, 137)
		
		#Create a 10x10 Grid
		for columns in range(0, 10):
			self.parent.columnconfigure(columns, pad = 14)
		for rows in range(0, 10):
			self.parent.rowconfigure(rows, pad = 14)
		
		#File Name: (label)
		fileNameLabel = Label(self.frame, text = "File Name: ", font = 'serif 12', padx = 4, pady = 17)
		fileNameLabel.grid(row = 1, column = 1)
		
		#File Name Text Entry Box
		global fileNameEntry
		fileNameEntry = Entry(self.frame, font = 'serif 12')
		fileNameEntry.grid(row = 1, column = 2, sticky = 'we')
		
		#Upload Button
		uploadButton = Button(self.frame, font = 'serif 12', height = 1, width = 7, padx = 10, pady = 10, text = "Upload", command = self.uploadClick)
		uploadButton.grid(row = 3, column = 2, sticky = 'e')
		
		#Error Label
		global v
		v = StringVar()
		v.set("")
		errorLabel = Label(self.frame, textvariable = v, font = 'serif 10', fg = 'red', padx = 4, pady = 17)
		errorLabel.grid(row = 5, column = 0, columnspan = 4)
		
		self.frame.pack()

	#Upload Button Listener
	def uploadClick(self):
		global img, _img, centerImageLabel, fileNameEntry, v, isSoundUpdated, sound

		file_name = fileNameEntry.get()
		
		if file_name.endswith(".jpg"):
			try:
				file_name = "jpgs/" + file_name
				img  = ImageTk.PhotoImage(Image.open(file_name))
				_img = imread(file_name)
				v.set("Upload Successful!")
				centerImageLabel.configure(image = img)
				setGlobals()
				self.parent.destroy()
			except:
				v.set("Unable to load image. Please select a different image.")

		elif file_name.endswith(".wav"):
			
			try:
				file_name = "/Users/NatalyMoreno/Documents/Code/MAT201A/final/final/mySounds/" + file_name
				sound = wavfile.read(file_name)
				v.set("Upload Successful!")
				
			except:
				v.set("Unable to load sound. Please select a different sound file.")
			
			centerImageLabel.configure(image = img)
			soundToImage()
			setGlobals()
			self.parent.destroy()
			
				
		else:
			v.set("Please choose a valid file name.")


#for x in range(0,400):
#			for y in range(0,400):
#				r = 7%200 + 55
#				g = 9%200 + 55
#				b = 111%200 + 55
#				dotcolor = '#%02x%02x%02x' %(r,g,b)
#				self.img.put(dotcolor,to=(x,y))

#		l = Label(root, image = self.img)
#		l.pack()

#############################################
###########Global Helper Functions###########
#############################################
def updateImage():
	global centerImageLabel, _img, img
	imsave('outimg.jpg', _img)
	img = ImageTk.PhotoImage(Image.open('outimg.jpg'))
	centerImageLabel.configure(image = img)
	setGlobals()

def setGlobals():
	global _img, img2D, red, green, blue, isSoundUpdated

	isSoundUpdated = 0
	img2D = _img[:, :, 0]

	#Save r,g,b values to put color back in later
	n = 0
	red   = zeros((_img.shape[0], _img.shape[1]))
	green = zeros((_img.shape[0], _img.shape[1]))
	blue  = zeros((_img.shape[0], _img.shape[1]))
	
	for a in range(_img.shape[0]):
		for b in range(_img.shape[1]):
			red[a, b]   = _img[a, b, 0]
			green[a, b] = _img[a, b, 1]
			blue[a, b]  = _img[a, b, 2]
			n = n + 1

#Convert image to sound
def imageToSound():
	global _img, sound, isSoundUpdated
	soundFile = []
	
	for row in range(len(_img[:,0])-1):
		mag_spec = _img[row,:,1]
		phs_spec = zeros(len(mag_spec))
		X = [pl.np.complex(cos(phs)* mag, sin(phs)* mag) for mag, phs in zip(mag_spec, phs_spec)]
		x = fft.irfft(X)
		soundFile.extend(x)

	#Flatten the Array
#	sound_flattened = []
#	for row in soundFile:
#		for col in row:
#			sound_flattened.extend(col)

	sound = asarray(soundFile)
	isSoundUpdated = 1

#Convert sound to image
def soundToImage():
	global img, _img, sound
	#print sound[1].shape

	_img = imread('/Users/NatalyMoreno/Documents/Code/MAT201A/final/examples/jpgs/lena.jpg')
	soundArray = sound
	#pdb.set_trace()
	#print soundArray
	#print soundArray.shape[0]
	sarSize = soundArray.shape
	a = 0
	for x in range(0, 512):
		for y in range(0, 512):
			if a >= sarSize[0]-1:
				a = 0
			_img[x][y][0] = soundArray[a].astype('uint8')
			a = a + 1
			
			if a >= sarSize[0]-1:
				a = 0
			_img[x][y][1] = soundArray[a].astype('uint8')
			a = a + 1
			
			if a >= sarSize[0]-1:
				a = 0
			_img[x][y][2] = soundArray[a].astype('uint8')#+ soundArray[a][1].astype('uint8')) % 255
			a = a + 1

	updateImage()

#import pdb
#pdb.set_trace()

#Save Sound
def saveSound():
	global isSoundUpdated, sound
	
	if isSoundUpdated == 0:
		imageToSound()

	outSound = sound * (2**15)/255.0
	outSound = (outSound * 1.4).astype(int16)
	
	#pdb.set_trace()
	wavfile.write('/Users/NatalyMoreno/Documents/Code/MAT201A/final/final/mySounds/sound.wav', 44100, outSound)

#Code is from http://stackoverflow.com/questions/6951046/pyaudio-help-play-a-file
def playSound():
	#length of data to read
	chunk = 1024
	
	#open wave file to read
	wf = wave.open('mySounds/sound.wav', 'rb')
	p = pyaudio.PyAudio()

	#open stream based on the wave object which has been input.
	stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

	#read data (based on the chunk size)
	data = wf.readframes(chunk)

	# play stream (looping from beginning of file to the end)
	while data != '':
		#writing to the stream is what *actually* plays the sound.
		stream.write(data)
		data = wf.readframes(chunk)

	#cleanup stuff.
	stream.close()
	p.terminate()

#Warp - Pixel Mapping
def warp(a, b):
    if a < b:
        out = a + b
    else:
        out = a - b
    return out

#dynaRange - Dynamic Range
def dynaRange(pixel, center, factor):
    centered = float(pixel) - center
    out = (centered*factor) + center
    if out > 255:
        out = 255
    if out < 0:
        out = 0
    return uint8(out)


def main():
	root = Tk()
	app = App(root)
	root.mainloop()

if __name__ == '__main__':
	main()
