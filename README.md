# Text Extractor

Text Extractor is a Flask web application that allows users to upload images and extract text content from them. It utilizes optical character recognition (OCR) to analyze the uploaded images and extract any text present in them. Additionally, it provides basic image segmentation functionality to isolate individual visual elements within the uploaded images.

## Features

- Upload images: Users can upload images containing text content.
- Text extraction: The application utilizes optical character recognition (OCR) to extract text from uploaded images.
- Image segmentation: Basic image segmentation techniques are employed to potentially isolate individual visual elements within the uploaded images.

## Installation

1. Clone the repository to your local machine:
git clone https://github.com/your_username/text-extractor.git

2. Navigate to the project directory:
cd text-extractor

3. Install the required Python packages using pip:
pip install -r requirements.txt

4. Set up the Google Cloud Vision API:

   - You need to obtain credentials for the Google Cloud Vision API and set up the environment variable `GOOGLE_APPLICATION_CREDENTIALS` with the path to your JSON key file.

## Usage

1. Run the Flask application:
python main.py

2. Access the application in your web browser at `http://localhost:5000`.
3. Upload an image containing text content.
4. View the extracted text and segmented visual elements in the output.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/improvement`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/improvement`).
6. Create a new pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



