# Youtube Hatespeech research

All notable changes to this research, starting from 22 of july 2018, will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)


## v0.2 - 2018-08-15

### Added
- YouTube api call to collect all comments (not reply to comments) from videoId
- script to collect all comments from all database videos

## v0.1 - 2018-07-30

### Added
- Changelog file
- Scripts to read list of medias from mediabiasfactcheck.com and their biases
- Requirements.txt
- Dir data with a list of medias and its' biases
- Class to handle youtube v3 api requests
- Script crawling/youtube/find_media_in_youtube.py to consult channels in youtube and write it's statistics
- youtube_api now collect channel info
- find_media_in_youtube.py now looks for media in youtube and collect the top channel recommendation
- General scripts directory
- Script to filter the most popular channels (+100.000 subscribers) on youtube in each category
- Manually selected channels results ( data/manually-filtered/youtube_channels.csv)
- Python script (crawling/youtube/collect_videos_in_channel.py) to collect all videoIDs from a YouTube Channel
- Collected videoIDs from manually selected channels (data/manually-filtered/youtube_videos.csv)
- Added funcionality of collecting video's captions with youtube_api.py

### Changed
- Moved the directory imgs to assets
- Aggregated results from manually select chanels into a single csv

