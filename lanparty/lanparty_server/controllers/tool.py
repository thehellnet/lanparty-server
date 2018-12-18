from odoo import http


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
