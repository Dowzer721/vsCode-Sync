"""
Currently I am saving the original frame to the frames folder, but instead maybe I should just save the grayscale frame to the folder, 
as that will speed up the processing, and it may also make highlighting motion easier.
"""


import cv2
import os
from progressbar import ProgressBar
import shutil

skipFrameDel = False
showFeedback = False

# The name of the video
videoName = "peopleWalkingTimelapse_4s.mp4"

# The location of the video
videoLocation = "C:/Users/Luke/Documents/Learning Python/Computer Vision/Motion Detection/Crowd Mapping/"

# The name of the folder to store the frames of the video within, appended with the GrayScale tag at the end
# frameFolder = videoLocation + str(videoName[:-4]) + "_Frames_GS/"
frameFolder = videoLocation + "Created Frames/" + str(videoName[:-4]) + "_Frames_GRAY/"

# # Create the folder if it doesn't already exist
# if not os.path.exists(frameFolder):
#     os.makedirs(frameFolder)

# If the folder already exists, delete it first. Otherwise create the folder
if os.path.exists(frameFolder) and not skipFrameDel:
    # os.rmdir(frameFolder)
    shutil.rmtree(frameFolder, ignore_errors=True)
    if showFeedback: print("Folder deleted")

if not skipFrameDel:
    os.makedirs(frameFolder)
    if showFeedback: print("Folder created")

videoCap = cv2.VideoCapture(videoLocation + videoName)

videoW = int( videoCap.get(cv2.CAP_PROP_FRAME_WIDTH) )
videoH = int( videoCap.get(cv2.CAP_PROP_FRAME_HEIGHT))
if showFeedback: print(f"Original Video- w:{videoW}, h:{videoH}")

# Could be used for a progress bar
numberOfFrames = int(videoCap.get(cv2.CAP_PROP_FRAME_COUNT))

fileNames = []

if not skipFrameDel:
    if showFeedback: print(f"Creating {numberOfFrames} frames:")
    pBar = ProgressBar()
    for count in pBar(range(numberOfFrames)) if showFeedback else range(numberOfFrames):
        frameName = f"Frame_{count}.jpg"
        framePath = frameFolder + frameName # f"Frame_{count}.jpg"
        
        fileNames.append(frameName)

        _, colourFrame = videoCap.read()
        grayFrame = cv2.cvtColor(colourFrame, cv2.COLOR_BGR2GRAY)
        
        # thresholdMinimum = 170 # 85
        # thresholdMaximum = 255 # 170
        # _, binaryFrame = cv2.threshold(grayFrame, thresholdMinimum, thresholdMaximum, cv2.THRESH_BINARY)

        if not os.path.exists(framePath):
            # cv2.imwrite(framePath, colourFrame)
            cv2.imwrite(framePath, grayFrame)
            # cv2.imwrite(framePath, binaryFrame)

    if showFeedback: print(f"{count + 1} frames successfully captured and converted to GrayScale.")

if showFeedback: print(f"Original pixel count: {videoW * videoH}")

frameResolution = 0.5
grayscaleVideoSize = (int(videoW * frameResolution), int(videoH * frameResolution))
if showFeedback: 
    print(f"Grayscale Video- w:{grayscaleVideoSize[0]}, h:{grayscaleVideoSize[1]}")
    print(f"Grayscale Pixel count: {grayscaleVideoSize[0] * grayscaleVideoSize[1]}")

# Just going to test that the frames can be converted back into a video:

videoNameEnding = "_GRAY"
testVid = cv2.VideoWriter(videoLocation + "Created Videos/" + str(videoName[:-4]) + videoNameEnding + ".avi", cv2.VideoWriter_fourcc(*"DIVX"), 15, grayscaleVideoSize)

# fileNames = sorted(os.listdir(frameFolder))
# fileNames.sort()
# print(fileNames)

for frameNumber in range(numberOfFrames):
    gsFrame = cv2.imread(frameFolder + fileNames[frameNumber])
    gsFrame = cv2.resize(gsFrame, (0,0), fx=frameResolution, fy=frameResolution)
    # height, width, _ = gsFrame.shape
    # size = ...
    testVid.write(gsFrame)
testVid.release()


# allFrames = []
# for name in fileNames[:100]:
#     frame = cv2.imread(frameFolder + name)
#     frame = cv2.resize(frame, (0,0), fx=frameResolution, fy=frameResolution)
#     height, width, _ = frame.shape
#     size = (width, height)
#     allFrames.append(frame)
#     # i = name.index('_')
#     # s = name[i:]
#     # print(s, end=',')

# testVid = cv2.VideoWriter(videoLocation + str(videoName[:-4]) + "_GS.avi", cv2.VideoWriter_fourcc(*"DIVX"), 15, size)

# for vidFrame in allFrames:
#     testVid.write(vidFrame)
# testVid.release()