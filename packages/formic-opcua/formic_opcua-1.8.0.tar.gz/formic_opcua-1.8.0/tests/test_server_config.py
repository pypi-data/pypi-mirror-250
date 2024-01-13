# Copyright Formic Technologies 2023
from unittest import TestCase

from formic_opcua.core import InvalidYamlError, parse_settings


class TestOpcuaServer(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ok_server_config_path = 'data/ok_server_config.yaml'
        cls.nok_server_config_path = 'data/nok_server_config.yaml'
        cls.nok_dict_server_config_path = 'data/nok_dict_server_config.yaml'

    def test_parse_settings_yaml_typo(self):
        with self.assertRaises(InvalidYamlError):
            parse_settings(self.nok_server_config_path)

    def test_parse_settings_invalid_dict_structure(self):
        with self.assertRaises(InvalidYamlError):
            parse_settings(self.nok_dict_server_config_path)

    def test_no_server_config(self):
        with self.assertRaises(FileNotFoundError):
            parse_settings('non_existing_file.yaml')
