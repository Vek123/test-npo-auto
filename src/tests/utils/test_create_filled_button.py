from utils import create_filled_button


class TestFilledButton:
    def setup_class(self):
        self.params = {
            "text": "Hello World",
        }

    def test_create_button(self):
        button = create_filled_button(self.params)
        assert button.text == self.params["text"]
