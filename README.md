## COVID-19 Lung Lesion Segmentation Using a Sparsely Supervised Mask R-CNN on Chest X-rays Automatically Computed from Volumetric CTs
<a href="https://orcid.org/0000-0002-6521-7898"><img height="30" src="https://github.com/rvignav/rvignav/blob/master/docs/orcid.pdf"></a>&nbsp;&nbsp;Vignav Ramesh, <a href="https://orcid.org/0000-0002-4490-0444"><img height="30" src="https://github.com/rvignav/rvignav/blob/master/docs/orcid.pdf"></a>&nbsp;&nbsp;Blaine Rister, <a href="https://orcid.org/0000-0001-5057-4369"><img height="30" src="https://github.com/rvignav/rvignav/blob/master/docs/orcid.pdf"></a>&nbsp;&nbsp;Daniel L. Rubin

<!-- [arXiv]() / [Full Paper (PDF)]() / [Google Scholar]() / [Papers With Code]() / [Mask R-CNN Code]() -->

![GIF](https://github.com/rvignav/CT2Xray/blob/master/docs/gif.gif)

### Pre-trained models

| Training dataset | Train/test split | Data augmentation (y/n) | URL |
| --- | --- | --- | --- |
| X-rays Only | 60/40 | y | [Download](https://drive.google.com/file/d/1Db0NhVCIBOJJTfDHjtmgm3I10-KsUpg-/view?usp=sharing) |
| Mixed | 60/40 | y | [Download](https://drive.google.com/file/d/1nizSK5_RQXsaQ-omKtKL3dwaLL2xJnfC/view?usp=sharing) |
| X-rays Only | 80/20 | y | [Download](https://drive.google.com/file/d/15TBvC-UUYZ4OB_ExNCewHNrZFXdDCPZR/view?usp=sharing) |
| Mixed | 80/20 | y | [Download](https://drive.google.com/file/d/1cO2ck9sJm79tmW-FvawO_ogIL_4yLFpU/view?usp=sharing) |
| X-rays Only | 80/20 | n | [Download](https://drive.google.com/file/d/1fNQndbTef8bu-OPJZHUio4CtTgQMKKxr/view?usp=sharing) |
| Mixed | 80/20 | n | [Download](https://drive.google.com/file/d/11Bs9XbJNKPXaVzKWydvR6r6j9cOFf5ig/view?usp=sharing) |

### Environment setup

Our models were trained on a single GPU (Tesla P4 GPU provided by Google Colab, 16 GB memory). The code is implemented using TensorFlow v1, but is compatible with TensorFlow v2 and can be ported to the [most recent version of TensorFlow](https://www.tensorflow.org/versions) if desired. To install all required dependencies, run the following:

    pip install Pillow numpy glob2 regex os-sys argparse matplotlib

Afterwards, set up the Mask R-CNN model:
```
git clone --quiet https://github.com/rvignav/Mask_RCNN.git
cd ~/Mask_RCNN
pip install -q PyDrive
pip install -r requirements.txt
python setup.py install
cp ~/Mask_RCNN/samples/balloon/balloon.py ./lesion.py
sed -i -- 's/balloon/lesion/g' lesion.py
sed -i -- 's/Balloon/Lesion/g' lesion.py
```

### Data

| Dataset | URL |
| --- | --- |
| Training Dataset 1 (X-rays Only) | [Download](https://github.com/rvignav/CT2Xray/tree/master/xrays_only) |
| Training Dataset 2 (Mixed) | [Download](https://github.com/rvignav/CT2Xray/tree/master/mixed) |
| Test Dataset | [Download](https://github.com/rvignav/CT2Xray/tree/master/mixed/val) |

### Pretraining

The following command can be used to pretrain a Mask R-CNN on either Dataset 1 or 2 (which reflects the default hyperparameters in our paper):
```
# Train a new model starting from pre-trained ImageNet weights
python lesion.py train --dataset='/path/to/data/' --weights=imagenet

# Train a new model starting from pre-trained COCO weights
python lesion.py train --dataset='/path/to/data/' --weights=coco

# Continue training a model that you had trained earlier
python lesion.py train --dataset='/path/to/data/' --weights=/path/to/weights/

# Continue training the last model you trained. This will find
# the last trained weights in the model directory.
python lesion.py train --dataset='/path/to/data/' --weights=last
```

To train with data augmentation, run:

    python lesion.py train --dataset='/path/to/data/' --weights=imagenet/coco/last --aug='y'

Alternatively, use the following Colabs to train the models:

X-rays only: <a href="https://colab.research.google.com/github/rvignav/CT2Xray/blob/master/Segment_Xrays_Only.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

Mixed: <a href="https://colab.research.google.com/github/rvignav/CT2Xray/blob/master/Segment_Mixed.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

The CT to X-ray re-projection algorithm can be executed in isolation as follows:

    python ct2xray.py <path/to/CT/volume> <path/to/mask/volume>

<!-- ### Cite
```
@article{chen2020big,
  title={Big Self-Supervised Models are Strong Semi-Supervised Learners},
  author={Chen, Ting and Kornblith, Simon and Swersky, Kevin and Norouzi, Mohammad and Hinton, Geoffrey},
  journal={arXiv preprint arXiv:2006.10029},
  year={2020}
}
``` -->
