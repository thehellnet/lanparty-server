import base64

from odoo import models, fields, api


class PartyCfgImportWizard(models.TransientModel):
    _name = "lanparty_server.wizard_party_cfg_import"
    _description = "CFG import wizard for lan party"

    party_id = fields.Many2one(
        string="Party",
        comodel_name="lanparty_server.party",
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

        utility_cfg = self.env["lanparty_server.utility_cfg"].sudo()

        cfg_raw = base64.b64decode(self.cfg_file).decode()
        cfg = utility_cfg.parse(cfg_raw)
        self.cfg = utility_cfg.serialize(cfg)

    def action_save(self):
        self.ensure_one()

        self.party_id.cfg = self.cfg
