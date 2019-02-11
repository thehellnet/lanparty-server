from odoo import http, _
from odoo.http import request


class ToolController(http.Controller):
    @http.route(
        route="/ap1/v1/tool/welcome",
        type="json",
        auth="public",
        methods=["POST"],
        cors="*",
        csrf=False
    )
    def welcome(self, **kwargs):
        return {
            "success": True
        }

    @http.route(
        route="/ap1/v1/tool/get_cfg",
        type="json",
        auth="public",
        methods=["POST"],
        cors="*",
        csrf=False
    )
    def get_cfg(self, **kwargs):
        if "barcode" not in kwargs:
            return {
                "success": False,
                "error": _("No barcode")
            }

        barcode = kwargs["barcode"]

        player_obj = request.env["lanparty_server.player"].sudo()
        party_obj = request.env["lanparty_server.party"].sudo()
        utility_cfg = request.env["lanparty_server.utility_cfg"]

        player_id = player_obj.search([("barcode", "=", barcode)], limit=1)
        if not player_id:
            return {
                "success": False,
                "error": _("No player found for given barcode")
            }

        cfg_default = party_obj.get_default_party().get_cfg()
        cfg_player = player_id.get_cfg()
        cfg = utility_cfg.compare(cfg_default=cfg_default, cfg_player=cfg_player)

        cfg_raw = utility_cfg.serialize(cfg)

        cfg_lines = [
            "unbindall"
        ]

        cfg_lines.extend(cfg_raw.splitlines())

        cfg_lines.append("name \"%s\"" % player_id.name)

        return {
            "success": True,
            "data": cfg_lines
        }
