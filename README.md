# CT2Xray

Automatic conversion from CT and mask volumes of axial slices to an annotated coronal X-ray. Segments COVID-19 lung lesions on those X-rays via a custom Mask-RCNN.

To perform chest X-ray COVID-19 lung lesion segmentation or test the Mask-RCNN, open and run [`Segment.ipynb`](https://github.com/rvignav/CT2Xray/blob/master/Segment.ipynb) or [`Inference.ipynb`](https://github.com/rvignav/CT2Xray/blob/master/Inference.ipynb), respectively.

To test the CT to X-ray algorithm, run the following:

    git clone https://github.com/rvignav/CT2Xray.git
    cd CT2Xray
    pip install Pillow numpy glob2 regex os-sys argparse matplotlib
    python ct2xray.py path/to/CT/volume path/to/mask/volume

Note: If `import glob` still raises an error after running the script above, run `npm install glob`.
