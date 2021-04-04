# CT2Xray

This repository contains the code for the following algorithms:
1. A pixel-based algorithm that computes a coronal X-ray projection (with overlaid segmentations) from an annotated CT volume.
2. An automated Mask-RCNN architecture for the segmentation of COVID-19 lung lesions on chest X-rays.

To test the CT to X-ray conversion algorithm, run the following:

    git clone https://github.com/rvignav/CT2Xray.git
    cd CT2Xray
    pip install Pillow numpy glob2 regex os-sys argparse matplotlib
    python ct2xray.py <path/to/CT/volume> <path/to/mask/volume>

To perform COVID-19 lung lesion segmentation on chest X-rays, open and run [`Segment_Mixed.ipynb`](https://github.com/rvignav/CT2Xray/blob/master/Segment_Mixed.ipynb) or [`Segment_Xrays_Only.ipynb`](https://github.com/rvignav/CT2Xray/blob/master/Segment_Xrays_Only.ipynb).

For further details, see the below description of the structure of this folder:
```
.
├── Mask_RCNN: Implementation of the Mask-RCNN network architecture.
├── Segment_Xrays_Only.ipynb: Performs COVID-19 lung lesion segmentation on Dataset 1 (X-rays Only).
├── Segment_Mixed.ipynb: Performs COVID-19 lung lesion segmentation on Dataset 2 (Mixed).
├── ct2xray.py: CT to X-ray conversion algorithm.
├── data
│   └── README.md: Download link for all CT and mask volumes.
├── general_blockchain: Various tools for visualizing and manipulating the General Blockchain Inc. test dataset, e.g. computing DICE and IOU scores, visualizing images with overlaid ground truth annotations, generating Normal probability plots and confidence intervals, etc.
├── lesion
│   └── README.md: Download link for all saved model weights (H5 format).
├── mixed
│   ├── train: Mixed training dataset.
│   └── val: Mixed validation dataset.
├── tests
│   ├── ground_truth_masks: Ground truth masks for test images.
│   ├── mixed_masks: Masks predicted by Segment_Mixed.ipynb.
│   ├── xrays_only_masks: Masks predicted by Segment_Xrays_Only.ipynb.
│   └── baseline: Images, notebooks, and other resources for training the baseline model (Tang et al.'s U-Net segmentation model) on Datasets 1 and 2.
├── util: Various tools for converting and manipulating images, e.g. DICOM to PNG conversion, ConcaveHull implementation, etc.
└── xrays_only
    ├── train: X-rays only training dataset.
    └── val: X-rays only validation dataset.
```
