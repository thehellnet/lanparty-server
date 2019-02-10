import base64

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

        file_cfg_raw = base64.b64decode(self.cfg_file).decode()
        cfg_file = file_cfg_raw.splitlines()

        party_obj = self.env["lanparty_server.party"].sudo()
        cfg_utility = self.env["lanparty_server.utility_cfg"].sudo()

        cfg_default = party_obj.get_default_cfg()
        cfg = cfg_utility.compare(cfg_default, cfg_file)

        cfg_player = cfg_utility.remove_common_lines(cfg, cfg_default)
        self.cfg = "\n".join(cfg_utility.remove_forbidden_commands(cfg_player))

    def action_save(self):
        self.ensure_one()

        self.player_id.cfg = self.cfg
