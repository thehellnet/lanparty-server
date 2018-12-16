from odoo import models, fields


class Seat(models.Model):
    _name = "lanparty_server.seat"
    _inherit = "mail.thread"

    _sql_constraints = [
        ("name_uniq", "UNIQUE(name)", "Address already present"),
        ("address_uniq", "UNIQUE(address)", "Address already present")
    ]

    name = fields.Char(
        string="Name",
        reuqired=True,
        translate=False,
        track_visibility="onchange"
    )

    address = fields.Char(
        string="Address",
        required=True,
        translate=False,
        track_visibility="onchange"

    )

    player_id = fields.Many2one(
        string="Current player",
        comodel_name="lanparty_server.player",
        track_visibility="onchange",
        readonly=True
    )

    note = fields.Html(
        string="Note"
    )
