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
                "default_cfg": self.get_party_cfg()
            }
        }

    def action_cfg_import(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Import CFG",
            "res_model": "lanparty_server.wizard_player_cfg_import",
            "view_type": "form",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_player_id": self.id
            }
        }

    def get_cfg(self):
        self.ensure_one()

        cfg = self.cfg and str(self.cfg) or ""
        cfg_lines = cfg.splitlines()
        return list(cfg_lines)

    def get_party_cfg(self):
        self.ensure_one()

        party_obj = self.env["lanparty_server.party"].sudo()
        utility_cfg = self.env["lanparty_server.utility_cfg"].sudo()

        cfg_lines = [
            "unbindall"
        ]

        cfg_default = party_obj.get_default_cfg()
        cfg_player = self.get_cfg()
        cfg = utility_cfg.compare(cfg_default, cfg_player)
        cfg_lines.extend(cfg)

        cfg_lines.extend([
            "name \"%s\"" % self.name,
            "say %s collegato" % self.name
        ])

        return cfg_lines
