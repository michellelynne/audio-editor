import mock

import pytest

from audio_silence_splitter import audio_editor_list, AudioEditor


class TestAudioSplitter(object):

    @pytest.fixture()
    def audio_editor(self):
        return AudioEditor('audio_test.mp3', 'output')

    @pytest.mark.parametrize('audio,call_args_list', [
        ('test.mp3', [mock.call('test.mp3', 'output/test')]),
        ('test1.mp3,test2.mp3', [
            mock.call('test1.mp3', 'output/test1'), mock.call('test2.mp3', 'output/test2')])
    ])
    @mock.patch('os.mkdir')
    @mock.patch('audio_silence_splitter.AudioEditor')
    def test_audio_editor_list(self, mock_editor, mock_mkdir, audio, call_args_list):
        audio_editor_list(audio)
        assert mock_editor.call_args_list == call_args_list

    def test_init(self, audio_editor):
        assert audio_editor.audio_file == 'audio_test.mp3'
        assert audio_editor.output_directory == 'output'
        assert audio_editor.audio_file_name == 'audio_test'
        assert audio_editor.chunk_name_format == 'audio_test_{current}_of_{total}.mp3'

    def test_audio_chunks(self, audio_editor):
        _audio_chunks = audio_editor.audio_chunks
        assert len(_audio_chunks) == 2
        assert _audio_chunks[0].duration_seconds == 1.2709977324263038
        assert _audio_chunks[1].duration_seconds == 1.0059863945578231

    @mock.patch('audio_silence_splitter.AudioSegment.export')
    def test_write_audio_chunks(self, mock_audio_segment, audio_editor):
        audio_editor.write_audio_chunks()
        mock_audio_segment.assert_called_with('output/audio_test_2_of_2.mp3', format='mp3')

    @mock.patch('audio_silence_splitter.AudioEditor.get_speech_recognition_results')
    def test_get_transcript(self, mock_speech_results, audio_editor):
        mock_speech_results.return_value = {'results': [{'alternatives': [{'transcript': 'test'}]}]}
        assert audio_editor.get_transcript(audio_editor.audio_file) == 'test'