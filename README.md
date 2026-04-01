# Understanding TensorFlow with Image Detection

This repository documents a Binary CNN classifier: **person** vs **no person**, with **PyTorch** and **Jupyter Notebooks**.

---

## Goal

To understand how image classification and object detection work under the hood by:

- Gathering and preparing a dataset
- Building and training a Binary CNN classifier
- Experimenting with model architecture and loss curves

---

## Start

### 1. Clone the repo
```bash
git clone https://github.com/cjvillar/tf-image-train-workbook.git
cd tf-image-train-workbook
```

### 2. Set up the environment
```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the notebook

If first time:
```bash
source env/bin/activate   # or .\env\Scripts\activate
pip install notebook ipykernel
python -m ipykernel install --user --name=env --display-name "Python (env)"
code .       # launch VS Code
```

Open the Jupyter Notebook and follow the steps:
```bash
jupyter notebook tf_image.ipynb
```

---

## Project Structure

```text
.
├── image_scrape_code/       # Scripts for collecting images
├── tf_image.ipynb           # Main training and experimentation notebook
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## Learning Resources

These helped shape the content and concepts in this project:

- [Build a Deep CNN Image Classifier in TensorFlow](https://youtu.be/jztwpsIzEGc?feature=shared)
- [Building an Object Detector (Medium)](https://medium.com/nerd-for-tech/building-an-object-detector-in-tensorflow-using-bounding-box-regression-2bc13992973f)
- [DigitalSreeni: Object Detection Series](https://youtu.be/JhQqquVeCE0?feature=shared)
- [Interpreting Loss Curves](https://developers.google.com/machine-learning/testing-debugging/metrics/interpretic)
- [Effect of Batch Size on Training Dynamics](https://medium.com/mini-distill/effect-of-batch-size-on-training-dynamics-21c14f7a716e)

---

# Get Training Images:

## 1. Install dependencies (only needed once)
npm install

## 2. Run the script
node ScreenShot.js


## 3. Label

pip install opencv-python
python label_images.py

python label_images.py --input .\image_scrape_code\screenshots --crop 15 68 843 462

## Screenshot/Video Sources for Dataset (YouTube)
~Check for quality as YouTube does not like automation when used to scape data

Visual data used for scraping or reference:

1. [Source 1](https://youtu.be/7XNOJoE6Utg?feature=shared)
2. [Source 2](https://youtu.be/SB0rNXOgY6I?feature=shared)
3. [Source 3](https://youtu.be/RgdMryWc7X0?feature=shared)
4. [Source 4](https://youtu.be/PBYoPqlxuh0?feature=shared)
5. [No people] [Source 5](https://youtu.be/WK4tNpULpd8?feature=shared&t=975)
6. [No people] [Source 6](https://youtu.be/D_QiMn4d9GA?feature=shared)

---

## Contributions

This project is purely educational and self-directed. Feel free to fork it or open an issue if you'd like to collaborate, suggest improvements, or ask questions.