import mock

import pytest

from audio_silence_splitter import audio_editor_list, AudioEditor


class TestAudioSplitter(object):

    @pytest.fixture()
    def audio_editor(self):
        return AudioEditor('apples.mp3', 'apples')

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

    # TODO: Create test audio file to include. Teardown any created files.
