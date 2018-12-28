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

    def get_party_cfg(self):
        self.ensure_one()

        party_obj = self.env["lanparty_server.party"].sudo()

        final_cfg_lines = [
            "name \"%s\"" % self.name
        ]

        default_cfg_lines = party_obj.get_default_cfg_lines()
        cfg_lines = self.get_cfg_lines()

        for default_cfg_line in default_cfg_lines:
            line_add = default_cfg_line

            line_start = None

            items = default_cfg_line.split()
            if items[0] == "bind":
                line_start = " ".join(items[0:1])

            if line_start:
                for cfg_line in cfg_lines:
                    if cfg_line.startswith(line_start):
                        line_add = cfg_line
                        break

            final_cfg_lines.append(line_add)

        return "\n".join(final_cfg_lines)

    def get_cfg_lines(self):
        self.ensure_one()

        cfg = self.cfg and str(self.cfg) or ""
        cfg_lines = cfg.splitlines()
        return list(cfg_lines)
