# CT2Xray

To test the CT to Xray algorithm, run the following:

    git clone https://github.com/rvignav/CT2Xray.git
    cd CT2Xray
    pip install Pillow numpy glob2 regex os-sys argparse matplotlib
    python ct2xray.py path/to/CT/volume path/to/mask/volume

Note: If `import glob` still raises an error after running the script above, run `npm install glob`.
