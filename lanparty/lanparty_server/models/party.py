from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


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

    @api.model
    def create(self, values):

        if "cfg" in values:
            utility_cfg = self.env["lanparty_server.utility_cfg"]
            cfg_raw = values["cfg"]
            cfg = utility_cfg.parse(cfg_raw)
            values["cfg"] = utility_cfg.serialize(cfg)

        return super().create(values)

    @api.multi
    def write(self, values):

        if "cfg" in values:
            utility_cfg = self.env["lanparty_server.utility_cfg"]
            cfg_raw = values["cfg"]
            cfg = utility_cfg.parse(cfg_raw)
            values["cfg"] = utility_cfg.serialize(cfg)

        return super().write(values)

    def action_default_set(self):
        self.ensure_one()

        self.search([]).write({
            "default": False
        })

        self.default = True

    def action_cfg_export(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Import CFG",
            "res_model": "lanparty_server.wizard_export",
            "view_type": "form",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_cfg": self.get_cfg()
            }
        }

    def action_cfg_import(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Import CFG",
            "res_model": "lanparty_server.wizard_party_cfg_import",
            "view_type": "form",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_party_id": self.id
            }
        }

    @api.model
    def get_default_party(self):
        party_obj = self.sudo()

        party_id = party_obj.search([("default", "=", True)], limit=1)
        if not party_id:
            raise ValidationError(_("No default party set"))

        return party_id

    def get_cfg(self):
        self.ensure_one()

        utility_cfg = self.env["lanparty_server.utility_cfg"]

        cfg_raw = self.cfg and str(self.cfg) or ""
        return utility_cfg.parse(cfg_raw)
