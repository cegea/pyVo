# pyVo - Stream Recorder

This application allows you to schedule and record multiple streams defined in a streams.json file. It handles start and end times, reconnects if the connection is lost during recording, and saves recordings to specified output files.

## Prerequisites
1. Install Python

Ensure you have Python 3.8+ installed on your system. You can download it from python.org.

2. Install MPV

MPV is the media player used for recording streams. Follow the installation instructions for your platform:

### Windows
- Download the latest MPV release from mpv.io.
- Extract the downloaded archive.
- Add the mpv.exe path to your system's environment variables to make it accessible from the terminal.

### Mac
Install Homebrew if not already installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install MPV via Homebrew:
```bash
brew install mpv
```

### Linux: Install MPV via your package manager. For example:
```bash
sudo apt install mpv
```

## Setup Instructions

### Clone the Repository:

```bash
git clone https://github.com/cegea/pyVo.git
cd pyVo
```

### Create a Virtual Environment:

```bash
python -m venv venv
```

### Activate the Virtual Environment:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies:

```bash
pip install -r requirements.txt
```

## Configuring streams.json

The streams.json file defines the streams to record. Each entry should look like this:
```json
[
    {
        "id": "a3f11cbe2d144dfe8a8927b4ca5195cc55fb45ab",
        "start_time": "2024-11-15T10:00:00",
        "end_time": "2024-11-15T10:30:00",
        "output_file": "stream1.ts"
    },
    {
        "id": "7f8ad9d2c8c3a4f96754321de459b7ab8132ef56",
        "start_time": "2024-11-15T19:25:00",
        "end_time": "2024-11-15T20:30:00",
        "output_file": "stream2.ts"
    }
]
```

Parameters:

- id: The unique identifier for the stream (e.g., a hash value).
- start_time: The scheduled start time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS).
- end_time: The scheduled end time in ISO 8601 format.
- output_file: The name of the file where the recording will be saved.

## Running the Application

Activate the virtual environment (if not already active):

Windows

```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

Run the application:

```bash
python main.py
```

## Logs

The application logs all activities to recording.log. Check this file for detailed traces of the recording process.