# YouTube Downloader Python

This is a Python script that allows you to download videos and audio from YouTube using the `pytube` library. It provides a command-line interface (CLI) to interact with the script and easily download YouTube content.

## Features

- Download videos or audio from YouTube.
- Specify the video quality or format for downloading.
- Supports downloading entire playlists or individual videos.
- Concurrent downloads for faster performance.
- Progress bar to track the download progress.

## Installation

1. Clone or download the repository:

```bash
git clone https://github.com/dtsuper3/yt-downloader-python.git
```

2. Navigate to the project directory:

```bash
cd yt-downloader-python
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To download a video or audio from YouTube, run the following command:

```bash
python yt_downloader.py <URL>
```

Replace `<URL>` with the YouTube video URL you want to download.

Optional arguments:

- `-q, --quality`: Specify the video quality. Available options are `highest`, `lowest`, `hd720`, `medium`, `small`, `audio`. Default is `highest`.
- `-f, --format`: Specify the video format. Available options are `mp4` and `webm`. Default is `mp4`.
- `-p, --playlist`: Specify this flag if you want to download an entire playlist instead of a single video.

Examples:

- Download a single video in the highest quality available:

```bash
python yt_downloader.py https://www.youtube.com/watch?v=VIDEO_ID
```

- Download a video in a specific format (e.g., webm):

```bash
python yt_downloader.py -f webm https://www.youtube.com/watch?v=VIDEO_ID
```

- Download an entire playlist:

```bash
python yt_downloader.py -p https://www.youtube.com/playlist?list=PLAYLIST_ID
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

When contributing to this project, please ensure that your changes are well-documented and follow the existing coding style.

## License

This project is licensed under the [MIT License](https://github.com/dtsuper3/yt-downloader-python/blob/main/LICENSE).
