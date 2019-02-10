import shlex
from unittest import TestCase

CFG_DEFAULT = [
    "unbindall",
    "bind TAB \"+scores\"",
    "bind SPACE \"+gostand\"",
    "bind . \"exec lanpartytool\"",
    "bind 1 \"weapnext\"",
    "bind 6 \"+actionslot 4\"",
    "bind ~ \"toggleconsole\"",
    "bind F12 \"screenshotJPEG\"",
    "seta cg_fov \"80\"",
    "seta name \"default\"",
    "seta sensitivity \"5\"",
    "say \"Collegato\""
]


def cfg_split_lines(cfg_raw):
    return [x.strip() for x in cfg_raw.splitlines()]


def cfg_split_command(command_raw):
    return [x.strip() for x in shlex.split(command_raw)]


def cfg_parse_command(default="", cfg_user=None):
    if cfg_user is None:
        cfg_user = []

    items = cfg_split_command(default)

    row_command = items[0].lower()

    if row_command == "bind":
        for cfg_user_row in cfg_user:
            row_items = cfg_split_command(cfg_user_row)
            if row_items[0].lower() == row_command and row_items[1].upper() == items[1].upper():
                return cfg_user_row

    if row_command == "seta":
        for cfg_user_row in cfg_user:
            row_items = cfg_split_command(cfg_user_row)
            if row_items[0].lower() == row_command and row_items[1].upper() == items[1].upper():
                return cfg_user_row

    return default


def cfg_compare(cfg_default=None, cfg_user=None):
    if cfg_default is None:
        cfg_default = []
    if cfg_user is None:
        cfg_user = []

    cfg = []

    for cfg_default_row in cfg_default:
        row = cfg_parse_command(cfg_default_row, cfg_user)
        cfg.append(row)

    return cfg


def remove_duplicated(cfg):
    cfg_items = {}

    for cfg_row in cfg:
        items = cfg_split_command(cfg_row)
        row_command = items[0].lower()

        if row_command in ["bind", "seta"]:
            key = " ".join(items[0:2])
            value = " ".join(items[2:])
        elif row_command in ["sensitivity"]:
            key = " ".join(items[0:1])
            value = " ".join(items[1:])
        else:
            continue

        cfg_items[key] = value

    cfg = ["%s \"%s\"" % (key, value) for key, value in cfg_items.items()]

    return cfg


class TestCfg(TestCase):

    def test_cfg_split_command(self):
        self.assertListEqual([], cfg_split_command(""))
        self.assertListEqual(["a"], cfg_split_command("a"))
        self.assertListEqual(["ab"], cfg_split_command("ab"))
        self.assertListEqual(["a", "b"], cfg_split_command("a b"))
        self.assertListEqual(["a", "b", "c"], cfg_split_command("a b c"))
        self.assertListEqual(["a", "b c"], cfg_split_command("a \"b c\""))
        self.assertListEqual(["a", "b c"], cfg_split_command("a 'b c'"))
        self.assertListEqual(["a", "b c"], cfg_split_command("'a' 'b c'"))
        self.assertListEqual(["a", "b c"], cfg_split_command("'a ' 'b c'"))
        self.assertListEqual(["a", "b c"], cfg_split_command("'a ' ' b c'"))
        self.assertListEqual(["a", "b c"], cfg_split_command("'a ' ' b c '"))
        self.assertListEqual(["a", "b c"], cfg_split_command("'a ' 'b c '"))
        self.assertListEqual(["a", "b c"], cfg_split_command("' a ' 'b c '"))
        self.assertListEqual(["a", "b c"], cfg_split_command("' a' 'b c '"))
        self.assertListEqual(["a", "b   c"], cfg_split_command("'a ' 'b   c '"))
        self.assertListEqual(["a", "b", "c"], cfg_split_command("'a ' 'b  ' \" c \""))
        self.assertListEqual(["bind", "SPACE", "+gostand"], cfg_split_command("bind SPACE \"+gostand\""))
        self.assertListEqual(["bind", "0", "+actionslot 4"], cfg_split_command("bind 0 \"+actionslot 4\""))

    def test_compare_no_changes(self):
        cfg_input = [
        ]

        cfg_expected = [
            "unbindall",
            "bind TAB \"+scores\"",
            "bind SPACE \"+gostand\"",
            "bind . \"exec lanpartytool\"",
            "bind 1 \"weapnext\"",
            "bind 6 \"+actionslot 4\"",
            "bind ~ \"toggleconsole\"",
            "bind F12 \"screenshotJPEG\"",
            "seta cg_fov \"80\"",
            "seta name \"default\"",
            "seta sensitivity \"5\"",
            "say \"Collegato\""
        ]

        cfg_actual = cfg_compare(CFG_DEFAULT, cfg_input)

        self.assertEqual(cfg_expected, cfg_actual)

    def test_compare_bind(self):
        cfg_input = [
            "bind TAB \"+frag\""
        ]

        cfg_expected = [
            "unbindall",
            "bind TAB \"+frag\"",
            "bind SPACE \"+gostand\"",
            "bind . \"exec lanpartytool\"",
            "bind 1 \"weapnext\"",
            "bind 6 \"+actionslot 4\"",
            "bind ~ \"toggleconsole\"",
            "bind F12 \"screenshotJPEG\"",
            "seta cg_fov \"80\"",
            "seta name \"default\"",
            "seta sensitivity \"5\"",
            "say \"Collegato\""
        ]

        cfg_actual = cfg_compare(CFG_DEFAULT, cfg_input)

        self.assertEqual(cfg_expected, cfg_actual)

    def test_compare_bind_seta(self):
        cfg_input = [
            "bind TAB \"+frag\"",
            "seta sensitivity \"3\"",
        ]

        cfg_expected = [
            "unbindall",
            "bind TAB \"+frag\"",
            "bind SPACE \"+gostand\"",
            "bind . \"exec lanpartytool\"",
            "bind 1 \"weapnext\"",
            "bind 6 \"+actionslot 4\"",
            "bind ~ \"toggleconsole\"",
            "bind F12 \"screenshotJPEG\"",
            "seta cg_fov \"80\"",
            "seta name \"default\"",
            "seta sensitivity \"3\"",
            "say \"Collegato\""
        ]

        cfg_actual = cfg_compare(CFG_DEFAULT, cfg_input)

        self.assertEqual(cfg_expected, cfg_actual)

    def test_compare_not_allowed(self):
        cfg_input = [
            "bind TAB \"+frag\"",
            "seta cg_drawLagometer \"1\"",
        ]

        cfg_expected = [
            "unbindall",
            "bind TAB \"+frag\"",
            "bind SPACE \"+gostand\"",
            "bind . \"exec lanpartytool\"",
            "bind 1 \"weapnext\"",
            "bind 6 \"+actionslot 4\"",
            "bind ~ \"toggleconsole\"",
            "bind F12 \"screenshotJPEG\"",
            "seta cg_fov \"80\"",
            "seta name \"default\"",
            "seta sensitivity \"5\"",
            "say \"Collegato\""
        ]

        cfg_actual = cfg_compare(CFG_DEFAULT, cfg_input)

        self.assertEqual(cfg_expected, cfg_actual)

    def test_remove_duplicated(self):
        cfg_input = [
            "bind TAB \"+frag\"",
            "bind SPACE \"+gostand\"",
            "bind TAB \"toggleconsole\"",
        ]

        cfg_expected = [
            "bind TAB \"toggleconsole\"",
            "bind SPACE \"+gostand\"",
        ]

        cfg_actual = remove_duplicated(cfg_input)

        self.assertEqual(cfg_expected, cfg_actual)
