import base64
import shlex

from odoo import models, fields, api


class PlayerCfgImportWizard(models.TransientModel):
    _name = "lanparty_server.wizard_player_cfg_import"

    player_id = fields.Many2one(
        string="Player",
        comodel_name="lanparty_server.player",
        readonly=True
    )

    cfg_file = fields.Binary(
        string="CFG file"
    )

    cfg_file_name = fields.Char(
        string="CFG file name"
    )

    cfg = fields.Text(
        string="CFG",
        translate=False
    )

    @api.onchange("cfg_file")
    def onchange_cfg_file(self):
        self.ensure_one()

        if not self.cfg_file:
            return

        file_cfg = base64.b64decode(self.cfg_file).decode()
        file_cfg_lines = file_cfg.splitlines()

        default_cfg_lines = self.env["lanparty_server.party"].sudo().get_default_cfg_lines()

        new_lines = []

        for default_cfg_line in default_cfg_lines:
            default_items = shlex.split(default_cfg_line)

            default_param = None
            default_value = None

            if default_items[0] == "bind":
                default_param = "%s %s" % (default_items[0], default_items[1])
                default_value = "\"" + "\" \"".join(default_items[2:]) + "\""
            elif default_items[0] == "seta":
                if default_items[1] not in ["sensitivity"]:
                    continue
                default_param = "%s %s" % (default_items[0], default_items[1])
                default_value = "\"" + "\" \"".join(default_items[2:]) + "\""

            if not default_param:
                continue

            for file_cfg_line in file_cfg_lines:
                if not file_cfg_line.startswith(default_param):
                    continue

                items = shlex.split(file_cfg_line)
                value = "\"" + "\" \"".join(items[2:]) + "\""

                if value != default_value:
                    new_lines.append(file_cfg_line)

        ordered_new_lines = list(set(new_lines))
        ordered_new_lines.sort()
        cfg = "\n".join(ordered_new_lines)
        self.cfg = cfg

    def action_save(self):
        self.ensure_one()

        self.player_id.cfg = self.cfg
