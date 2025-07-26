# Text Extractor

Text Extractor is a simple Python script that uses Optical Character Recognition (OCR) to extract text from image files and save it to a `.txt` file. It leverages the Tesseract OCR engine and works with common image formats such as PNG, JPEG, and BMP.

## Features

- Extracts readable text from images using Tesseract OCR
- Supports PNG, JPG, JPEG, and BMP formats
- Saves output to a plain text file
- Runs on macOS, Windows, and Linux

## Installation

1. Clone this repository:

```bash
git clone https://github.com/Jakeyar/text-extractor.git
cd text-extractor
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR:

- macOS (Homebrew):

```bash
brew install tesseract
```

- Windows:  
[Download the Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki) and ensure it is added to your system's PATH.

- Ubuntu/Debian:

```bash
sudo apt install tesseract-ocr
```

## Usage

Run the script from the command line:

```bash
python TextExtractor.py
```

You will be prompted to enter the name of the image file. The script will display the extracted text and give you the option to save it to a file.

## Example

**Input image:**  
(Place an example image in the `example/` folder)

**Output (`output.txt`):**
```
This is a sample image.
The OCR engine extracted this text successfully.
```

## Requirements

- Python 3.7 or later
- pytesseract
- Pillow (PIL)
- Tesseract OCR (must be installed separately)

See `requirements.txt` for exact Python packages.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Author

Created by [Jakeyar](https://github.com/Jakeyar)
