# Youtube Hatespeech research

All notable changes to this research, starting from 22 of july 2018, will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)

## v0.4  - 2018-08-30
 
### Added
- script that prepare teh data for analysis


## v0.3 - 2018-08-15

### Added
- YouTube api call to collect all comments (not reply to comments) from videoId
- script to collect all comments from all database video
- script to collect all coments from video now logs the videos that disabled comments into "data/videos_that_disabled_comments.csv" 
- script to summarize statistics from collected data

### Fix
- Adding exception handler for error 403 ( YouTube Video's disabled comments) and 400 (api temporaly failure)
- Encode fix on youtube_channels.csv

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

