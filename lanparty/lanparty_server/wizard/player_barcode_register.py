from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PlayerBarcodeRegisterWizard(models.TransientModel):
    _name = "lanparty_server.wizard_player_barcode_register"
    _description = "Wizard for registering barcode to player"

    player_id = fields.Many2one(
        string="Player",
        comodel_name="lanparty_server.player",
        readonly=True
    )

    barcode = fields.Char(
        string="Barcode",
        required=True
    )

    @api.onchange("barcode")
    def onchange_barcode(self):
        self.ensure_one()

        if not self.barcode:
            return

        player_obj = self.env["lanparty_server.player"]

        player_id = player_obj.search([("barcode", "=", self.barcode)])
        if player_id:
            raise ValidationError("Barcode already registered for player %s" % player_id.name)

        self.player_id = player_id

    def action_barcode_register(self):
        self.ensure_one()

        self.player_id.barcode = self.barcode
