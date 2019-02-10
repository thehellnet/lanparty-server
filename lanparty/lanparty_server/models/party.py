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

    @api.model
    def get_default_cfg(self):
        party_id = self.get_default_party()
        return party_id.get_cfg()

    def get_cfg(self):
        self.ensure_one()

        cfg = self.cfg and str(self.cfg) or ""
        cfg_lines = self.list_uniq(cfg.splitlines())
        return cfg_lines

    @staticmethod
    def list_uniq(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]
