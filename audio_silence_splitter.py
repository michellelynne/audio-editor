import argparse
import csv
import logging
import os
import sys
import textwrap
from datetime import datetime

from cached_property import cached_property
from ibm_watson.speech_to_text_v1 import SpeechToTextV1
from pydub import AudioSegment
from pydub.silence import split_on_silence

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
IBM_API_KEY = os.getenv('IBM_API_KEY')
TRANSCRIPT_URL = 'https://stream.watsonplatform.net/speech-to-text/api'


class AudioEditor(object):

    def __init__(self, audio_file, output_directory):
        self.audio_file = audio_file
        self.output_directory = output_directory
        self.audio_file_name = os.path.splitext(audio_file)[0]
        self.chunk_name_format = self.audio_file_name + '_{current}_of_{total}.mp3'

    @cached_property
    def audio_chunks(self):
        """Audio broken into segments based on silence."""
        song = AudioSegment.from_mp3(self.audio_file)
        return split_on_silence(
            song,
            keep_silence=500,
            min_silence_len=2000,
            silence_thresh=-48
        )

    def write_audio_chunks(self):
        """Writes audio chunks to disk.

        Returns:
            List<str>: List of audio paths created.

        """
        _audio_chunk_file_paths = []
        for chunk_num, audio_chunk in enumerate(self.audio_chunks):
            _chunk_name = self.chunk_name_format.format(
                current=chunk_num + 1, total=len(self.audio_chunks)
            )
            _chunk_file_path = os.path.join(self.output_directory, _chunk_name)
            _audio_chunk_file_paths.append(_chunk_file_path)
            audio_chunk.export(
                _chunk_file_path,
                format='mp3'
            )
        return _audio_chunk_file_paths

    def get_speech_recognition_results(self, audio_path):
        """Get the speech recognition results from IBM Cloud.

        Args:
            audio_path (str): Name of the audio file.

        Return:
            DetailedResponse: Response from IBM Cloud.

        """
        speech_to_text = SpeechToTextV1(iam_apikey=IBM_API_KEY, url=TRANSCRIPT_URL)
        with open(audio_path, 'rb') as audio_path:
            speech_recognition_results = speech_to_text.recognize(
                audio=audio_path,
                content_type='audio/mp3'
            )
        return speech_recognition_results.get_result()

    def get_transcript(self, audio_path):
        """Get the transcript from IBM Cloud for the Audio File.

        Args:
            audio_path (str): Name of the audio file.

        Return:
            str: Transcript of the audio file.

        """
        speech_recognition_results = self.get_speech_recognition_results(audio_path)
        _transcript = ''
        for sr_result in speech_recognition_results['results']:
            _transcript += ' ' + sr_result['alternatives'][0]['transcript']
        return _transcript.strip()

    def write_transcript_csv(self, audio_chunk_file_paths):
        """Writes transcript of chunks to a CSV file.

        Args:
            List<str>: List of audio chunk file paths.

        """
        csv_file_name = '{}_{}.csv'.format(self.audio_file_name, datetime.now().strftime('%Y%m%d'))
        csv_file_path = os.path.join(self.output_directory, csv_file_name)
        with open(csv_file_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['segment', 'transcript'])
            for audio_path in audio_chunk_file_paths:
                # transcript = self.get_transcript(audio_path)
                chunk_name = os.path.basename(audio_path)
                # writer.writerow([chunk_name, transcript])

    def run(self):
        audio_chunk_file_paths = self.write_audio_chunks()
        # self.write_transcript_csv(audio_chunk_file_paths)


def audio_editor_list(audio):
    """Run Audio Editor on a list of audio files.

    Creates a directory for each audio file

    Args:
        audio (str): List of audio files separated by comma.

    """
    for audio_file in audio.split(','):
        LOGGER.info('Processing {}'.format(audio_file))
        name = os.path.splitext(audio_file)[0]
        sub_dir = os.path.join('output', name)
        if not os.path.exists(sub_dir):
            os.mkdir(sub_dir)
        audio_editor = AudioEditor(audio_file, sub_dir)
        audio_editor.run()


def get_args():
    description = textwrap.dedent('''
    Separates an audio file when there is silence.

    Examples: 

    audio_silence_splitter.py audio_file.mp3
    ''')

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('audio')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    audio_editor_list(args.audio)
