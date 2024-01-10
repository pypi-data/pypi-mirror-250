from pytee2 import Tee

def test_capturedtext():
    tee = Tee()

    tee.start()
    print('test_capturedtext')
    tee.stop()
    assert tee.get_capturedtext() == 'test_capturedtext\n'

    very_long_string = ''.join(['This is a very long string. ' for _ in range(10000)])
    tee.start()
    print(very_long_string)
    tee.stop()
    assert tee.get_capturedtext() == very_long_string + '\n'

def test_file_output(tmp_path):
    output_filepath = tmp_path / 'test_output.txt'
    tee = Tee(output_filepath=output_filepath)

    tee.start()
    print('test_capturedtext')
    tee.stop()
    assert output_filepath.read_text() == 'test_capturedtext\n'
    assert len(list(tmp_path.iterdir())) == 1

    very_long_string = ''.join(['This is a very long string. ' for _ in range(10000)])
    tee.start()
    print(very_long_string)
    tee.stop()
    assert output_filepath.read_text() == very_long_string + '\n'
    assert len(list(tmp_path.iterdir())) == 1
