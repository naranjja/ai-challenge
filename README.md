Install the virtual environment library:

`pip3 install virtualenv`

Activate the environment:
- `source env/bin/activate` (Linux)
- `env\Scripts\activate.bat` (Windows)

Install requirements:

`pip3 install -r requirements.txt`

Download pretrained FaceNet models from [here](https://drive.google.com/file/d/1R77HmFADxe87GmoLwzfgMu_HY0IhcyBz/view) and unzip file to `pre_model` folder.

Download pretrained Yolo models from [here](https://drive.google.com/uc?id=1Q9WhhRlqQbA4jgBkCDrynvgquRXZA_f8&export=download) and [here](https://drive.google.com/uc?id=1wg4q9cc6q04oRr_Xaf9GVhhbTSH4-ena&export=download) and place them in the `HeadDetector` folder.

Install tkinter:

`sudo apt-get install python3-tk`