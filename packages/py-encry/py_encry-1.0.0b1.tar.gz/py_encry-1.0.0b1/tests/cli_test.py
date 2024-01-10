import unittest
from click.testing import CliRunner
from src.pyencry.cli import cli

class CliTests(unittest.TestCase):
    def test_can_print_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'pyencry version 1.0.0b1\n')

    def test_can_encode_then_decode(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['-f', 'img/d.png', '-e', '-m', 'rail_fence_cipher', '--data', 'This is a secret message', '--new-file', 'img/test_encoded.png', '4'])
        print(result)
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-f', 'img/test_encoded.png', '-d', '-m', 'rail_fence_cipher', '4'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'This is a secret message\n')

    def test_can_encode_then_decode_with_random_spacing(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['-f', 'img/d.png', '-e', '-m', 'random_spacing', '--data', 'This is a secret message', '--new-file', 'img/test_encoded.png', '4'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-f', 'img/test_encoded.png', '-d', '-m', 'random_spacing', '4'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'This is a secret message\n')

    def test_can_encode_then_decode_with_random_spacing_and_different_key(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['-f', 'img/d.png', '-e', '-m', 'random_spacing', '--data', 'This is a secret message', '--new-file', 'img/test_encoded.png', '5'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-f', 'img/test_encoded.png', '-d', '-m', 'random_spacing', '5'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'This is a secret message\n')

    def test_can_encode_then_decode_with_random_spacing_and_different_key_and_different_file(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['-f', 'img/d.png', '-e', '-m', 'random_spacing', '--data', 'This is a secret message', '--new-file', 'img/test_encoded.png', '6'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-f', 'img/test_encoded.png', '-d', '-m', 'random_spacing', '6'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'This is a secret message\n')

    def test_can_encode_with_text_file(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['-f', 'img/d.png', '-e', '-m', 'random_spacing', '--data-file', 'data/test.txt', '--new-file', 'img/test_encoded.png', '6'])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['-f', 'img/test_encoded.png', '-d', '-m', 'random_spacing', '6'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'This is a secret message\n')

    def test_can_decode_with_text_file(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['-f', 'img/d.png', '-e', '-m', 'random_spacing', '--data-file', 'data/test.txt', '--new-file', 'img/test_encoded.png', '6'])
        result = runner.invoke(cli, ['-f', 'img/test_encoded.png', '-d', '-m', 'random_spacing', '--new-data-file', 'data/test_decoded.txt', '6'])
        self.assertEqual(result.exit_code, 0)
        with open('data/test_decoded.txt', 'r') as f:
            self.assertEqual(f.read(), 'This is a secret message')
