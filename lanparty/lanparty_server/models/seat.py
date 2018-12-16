from odoo import models, fields


class Seat(models.Model):
    _name = "lanparty_server.seat"
    _inherit = "mail.thread"

    _constraints = [
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

    note = fields.Html(
        string="Note"
    )
