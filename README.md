This project is for tools I created to making my podcast easier.

# audio-silence-splitter

When editing a podcast I start with two tracks, mine and my guest. I realized that I spent alot of time cutting up each track into chunks for editing.
I also wanted a transcript of what was in those files. This would make it easier to edit, and then have a transcript I could post with the episodes.
I tried a bunch of different speech to text tools, and landed on IBM which had both the best accuracy and ease of use.

Usage:

Sign up for a free [IBM Cloud Account](https://cloud.ibm.com/services/speech-to-text/). 

Follow the steps for Speech to Text quickstart until you get an API Key.

Save as environment variable IBM_API_KEY (command depends on your environment)

Install [Python 3.7](https://www.python.org/downloads/release/python-370/)

Create Python 3.7 virtualenv ```virtualenv -p python3 audio_editor```

Activate virtualenv ```source audio_editor/bin/activate```

Install requirements ```pip install -r requirements.txt```

Run Script: ```audio_silence_splitter.py audio_file.mp3```

Wait. It takes a long time. Maybe go watch a movie. 

#TODO: Write tests.