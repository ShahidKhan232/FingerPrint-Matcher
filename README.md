
# FingerPrint Matcher

A Python-based fingerprint matching application with an interactive GUI built using `Tkinter`. The application leverages OpenCV's SIFT (Scale-Invariant Feature Transform) algorithm to match fingerprint images from a provided sample against a dataset of real fingerprints. It provides visual feedback of the best match along with the matching score.

## Features

- **Load Sample Image**: Users can select a sample fingerprint image in `.BMP` format.
- **Real-time Matching**: The application processes and compares the sample fingerprint against all images in a dataset and displays the best match.
- **Progress Tracking**: A loading spinner and progress bar help track the processing of images.
- **Best Match Visualization**: The matched fingerprint is displayed alongside the sample image with keypoints highlighted.

## Technologies Used

- **Python**: The core programming language.
- **Tkinter**: For building the graphical user interface.
- **OpenCV**: For image processing and fingerprint matching using SIFT.
- **Pillow (PIL)**: For image handling in the GUI.

## Requirements

Before running the application, make sure you have the following libraries installed:

1. **OpenCV** (`cv2`)
2. **Tkinter** (comes pre-installed with Python)
3. **Pillow** (`PIL`)

You can install the dependencies using `pip`:

```bash
pip install opencv-python-headless pillow
```

## Dataset

The fingerprint dataset used in this project is the **SOCOFing** dataset. It includes real and altered fingerprint images. For demonstration purposes, the sample fingerprint is compared against images in the `Real` folder.

Place the dataset in the following structure:
Link:
```
https://www.kaggle.com/datasets/ruizgara/socofing
```

> Ensure the `Real` folder contains fingerprint images in `.BMP` format.

## How to Use

1. Clone this repository:

```bash
git clone https://github.com/ShahidKhan232/fingerprint-matching.git

```

2. Ensure the **SOCOFing** dataset is correctly placed under the `archive/SOCOFing/Real` directory.
3. Run the application:

```bash
python main.py
```

4. In the GUI:
   - **Load a sample image** by clicking on the `Load Sample Image` button.
   - After loading, click the `Match Fingerprints` button to start the matching process.
   - The best match will be displayed on the screen, and the score will be shown in a message box.

## GUI Overview

- **Load Sample Image**: Opens a file dialog to load a fingerprint sample for matching.
- **Match Fingerprints**: Starts the matching process, comparing the sample against the dataset.
- **Progress Bar & Status**: Shows the progress of the image processing in real time.

## Screenshots

### Main Interface

![Main Interface](https://github.com/user-attachments/assets/9ee46ff5-ffa2-44ee-ae83-07baf3fea465)
)

### Matching in Progress

![Matching in Progress](https://github.com/user-attachments/assets/33cceda6-0f13-4acc-a06d-f6cc94299559)
)

### Best Match Result

![Match Result]()![output](https://github.com/user-attachments/assets/5e7500c2-f08e-4944-a23d-45e1b3885266)


## Project Structure

```bash
.
├── archive/
│   └── SOCOFing/
│       └── Real/                  # Place the dataset here
├── main.py                        # The main application code
└── README.md                      # Project documentation
```

## Future Enhancements

- Add support for additional matching algorithms.
- Provide more flexibility in image formats for the dataset.
- Include options to adjust SIFT parameters via the GUI.
- Implement threshold tuning for match accuracy.
