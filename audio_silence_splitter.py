# Import the AudioSegment class for processing audio and the
# split_on_silence function for separating out silent chunks.
import argparse
import os
import textwrap

from pydub import AudioSegment
from pydub.silence import split_on_silence


def split_audio_bulk(audio_list, output_directory):
    audio_list = audio_list.split(',')
    for audio_file in audio_list:
        print('Processing {}'.format(audio_file))
        name = os.path.splitext(audio_file)[0]
        sub_dir = os.path.join(output_directory, name)
        os.mkdir(sub_dir)
        split_audio(audio_file, sub_dir)


def split_audio(audio_file, output_directory):
    # Load your audio.
    song = AudioSegment.from_mp3(audio_file)
    name = os.path.splitext(audio_file)[0]

    # Split track where the silence is 2 seconds or more and get chunks using
    # the imported function.
    chunks = split_on_silence(
        # Use the loaded audio.
        song,
        keep_silence=500,
        # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
        min_silence_len=2000,
        silence_thresh=-48
    )

    # Process each chunk with your parameters
    for chunk_num, audio_chunk in enumerate(chunks):
        # # Normalize the entire chunk.
        # normalized_chunk = match_target_amplitude(audio_chunk, -20.0)
        chunk_name = '{0}_{1}_of_{2}.mp3'.format(name, chunk_num, len(chunks))
        print('Exporting {0}'.format(chunk_name))
        output = os.path.join(output_directory, chunk_name)
        audio_chunk.export(
            output,
            format='mp3'
        )


def get_args():
    description = textwrap.dedent('''
    Separates an audio file when there is silence.

    Examples: 

    audio_silence_splitter.py -i audio_file.mp3 -o output_folder
    ''')

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-i', '--input',
                        help='Input filename')
    parser.add_argument('-o', '--output',
                        help='Output audio chunks to directory.')
    parser.add_argument('-b', '--bulk',
                        help='Bulk input of files, comma separated.')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    if args.bulk:
        split_audio_bulk(args.bulk, args.output)
    split_audio(args.input, args.output)