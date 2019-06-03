#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import sys
import cv2
import argparse

class Camera:
    def __init__(self, device_idx=0):
        "Wraps video capture device with index device_idx."
        self.vc = cv2.VideoCapture(device_idx)
        self.vc.set(3, 1920)
        self.vc.set(4, 1080)
        self.is_closed = False

    def get_frame(self):
        "Returns a frame from the camera as a numpy.ndarray"
        if self.is_closed:
            raise RuntimeError("Cannot retrieve frame from closed camera")
        ret, frame = self.vc.read()
        if ret==False:
            raise RuntimeError("Camera failed")
        return frame

    def close(self):
        "Releases the camera."
        self.vc.release()
        self.is_closed = True

    def __repr__(self):
        return "<Camera %x>" % id(self)

def main(argv):
    parser = argparse.ArgumentParser(description='Capture frame or frames from camera.')
    parser.add_argument('devidx', metavar='idx', type=int, nargs='?',
                        help='Device index', default=0)
    parser.add_argument('--paused', action='store_true',
                        help='Capture a single frame and freeze')
    parser.add_argument('--screenshot-prefix', metavar='prefix', type=str, nargs='?',
                        help='Screenshot prefix', default='opencv-')
    args = parser.parse_args()

    try:
        cam = Camera(args.devidx)
        frame = cam.get_frame()
        print(args)
        cv2.imshow('frame',frame)

        paused = args.paused
        while(True):
            if not paused:
                frame = cam.get_frame()
                cv2.imshow('frame',frame)

            key = cv2.waitKey(1) & 0xFF
            if key in {ord('q'), 99}: # quit
                break
            if key in {ord('p'), 32}: # play/pause recording
                paused = not paused
            if key in {ord('s')}: # screenshot
                timestamp = datetime.datetime.now().strftime('%Yy%mm%dd%Hh%Mm%Ss%fms')
                cv2.imwrite('%s%s.jpg'%(args.screenshot_prefix, timestamp), frame)
    finally:
        cam.close()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
