# -*- coding: utf-8 -*-
"""Copy of Copy of Copy of YOLOv5 Classification Tutorial.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CKrfCgBzbGtZx3nXBnw5ib6wY0aBuNh-

## YOLOv5 Classification Tutorial

YOLOv5 supports classification tasks too. This is the official YOLOv5 classification notebook tutorial. YOLOv5 is maintained by [Ultralytics](https://github.com/ultralytics/yolov5).

This notebook covers:

*   Inference with out-of-the-box YOLOv5 classification on ImageNet
*  [Training YOLOv5 classification](https://blog.roboflow.com//train-YOLOv5-classification-custom-data) on custom data

*Looking for custom data? Explore over 66M community datasets on [Roboflow Universe](https://universe.roboflow.com).*

This notebook was created with Google Colab. [Click here](https://colab.research.google.com/drive/1FiSNz9f_nT8aFtDEU3iDAQKlPT8SCVni?usp=sharing) to run it.

# Setup

Pull in respective libraries to prepare the notebook environment.
"""

# Commented out IPython magic to ensure Python compatibility.
!git clone https://github.com/ultralytics/yolov5  # clone
# %cd yolov5
# %pip install -qr requirements.txt  # install

import torch
import utils
display = utils.notebook_init()  # checks

!git clone https://github.com/DarvinX/trash_classifier.git

"""# 1. Infer on ImageNet

To demonstrate YOLOv5 classification, we'll leverage an already trained model. In this case, we'll download the ImageNet trained models pretrained on ImageNet using YOLOv5 Utils.
"""

!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="uM1ttr0IhxTTi37lvExZ")
project = rf.workspace("bug-bite").project("bug-bite-single")
dataset = project.version(19).download("folder")

from utils.downloads import attempt_download

p5 = ['n', 's', 'm', 'l', 'x']  # P5 models
cls = [f'{x}-cls' for x in p5]  # classification models

for x in cls:
    attempt_download(f'weights/yolov5{x}.pt')

"""Now, we can infer on an example image from the ImageNet dataset.

### Train On Custom Data 🎉
Here, we use the DATASET_NAME environment variable to pass our dataset to the `--data` parameter.

Note: we're training for 100 epochs here. We're also starting training from the pretrained weights. Larger datasets will likely benefit from longer training.
"""

!python classify/train.py --model yolov5n-cls.pt --data {dataset.location} --epochs 2000 --batch 100 --img 224 --pretrained weights/yolov5s-cls.pt

"""### Validate Your Custom Model

Repeat step 2 from above to test and validate your custom model.
"""

!python classify/val.py --weights runs/train-cls/exp7/weights/best.pt --data {dataset.location}

!tensorboard --logdir=runs/train-cls/exp4

!ls runs/val-cls/exp

import os

"""### Infer With Your Custom Model"""

#Get the path of an image from the test or validation set
if os.path.exists(os.path.join(dataset.location, "test")):
  split_path = os.path.join(dataset.location, "test")
else:
  split_path = os.path.join(dataset.location, "val")
example_class = os.listdir(split_path)[0]
example_image_name = os.listdir(os.path.join(split_path, example_class))[0]
example_image_path = os.path.join(split_path, example_class, example_image_name)
os.environ["TEST_IMAGE_PATH"] = example_image_path

print(f"Inferring on an example of the class '{example_class}'")

#Infe
!python classify/predict.py --weights runs/train-cls/exp4/weights/best.pt --source /content/drive/MyDrive/IMG-20200222-WA0052.jpg

!python classify/predict.py --weights runs/train-cls/exp4/weights/best.pt --source /content/drive/MyDrive/image1.jpg

"""We can see the inference results show ~3ms inference and the respective classes predicted probabilities."""