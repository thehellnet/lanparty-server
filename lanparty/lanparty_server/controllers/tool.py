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
        route="/ap1/v1/tool/getCfg",
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
        player_id = player_obj.search([("barcode", "=", barcode)], limit=1)
        if not player_id:
            return {
                "success": False,
                "error": _("No player found for given barcode")
            }

        return {
            "success": True
        }
