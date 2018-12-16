from odoo import models, fields


class Player(models.Model):
    _name = "lanparty_server.player"
    _inherit = "mail.thread"

    _constraints = [
        ("name_uniq", "UNIQUE(name)", "Name already present"),
        ("barcode_uniq", "UNIQUE(barcode)", "Barcode already present")
    ]

    name = fields.Char(
        string="Name",
        reuqired=True,
        translate=False,
        track_visibility="onchange"
    )

    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        track_visibility="onchange"
    )

    barcode = fields.Char(
        string="Barcode",
        readonly=True
    )

    cfg = fields.Text(
        string="CFG",
        translate=False
    )

    note = fields.Html(
        string="Note"
    )
