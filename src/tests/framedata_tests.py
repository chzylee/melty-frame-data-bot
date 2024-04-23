import unittest
from discord import Embed
from app.commands import framedata

class TestFrameData(unittest.TestCase):
    def test_get_frame_data_returns_embed(self):
        framedata_response = framedata.get_frame_data()
        self.assertIsNotNone(framedata_response)
        self.assertTrue(isinstance(framedata_response, Embed))


if __name__ == '__main__':
    unittest.main()
