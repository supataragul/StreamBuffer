"""
Created on Sun Apr 06 2019

@author: Chayatorn Supataragul
"""
# OpenCV Python script to buffer the video stream

# import libraries of python OpenCV as cv2
import cv2
import sys
import threading
import queue

# == Start Initialization ==
frame_buffer_size = 5 # The queue size for keeping video frame for processing. Cannot less than 2

# Capture frames from the ip camera
fn = "rtsp://192.168.1.21:554/1"

# Set capture device from fn
cap = cv2.VideoCapture(fn)

# The queue for keeping video frame for processing
frame_buffer = queue.Queue(maxsize=frame_buffer_size)

# == End Initialization ==

# De-allocate any associated memory usage and exit the program
def deallocateAndExit():
    # De-allocate any associated memory usage
    cap.release()# release camera
    cv2.destroyAllWindows()# release screen
    sys.exit() # exit program

# This is a thread function to keep reading frames and put the frames into frame_buffer for preventing lag of frames reading.
def rtsp_read_buffer():
    # ret will be False when cap.read() timeout or error
    ret = True
    while (ret):
        # If frame_buffer queue is full, get the first queue element out of the queue
        if frame_buffer.full():
            frame_buffer.get()
        # Read frame-by-frame
        # capturing each frame
        ret, buffer_frame = cap.read()
        # Put the capturing frame to the queue
        frame_buffer.put(buffer_frame)
    # Exit program
    deallocateAndExit()


# Main function to start the program
def main():

    # Start thead functions to continue their task parallelly
    threading.Thread(target=rtsp_read_buffer, daemon=True).start()
    
    # Check cv2.VideoCapture(fn) is open
    while (cap.isOpened()):

        # Check if frame_buffer queue has frames waiting to process or not
        # If some processes are waiting, let calculate it
        if frame_buffer.empty() != True:

            # Get a frame from the frame_buffer queue
            frame = frame_buffer.get()

            frame_out = frame.copy()# output frame

            # Display video
            cv2.imshow('Frame out', frame_out)# display each frame

            # Terminate program
            if cv2.waitKey(33) == ord('q') or cv2.waitKey(33) == 27:# if user click key 'q', program will be closed
                break
    # End while loop

    # Exit program
    deallocateAndExit()

# start process
if __name__ == '__main__':
    main()