# CT2Xray

To test the CT to Xray algorithm, run the following:

    git clone https://github.com/rvignav/CT2Xray.git
    cd CT2Xray
    pip install Pillow numpy glob2 regex os-sys argparse
    python main.py CT

To use a custom CT volume, replace `CT` in the above command with the absolute or relative path to the directory containing the data.

Note: If `import glob` still raises an error after running the script above, run `npm install glob`.
