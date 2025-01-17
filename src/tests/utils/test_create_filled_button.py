from unittest import TestCase
from utils import create_filled_button


class TestFilledButton(TestCase):
    def setUp(self):
        self.params = {
            "text": "Hello World",
        }

    def test_create_button(self):
        button = create_filled_button(self.params)
        assert button.text == self.params["text"]
