import unittest
import configparser




class MyTestCase(unittest.TestCase):
    def test_config_details(self):
        cfg = configparser.ConfigParser()
        cfg.read('../config.cfg')
        actual_data = cfg['test']['sample_key']
        expected_data = 'sample_data_value'
        self.assertEqual(expected_data, actual_data)


if __name__ == '__main__':
    unittest.main()
