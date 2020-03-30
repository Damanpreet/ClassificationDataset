'''
    Author - Damanpreet Kaur
    Date - 29/03/2020
    Purpose - Split explants in the image and classify them as contaminated/not contaminated.
        input - rgb image directory.
'''

import cv2
import argparse
import numpy as np
from utils import RGBPreprocess, classify
import os
from os import path as osp
from matplotlib import pyplot as plt
from config import config as cfg

INVALID_GRID_TYPE = 'Grid type is Invalid.'

def get_arguments():
    """
        Parse all the command line arguments.
    """
    parser = argparse.ArgumentParser(description="label-components")
    parser.add_argument("--img-dir", type=str, default=cfg.RGB_DIR, help="RGB image directory path.")
    parser.add_argument("--output", default=cfg.OUTPUT, help="Output root directory")
    return parser.parse_args()

def create_dirs(output_dir):
    """
        Function to create output directories
    """
    if not osp.isdir(output_dir):
        os.mkdir(output_dir)
    
    if not osp.isdir(osp.join(output_dir, 'contaminated')):
        os.mkdir(osp.join(output_dir, 'contaminated'))
    
    if not osp.isdir(osp.join(output_dir, 'notcontaminated')):
        os.mkdir(osp.join(output_dir, 'notcontaminated'))


def main():
    print("Reading Arguments: ")
    args = get_arguments()
    print("Output root directory: ", args.output)

    create_dirs(args.output)

    images = []
    for r, d, f in os.walk(args.img_dir):
        for file in f:
            if '.jpg' in file:
                images.append(osp.join(r, file))
    
    print("Image list: ")
    print(images)

    for img in images:
        img = img.split('/')
        img_name = img[-1].strip('.jpg')
        gridtype = int(img[-2])
        image = cv2.cvtColor(cv2.imread('/'.join(img)), cv2.COLOR_BGR2RGB) # read and convert the image to RGB.
        
        print("gridtype: ", gridtype)
        if gridtype == 9:
            crop_dims, gridw, gridh = cfg.CROP_DIMS, cfg.GRIDW, cfg.GRIDH
        else:
            raise ValueError(INVALID_GRID_TYPE)

        # Process the image
        rgb = RGBPreprocess(crop_dims)      
        data = rgb.process_img(image, gridh, gridw)
        for i, im in enumerate(data):
            ret_val = classify(im)
            print(ret_val)

            if ret_val==2:
                img_path = osp.join(args.output, 'contaminated', img_name+'_'+str(i)+'.jpg')
            elif ret_val==1:
                img_path = osp.join(args.output, 'notcontaminated', img_name+'_'+str(i)+'.jpg')
            else:
                continue # do not save this image
            cv2.imwrite(img_path, cv2.cvtColor(im, cv2.COLOR_RGB2BGR))

        # exit()
           
if __name__ == '__main__':
    main()
