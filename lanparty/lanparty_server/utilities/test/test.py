import shlex
from unittest import TestCase


class CfgUtility:
    @staticmethod
    def split_lines(cfg_raw):
        return [x.strip() for x in cfg_raw.splitlines() if x.strip()]

    @staticmethod
    def split_command(command_raw):
        items = [x.strip() for x in shlex.split(command_raw)]

        row_command = items[0].lower()

        if row_command in ["bind"]:
            param = " ".join([items[0].lower(), items[1].upper()])
            value = " ".join(items[2:]).lower()
        elif row_command in ["seta"]:
            param = " ".join(items[0:2]).lower()
            value = " ".join(items[2:]).lower()
        elif row_command in ["sensitivity", "name", "say"]:
            param = " ".join(items[0:1]).lower()
            value = " ".join(items[1:]).lower()
        else:
            param = " ".join(items).lower()
            value = ""

        return param, value

    @staticmethod
    def compare(cfg_default=None, cfg_player=None):
        if cfg_default is None:
            cfg_default = {}
        if cfg_player is None:
            cfg_player = {}

        cfg = {}

        for key, default_value in cfg_default.items():
            cfg[key] = cfg_player[key] if key in cfg_player else cfg_default[key]

        return cfg

    @staticmethod
    def remove_forbidden(cfg=None):
        if cfg is None:
            cfg = {}

        return_cfg = {}

        for key, value in cfg.items():
            if key not in ["unbindall", "name", "seta name", "say"]:
                return_cfg[key] = value

        return return_cfg

    @staticmethod
    def parse(raw=""):
        lines = CfgUtility.split_lines(raw)
        cfg = {}

        for line in lines:
            key, value = CfgUtility.split_command(line)
            cfg[key] = value

        return CfgUtility.remove_forbidden(cfg)

    @staticmethod
    def serialize(cfg=None):
        if cfg is None:
            cfg = {}

        lines = []

        for key, value in cfg.items():
            if value:
                lines.append("%s \"%s\"" % (key, value))
            else:
                lines.append("%s" % key)

        return "\n".join(lines) + "\n"


class TestCfg(TestCase):

    def test_split_lines(self):
        data_input = "a\nb\rc\n\rd\r\ne\n\n\nf\n"
        data_expected = ["a", "b", "c", "d", "e", "f"]
        data_actual = CfgUtility.split_lines(data_input)
        self.assertListEqual(data_expected, data_actual)

    def test_split_command(self):
        data = {
            "seta name \"test\"": ("seta name", "test"),
            "seta NaMe \"teSt\"": ("seta name", "test"),
            "seta name test": ("seta name", "test"),
            "seta naME tesT": ("seta name", "test"),
            "naME tesT": ("name", "test"),
            "naME \"tesT\"": ("name", "test"),
            "naME 'tesT'": ("name", "test"),
            "bind F \"+testing\"": ("bind F", "+testing"),
            "bind r \"+ReDsting\"": ("bind R", "+redsting"),
            "bind F +testing": ("bind F", "+testing"),
            "sensitivity \"5\"": ("sensitivity", "5"),
            "sensitivity 5": ("sensitivity", "5"),
            "say tset": ("say", "tset"),
            "say \"tset\"": ("say", "tset"),
            "say 'tset'": ("say", "tset"),
            "unbindall": ("unbindall", ""),
        }

        for key, value in data.items():
            self.assertTupleEqual(value, CfgUtility.split_command(key))

    def test_compare(self):
        cfg_default = {
            "bind A": "test",
            "bind B": "test",
            "seta cg_fov": "65",
            "sensitivity": "5"
        }

        data_input = {
            0: {

            },
            1: {
                "bind A": "testing"
            },
            2: {
                "seta cg_fov": "80"
            },
            3: {
                "bind B": "hello", "seta cg_fov": "80"
            },
            4: {
                "sensitivity": "3.65"
            }
        }

        data_expected = {
            0: {
                "bind A": "test",
                "bind B": "test",
                "seta cg_fov": "65",
                "sensitivity": "5"
            },
            1: {
                "bind A": "testing",
                "bind B": "test",
                "seta cg_fov": "65",
                "sensitivity": "5"
            },
            2: {
                "bind A": "test",
                "bind B": "test",
                "seta cg_fov": "80",
                "sensitivity": "5"
            },
            3: {
                "bind A": "test",
                "bind B": "hello",
                "seta cg_fov": "80",
                "sensitivity": "5"
            },
            4: {
                "bind A": "test",
                "bind B": "test",
                "seta cg_fov": "65",
                "sensitivity": "3.65"
            }
        }

        for key, cfg_input in data_input.items():
            cfg_expected = data_expected[key]
            cfg_actual = CfgUtility.compare(cfg_default, cfg_input)
            self.assertDictEqual(cfg_expected, cfg_actual)

    def test_remove_forbidden(self):
        cfg_input = {
            "bind A": "test",
            "name": "testname",
            "seta name": "testname",
            "bind B": "test",
            "seta cg_fov": "65",
            "unbindall": "",
            "say": "test",
            "sensitivity": "5"
        }

        cfg_expected = {
            "bind A": "test",
            "bind B": "test",
            "seta cg_fov": "65",
            "sensitivity": "5"
        }

        cfg_actual = CfgUtility.remove_forbidden(cfg_input)

        self.assertDictEqual(cfg_expected, cfg_actual)

    def test_parse(self):
        data = {
            "": {},
            "\n": {},
            "\n\r": {},
            "\r": {},
            "\r\n": {},
            "unbindall": {},
            "unbindall\n": {},
            "unbindall\nname test": {},
            "unbindall\rname test": {},
            "unbindall\n\rname test": {},
            "unbindall\r\nname test": {},
            "unbindall\nname \"test\"": {},
            "unbindall\nname 'test'": {},
            "bind a +frag\nunbindall\nname 'test'": {"bind A": "+frag"},
            "bind A +frag\nunbindall\nname 'test'": {"bind A": "+frag"},
            "bind A \"+frag\"\nunbindall\nname 'test'": {"bind A": "+frag"},
            "bind A '+frag'\nunbindall\nname 'test'": {"bind A": "+frag"},
            "bind A '+frag'\n\r": {"bind A": "+frag"},
            "bind A '+frag'\r": {"bind A": "+frag"},
            "bind A \"+frag\"\nseta name tesst\nsensitivity 3": {"bind A": "+frag", "sensitivity": "3"},
            "bind A \"+frag\"\nseta name tesst\nsensitivity \"3\"": {"bind A": "+frag", "sensitivity": "3"}
        }

        for data_input, data_expected in data.items():
            data_actual = CfgUtility.parse(data_input)
            self.assertDictEqual(data_expected, data_actual)

    def test_serialize(self):
        data_input = {
            0: {"bind A": "+frag", "sensitivity": "3"},
            1: {"bind A": "+frag", "unbindall": ""},
        }

        data_expected = {
            0: "bind A \"+frag\"\nsensitivity \"3\"\n",
            1: "bind A \"+frag\"\nunbindall\n"
        }

        for key, cfg_input in data_input.items():
            expected = data_expected[key]
            actual = CfgUtility.serialize(cfg_input)
            self.assertEqual(expected, actual)
