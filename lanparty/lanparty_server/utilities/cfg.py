import shlex

from odoo import models


class CfgUtility(models.TransientModel):
    _name = "lanparty_server.utility_cfg"
    _description = "Utility for CFG parsing"

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
