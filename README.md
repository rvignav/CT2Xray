# CT2Xray

To test the CT to Xray algorithm, run the following:

    git clone https://github.com/rvignav/CT2Xray.git
    cd CT2Xray
    pip install Pillow numpy glob2 regex os-sys argparse matplotlib
    python ct2xray.py path/to/CT/volume path/to/mask/volume

To run the algorithm on the provided sample volumes, a possible command is

    python ct2xray.py volumes/CT masks/CT_Lung_Mask

Note: If `import glob` still raises an error after running the script above, run `npm install glob`.
