import shlex

from odoo import models


class CfgUtility(models.TransientModel):
    _name = "lanparty_server.utility_cfg"

    @staticmethod
    def cfg_split_lines(cfg_raw):
        return [x.strip() for x in cfg_raw.splitlines()]

    @staticmethod
    def cfg_split_command(command_raw):
        return [x.strip() for x in shlex.split(command_raw)]

    @staticmethod
    def remove_forbidden_commands(cfg=None):
        if cfg is None:
            cfg = []

        return [x for x in cfg if x not in ["unbindall", "name", "say"]]

    @staticmethod
    def remove_common_lines(cfg_default=None, cfg_user=None):
        if cfg_default is None:
            cfg_default = []
        if cfg_user is None:
            cfg_user = []

        return list(set(cfg_user) ^ set(cfg_default))

    def compare_command(self, default="", cfg_user=None):
        if cfg_user is None:
            cfg_user = []

        items = self.cfg_split_command(default)

        row_command = items[0].lower()

        if row_command in ["unbindall", "name", "say"]:
            return False

        elif row_command == "bind":
            for cfg_user_row in cfg_user:
                row_items = self.cfg_split_command(cfg_user_row)
                if row_items[0].lower() == row_command and row_items[1].upper() == items[1].upper():
                    return cfg_user_row

        elif row_command == "seta":
            for cfg_user_row in cfg_user:
                row_items = self.cfg_split_command(cfg_user_row)
                if row_items[0].lower() == row_command and row_items[1].upper() == items[1].upper():
                    return cfg_user_row

        elif row_command == "sensitivity":
            for cfg_user_row in cfg_user:
                row_items = self.cfg_split_command(cfg_user_row)
                if row_items[0].lower() == row_command:
                    return cfg_user_row

        return default

    def compare(self, cfg_default=None, cfg_user=None):
        if cfg_default is None:
            cfg_default = []
        if cfg_user is None:
            cfg_user = []

        cfg = []

        for cfg_default_row in cfg_default:
            row = self.compare_command(cfg_default_row, cfg_user)
            if not row:
                continue
            cfg.append(row)

        cfg = self.remove_duplicated(cfg)

        return cfg

    def remove_duplicated(self, cfg):
        cfg_items = {}

        for cfg_row in cfg:
            items = self.cfg_split_command(cfg_row)
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
