from odoo import models, fields


class Player(models.Model):
    _name = "lanparty_server.player"
    _inherit = "mail.thread"

    _sql_constraints = [
        ("name_uniq", "UNIQUE(name)", "Name already present"),
        ("barcode_uniq", "UNIQUE(barcode)", "Barcode already present")
    ]

    name = fields.Char(
        string="Name",
        reuqired=True,
        translate=False,
        track_visibility="onchange"
    )

    res_partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        track_visibility="onchange"
    )

    barcode = fields.Char(
        string="Barcode",
        translate=False,
        track_visibility="onchange"
    )

    cfg = fields.Text(
        string="CFG",
        translate=False,
        track_visibility="onchange"
    )

    note = fields.Html(
        string="Note"
    )

    def action_barcode_register(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Register barcode",
            "res_model": "lanparty_server.wizard_player_barcode_register",
            "view_type": "form",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_player_id": self.id
            }
        }
