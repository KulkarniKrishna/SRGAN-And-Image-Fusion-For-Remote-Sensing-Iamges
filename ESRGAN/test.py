import os.path as osp
import glob
from typing import Tuple
import cv2
import numpy as np
import torch
import RRDBNet_arch as arch
import os
from PIL import Image


# Set the input and output folder paths
input_folder = "LR"
output_folder = "DS"
target_size= (1260,1260)

# Loop through all the files in the input folder
for filename in os.listdir(input_folder):
    # Check if the file is a jp2 image
    if filename.endswith(".jp2"):
        # Open the jp2 image
        with Image.open(os.path.join(input_folder, filename)) as im:
            # Convert the image to RGB if it's not already in that format
            im = im.convert("RGB")
            print(im.size)
            # Save the image as a png file with no compression in the output folder
            im = im.resize(target_size, resample=Image.LANCZOS)
            im.save(os.path.join(output_folder, os.path.splitext(filename)[0] + ".png"), format="PNG", compress_level=0)
            print(im.size)
            im=""


model_path = 'models/RRDB_PSNR_x4.pth'  # models/RRDB_ESRGAN_x4.pth OR models/RRDB_PSNR_x4.pth
device = torch.device('cuda')  # if you want to run on CPU, change 'cuda' -> cpu
# device = torch.device('cpu')

test_img_folder = 'DS/*'

model = arch.RRDBNet(3, 3, 64, 23, gc=32)
model.load_state_dict(torch.load(model_path), strict=True)
model.eval()
model = model.to(device)

print('Model path {:s}. \nTesting...'.format(model_path))

idx = 0
for path in glob.glob(test_img_folder):
    idx += 1
    base = osp.splitext(osp.basename(path))[0]
    print(idx, base)
    # read images
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img1 = cv2.imread(path, cv2.IMREAD_COLOR)
    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)

    with torch.no_grad():
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round()
    cv2.imwrite('results/{:s}_rlt.png'.format(base), output)
    #Calculating PSNR for original image and ESRGAN output image
    resop = cv2.imread('results/{:s}_rlt.png'.format(base))
    resolution = tuple(resop.shape[:2])
    im_resized = cv2.resize(img1, resolution, interpolation=cv2.INTER_LANCZOS4)
    psnr = cv2.PSNR(im_resized,cv2.imread(path))
    print(f"PSNR value: {psnr:.2f}")
