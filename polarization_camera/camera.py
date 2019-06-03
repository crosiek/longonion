#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import sys
import cv2
import argparse
import threading
import itertools

class Camera:
    def __init__(self, device=0):
        "Wrap video capture device."
        self.vc = cv2.VideoCapture(device)
        self.vc.set(3, 640)
        self.vc.set(4, 480)
        self.is_closed = False
        self.buffer = self.get_frame()

    def get_frame(self):
        "Return a frame from the camera as a numpy.ndarray"
        if self.is_closed:
            raise RuntimeError("Cannot retrieve frame from closed camera")
        ret, frame = self.vc.read()
        if ret==False:
            raise RuntimeError("Camera failed")
        return frame

    def update_buffer(self):
        self.buffer = self.get_frame()

    def close(self):
        "Release the camera."
        self.vc.release()
        self.is_closed = True

    def __repr__(self):
        return "<Camera %x>" % id(self)


def main(argv):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('devices', metavar='dev', type=str, nargs='+',
                        help='Device path or index', default=())
    parser.add_argument('--paused', action='store_true',
                        help='Capture a single frame and freeze')
    parser.add_argument('--screenshot-prefix', metavar='prefix', type=str, nargs='?',
                        help='Screenshot prefix', default='opencv-')
    args = parser.parse_args()

    try:
        cameras = [Camera(d) for d in args.devices]
        # Alternate implementation:
        # camera_threads = [threading.Thread(target=lambda c=c:
        #                                    list(itertools.dropwhile(
        #                                        lambda _: True,
        #                                        (c.update_buffer() for _ in itertools.count())))).start()
        #                   for c in cameras]
        for c in cameras:
            def t(c=c):
                while True:
                    try:
                        c.update_buffer()
                    except RuntimeError:
                        break
            threading.Thread(target=t).start()

        current_idx = 0
        paused = args.paused
        frame = cameras[current_idx].get_frame()
        for i, c in enumerate(cameras):
            cv2.imshow(f'frame{i}', c.buffer)
        while(True):
            if not paused:
                frame = cameras[current_idx].buffer
                for i, c in enumerate(cameras):
                    cv2.imshow(f'frame{i}', c.buffer)
                c1, c2, *rest = cameras
                cv2.imshow(f'diff', c1.buffer//2 - c2.buffer//2 + 128)
            key = cv2.waitKey(1) & 0xFF
            if key in {ord('q'), 99}: # quit
                break
            if key in {ord('p'), 32}: # play/pause recording
                paused = not paused
            if key in {ord('s')}: # screenshot
                timestamp = datetime.datetime.now().strftime('%Yy%mm%dd%Hh%Mm%Ss%fms')
                cv2.imwrite('%s%s.jpg'%(args.screenshot_prefix, timestamp), frame)
            if key == 81: # left
                current_idx = (current_idx-1)%len(cameras)
            if key == 83: # right
                current_idx = (current_idx+1)%len(cameras)
    finally:
        es = []
        for c in cameras:
            try:
                c.close()
            except e:
                es.append(e)
        cv2.destroyAllWindows()
        if es:
            print(f'Camera.close() raised {len(es)} exceptions')

if __name__ == '__main__':
    main(sys.argv)
