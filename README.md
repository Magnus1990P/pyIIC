# pyIIC
Python Iris Image Classification (pyIIC) is a Python and QT4 application for manual classification of images.

#Description
pyIIC makes manual classification of images easy and faster. Create a list of the images file names and provide it to pyIIC when running the command.
Since this is primarily based for iris images, in the future it will incorporate a better GUI with buttons for classification and more fields for loading OSIRIS generated images with segmentation masks.

#pyIIC detailed info
1. Start pyIIC using  the command "./imageviewer.py path_to_image_file_list"
2. pyIIC loads the provided list of files
3. pyIIC loads the next file into the viewer and resizes it to fit the area.
4. User classify the image as "good" or "bad". (good: ctrl+G or bad: ctrl+B, alternatively use the menu)
5. pyIIC writes the filename to the respective output file ("image_G.txt" or "image_B.txt")
6. pyIIC repeats step 3-5 until last image is loaded
7. When loading "the next image" after "the last image" results in the application giving and message and quitting.

