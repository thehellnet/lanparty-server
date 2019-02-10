from odoo import models, fields


class CfgExportWizard(models.TransientModel):
    _name = "lanparty_server.wizard_cfg_export"

    cfg = fields.Text(
        string="CFG",
        translate=False
    )

    def action_download(self):
        self.ensure_one()
