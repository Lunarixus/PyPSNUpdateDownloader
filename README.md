# PyPSNUpdatePackageDownloader

[![Build Status](https://github.com/Lunarixus/PyPSNUpdateDownloader/actions/workflows/release.yml/badge.svg)](https://github.com/Lunarixus/PyPSNUpdateDownloader/actions/workflows/release.yml)

PyPSNUpdatePackageDownloader is a tool to help users download updates for PS3 titles using the Title ID, these files are saved to .pkg which can be used for RPCS3 etc.  

## Features

- Retrieve update packages by entering the Title ID.
- Download multiple update versions.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Building from Source](#building-from-source)

## Installation

### Pre-built Executables

You can download pre-built executables for Linux, Windows, and macOS from the [releases page](https://github.com/Lunarixus/PyPSNUpdateDownloader/releases).

### Requirements

- Python 3.x
- `pip` (Python package installer)

### Install from Source

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```
    python main.py
    ```

2. Enter the Title ID of the game you wish to download packages for and click "Get Packages".
3. The available packages will be displayed in the list. Double-click a package to select it and choose a save location.

## Building from Source

### Prerequisites

- `pyinstaller`
- `requests`

### Steps

1. Install PyInstaller:

    ```
    pip install pyinstaller
    ```

2. Build the executable:

    ```
    pyinstaller --onefile --noconsole --version-file=version.txt main.py
    ```

3. The executable will be available in the `dist` directory.
