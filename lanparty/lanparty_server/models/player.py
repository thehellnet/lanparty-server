from odoo import models, fields


class Player(models.Model):
    _name = "lanparty_server.player"
    _inherit = "mail.thread"

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

    note = fields.Html(
        string="Note"
    )
