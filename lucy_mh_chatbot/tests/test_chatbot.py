import unittest
from unittest.mock import patch

from scripts.chatbot import ChatBot


class TestChatBot(unittest.TestCase):
    def setUp(self):
        self.bot = ChatBot()

    def test_greeting(self):
        with patch('builtins.input', return_value='hello'):
            self.assertEqual(self.bot.handle_message(), 'Hi there!')

    def test_invalid_input(self):
        with patch('builtins.input', return_value='random input'):
            self.assertEqual(self.bot.handle_message(), "I'm sorry, I don't understand. Can you please rephrase that?")

    def test_exit_command(self):
        with patch('builtins.input', return_value='exit'):
            self.assertEqual(self.bot.handle_message(), 'Goodbye!')

if __name__ == '__main__':
    unittest.main()
