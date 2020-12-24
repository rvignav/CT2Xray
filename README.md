# CT2Xray

Automatic conversion from CT and mask volumes of axial slices to an annotated coronal X-ray. Segments COVID-19 lung lesions on those X-rays via a custom [Mask-RCNN](https://github.com/rvignav/Mask_RCNN).

To perform chest X-ray COVID-19 lung lesion segmentation, open and run [`Segment_Mixed.ipynb`](https://github.com/rvignav/CT2Xray/blob/master/Segment_Mixed.ipynb) or [`Segment_Xrays_Only.ipynb`](https://github.com/rvignav/CT2Xray/blob/master/Segment_Xrays_Only.ipynb).

To test the CT to X-ray algorithm, run the following:

    git clone https://github.com/rvignav/CT2Xray.git
    cd CT2Xray
    pip install Pillow numpy glob2 regex os-sys argparse matplotlib
    python ct2xray.py path/to/CT/volume path/to/mask/volume

<!-- Note: If `import glob` still raises an error after running the script above, run `npm install glob`. -->
