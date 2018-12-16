from odoo import models, fields


class PlayerBarcodeRegisterWizard(models.TransientModel):
    _name = "lanparty_server.wizard_player_barcode_register"

    player_id = fields.Many2one(
        string="Player",
        comodel_name="lanparty_server.player",
        readonly=True
    )

    barcode = fields.Char(
        string="Barcode",
        required=True
    )

    def action_barcode_register(self):
        self.ensure_one()

        self.player_id.barcode = self.barcode
