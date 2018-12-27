from odoo import models, fields


class Party(models.Model):
    _name = "lanparty_server.party"
    _inherit = "mail.thread"

    name = fields.Char(
        string="Name",
        required=True,
        track_visibility="onchange"
    )

    default = fields.Boolean(
        string="Default",
        required=True,
        default=False,
        readonly=True,
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

    def action_default_set(self):
        self.ensure_one()

        self.search([]).write({
            "default": False
        })

        self.default = True

    def action_cfg_export(self):
        self.ensure_one()

    def action_cfg_import(self):
        self.ensure_one()
