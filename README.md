This project is for tools I created to making my podcast easier.

# audio-silence-splitter

When editing a podcast I start with two tracks, mine and my guest. I realized that I spent alot of time cutting up each track into chunks for editing.
This script will check for silence and split into multiple mp3s. I recommend renaming the original file to something small
and easy to read. I add these split files to the audio editor one by one so it is easier to remove filler language
and put the different tracks together.

Usage:

Install [Python 3.7](https://www.python.org/downloads/release/python-370/)

Install ffmpeg ```brew install ffmpeg```

Create Python 3.7 virtualenv ```python3 -m venv audio_editor```

Activate virtualenv ```source audio_editor/bin/activate```

Install requirements ```pip install -r requirements.txt```

Run Script: ```audio_silence_splitter.py audio_file.mp3```


It takes a while. While you are waiting, you can listen to my podcast, [@FromSourcePod](https://twitter.com/FromSourcePod)

From the Source is an interview show about what tech jobs are really like, from the good, the bad, to the boring.

[Apple Podcasts](https://podcasts.apple.com/us/podcast/from-the-source/id1448339160) ~ [Spotify](https://open.spotify.com/show/0OpoyHy2U3Ev9n9gpYD3Zr?si=49XE0IRoR3GGB_iCqYSZKw) ~ [RSS](http://www.michellebrenner.com/feed/podcast/) ~ [Web](fromthesourcepod.com)

[Rate & review](https://podcasts.apple.com/us/podcast/from-the-source/id1448339160) to support the show and fine scripts like these.


# audio-transcript

I also wanted a transcript of what was in those files. This would make it easier to edit, and then have a transcript I could post with the episodes.
I tried a bunch of different speech to text tools, and landed on IBM which had both the best accuracy and ease of use.
This uses the same splitting functionality as audio-silence-splitter because it is easier to transcribe short audio.

Usage:

Sign up for a free [IBM Cloud Account](https://cloud.ibm.com/services/speech-to-text/). 

Follow the steps for Speech to Text quickstart until you get an API Key.

Save as environment variable IBM_API_KEY (command depends on your environment)

Follow all the steps for the splitt, but run the transcript instead. This also takes awhile, so you can listen to a second episode of [@FromSourcePod](https://twitter.com/FromSourcePod).

Run Script: ```audio_transcript.py audio_file.mp3```
