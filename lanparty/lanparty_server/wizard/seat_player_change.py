from odoo import models, fields, api


class SeatPlayerChangeWizard(models.TransientModel):
    _name = "lanparty_server.wizard_seat_player_change"

    seat_id = fields.Many2one(
        string="Seat",
        comodel_name="lanparty_server.seat",
        readonly=True
    )

    barcode = fields.Char(
        string="Search by Barcode",
        help="Type barcode for player search"
    )

    player_id = fields.Many2one(
        string="Player",
        comodel_name="lanparty_server.player",
        required=True
    )

    @api.onchange("barcode")
    def onchange_barcode(self):
        self.ensure_one()

        if not self.barcode:
            return

        player_obj = self.env["lanparty_server.player"]

        player_id = player_obj.search([("barcode", "=", self.barcode)])
        if not player_id:
            return

        self.player_id = player_id

    def action_player_change(self):
        self.ensure_one()

        self.seat_id.player_id = self.player_id
