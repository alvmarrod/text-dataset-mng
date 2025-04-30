# text-dataset-mng

<p align="center">
  <img alt="GitHub Tag" src="https://img.shields.io/github/v/tag/alvmarrod/text-dataset-mng">
  <img alt="Python" src="https://img.shields.io/badge/python-3.13-blue">
  <img alt="GitHub License" src="https://img.shields.io/github/license/alvmarrod/text-dataset-mng">
</p>

## Overview

A Python-Flask based web application for managing text datasets. This tool provides a simple interface to create, modify, and access text datasets for NLP and machine learning projects.

## Features

- Create and manage multiple text datasets
- Add, edit, and delete text samples
- Apply labels to samples
- Intuitive form-based web interface

### Roadmap

- Export datasets in various formats (JSON, CSV, TXT)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Start the web server:

```bash
python app.py
```

The web application will be available at `http://localhost:5000`

## Application Routes

### Datasets

- `GET /` - List all datasets
- `POST /` - Create a new dataset
- `GET /dataset/view/{id}` - View dataset details
- `GET /dataset/update/{id}` - View form to update a dataset
- `POST /dataset/update/{id}` - Update a dataset
- `GET /dataset/delete/{id}` - Delete a dataset

### Samples

- `POST /sample/create` - Create a new sample
- `GET /sample/update/{id}` - View form to update a sample
- `POST /sample/update/{id}` - Update a sample
- `GET /sample/delete/{id}` - Delete a sample

## Browser Usage

1. Access `http://localhost:5000` in your browser
2. Use the web forms to create and manage your datasets and samples
3. Navigate between different sections using the provided links

## License

MIT License.
