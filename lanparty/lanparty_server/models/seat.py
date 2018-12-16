from odoo import models, fields


class Seat(models.Model):
    _name = "lanparty_server.seat"
    _inherit = "mail.thread"

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
