#!/usr/bin/env python

################################################################################
##
## Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
################################################################################

################################################################################
##	System dependencies
################################################################################
import 	sys
from 		os.path 	import isfile
from 		PyQt4 		import QtCore, QtGui

################################################################################
##	Variables
################################################################################
IL = []

################################################################################
##	Initialise file list before start
################################################################################
if len(sys.argv) == 2:												#Check if a parameter is provided
	LN = sys.argv[1]														#	Grab parameter as List Name
	LF = open( LN, 'r' )												#	Open the LN into List File
	IL = LF.read().rstrip('\n').split('\n')			#	Read file and split into a list
else:																					#If no parameter is provided
	print "No ImageList parameter provided"			#	Console log message
	exit()																			#	Quit application


################################################################################
##	GUI and Application code
################################################################################
class ImageViewer(QtGui.QMainWindow):

	##############################################################################
	##	Initialise application GUI
	##############################################################################
	def __init__(self):
		super(ImageViewer, self).__init__()
		self.IC = 0																								#Image Counter
		self.G = open('image_G.txt', 'w')													#Create good file
		self.B = open('image_B.txt', 'w')													#Create bad file
		
		self.imageLabel = QtGui.QLabel()													#Holder for image
		self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
		self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
																	QtGui.QSizePolicy.Ignored)
		self.imageLabel.setScaledContents(True)
		
		self.scrollArea = QtGui.QScrollArea()											#Container for
		self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)		# image with
		self.scrollArea.setWidget(self.imageLabel)								# scroll bars
		
		self.setCentralWidget(self.scrollArea)										#Center area
		
		self.createActions()																			#Reg actions
		self.createMenus()																				#Generate menues
	
		self.resizeEvent = self.sizeAdjust												#Resize event
		
		self.setWindowTitle("Image Viewer")												#Title
		self.resize(500, 400)																			#init size

		self.loadNext()																						#Load first img
		
	##############################################################################
	##		LOAD NEXT IMAGE TO VIEW
	##############################################################################
	def loadNext(self):
		fileName = None																						#Null Filename

		if self.IC < len( IL ):																		#If not last img
			fileName = IL[ self.IC ]																#	 grab filename
		else:																											#If last img
			QtGui.QMessageBox.information(self, 										#	 Message user
																		"Image Viewer", 					#
																		"Last image" )						#	
			self.exitAct()																					#	 Exit app
			return																									#  return if fail
	  
		print "#" + str( self.IC ) + "\t" + str(IL[ self.IC ]) 		#Console log msg

		image = QtGui.QImage(fileName)														#Load	as QImage
		if image.isNull():																				#If not loaded
			QtGui.QMessageBox.information(self, 										#  Message user
																		"Image Viewer", 					#
																		"%s, not found" %fileName)#
			return																									#Return
	 
		self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))	#Put image as
																															#	 PixMap in	
																															#	 imageLabel
		self.sizeAdjust( None )																		#Adjust size of
																															#  image

		self.IC = self.IC + 1																			#Inc img count
		

	##############################################################################
	##	Resize imageLabel to fit inside scrollArea
	##			Resized on resizeEvent and on loading next image
	##############################################################################
	def sizeAdjust(self, event):
		r = self.scrollArea.rect()											#Grab scrollArea size 
		self.imageLabel.resize( r.width()-5, 						#Resize image to size-5px
														r.height()-5 )


	##############################################################################
	##	Classify Image as HQ
	##############################################################################
	def clasGood(self):
		self.G.write( IL[ self.IC ] )				#Write filename to good quality file
		self.G.write( "\n" )								#Write EOL
		self.loadNext()											#Load next image in list

	##############################################################################
	## Classify Image as LQ
	##############################################################################
	def clasBad(self):
		self.B.write( IL[ self.IC ] )				#Write filename to bad quality file
		self.B.write( "\n" )								#Write EOL
		self.loadNext()											#Load next image in list

	##############################################################################
	##	Close applicaiton gracefully
	##############################################################################
	def killApp(self):
		self.G.close()											#Close files to store data 
		self.B.close()
		self.close()												#Close the application

	##############################################################################
	##	Create menue actions and shortcuts
	##############################################################################
	def createActions(self):
		self.exitAct = QtGui.QAction(	"E&xit", 										#Exit / close
																	self, 											#self.killApp()
																	shortcut="Ctrl+Q",
																	triggered=self.killApp)

		self.nextAct = QtGui.QAction("&Next image", 							#view next image
																	self, 											#self.loadNext()
																	shortcut="Ctrl+N",
																	triggered=self.loadNext)
				
		self.clasGoodAct = QtGui.QAction("&Classify Good", 				#HQ classification
																	self,												#self.clasGood()
																	shortcut="Ctrl+G", 
																	triggered=self.clasGood)
		
		self.clasBadAct = QtGui.QAction("&Classify Good", 				#LQ classification
																	self,												#self.classBad()
																	shortcut="Ctrl+B", 
																	triggered=self.clasBad)

	##############################################################################
	##	Create menues
	##############################################################################
	def createMenus(self):
		############################################################################
		## Create file menu and add actions to the drop-down menue
		############################################################################
		self.fileMenu = QtGui.QMenu("&File", self)
		
		self.fileMenu.addAction(		self.nextAct				)
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(		self.clasGoodAct		)
		self.fileMenu.addAction(		self.clasBadAct			)
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(		self.exitAct				)

		############################################################################
		## Add main menues to menue bar
		############################################################################
		self.menuBar().addMenu(			self.fileMenu				)


################################################################################
##	Load the application 
################################################################################
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	imageViewer = ImageViewer()
	imageViewer.show()
	sys.exit(app.exec_())
