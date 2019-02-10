{
    "name": "LAN Party Server",
    "version": "12.0.0.0.0",
    "summary": "LAN Party server for tools",
    "description": """
LAN Party Server
====================
LAN Party Server for tool API and management
    """,
    "category": "Other Tools",
    "website": "https://www.thehellnet.org",
    "depends": [
        "contacts",
        "mail"
    ],
    "data": [
        "views/player.xml",
        "views/seat.xml",
        "views/party.xml",

        "wizard/player_barcode_register.xml",
        "wizard/seat_player_change.xml",
        "wizard/player_cfg_import.xml",
        "wizard/party_cfg_import.xml",

        "security/access/player.xml",
        "security/access/seat.xml",
        "security/access/party.xml",

        "menu/actions.xml",
        "menu/items.xml"
    ],
    "installable": True,
    "application": True,
    "auto_install": False
}
