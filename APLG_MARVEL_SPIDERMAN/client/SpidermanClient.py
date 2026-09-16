import asyncio
import json
import logging
from typing import Set

# Dépendances de base d'Archipelago
from CommonClient import CommonContext, server_loop, gui_enabled
from NetUtils import ClientStatus

# Configuration du port local pour le Mod C++
LOCAL_IPC_PORT = 51234

class SpidermanContext(CommonContext):
    game = "Marvel's Spider-Man Remastered"
    items_handling = 0b111  # Tout recevoir (progression, useful, fillers)

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.checked_locations: Set[int] = set()
        self.ipc_clients = set()

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.checked_locations = set(args.get("checked_locations", []))
            logging.info(f"[Spider-Man Client] Connecté au Multiworld ! {len(self.checked_locations)} checks déjà validés.")
        elif cmd == "ReceivedItems":
            for item in args.get("items", []):
                item_id = item.item
                player_from = item.player
                logging.info(f"[Spider-Man Client] Reçu item ID: {item_id} envoyé par le joueur {player_from}")
                # Envoi de la commande au jeu via le socket local
                asyncio.create_task(self.notify_game_give_item(item_id))

    async def notify_game_give_item(self, item_id: int):
        """Transmet l'item reçu à tous les clients du mod local C++"""
        if not self.ipc_clients:
            logging.warning(f"[IPC] Aucun mod Spider-Man connecté pour injecter l'item {item_id}")
            return

        payload = json.dumps({"command": "GIVE_ITEM", "item_id": item_id})
        for ws in list(self.ipc_clients):
            try:
                await ws.send_str(payload)
            except Exception as e:
                logging.error(f"[IPC Error] Échec d'envoi au jeu: {e}")

    async def handle_game_check(self, location_id: int):
        """Appelé quand le jeu signale qu'un collectible ou boss est complété"""
        if location_id not in self.checked_locations:
            self.checked_locations.add(location_id)
            await self.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])
            logging.info(f"[Spider-Man Client] Check envoyé au serveur: {location_id}")


# --- Serveur WebSocket Local pour communiquer avec la DLL C++ ---
from aiohttp import web

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    ctx: SpidermanContext = request.app["ctx"]
    ctx.ipc_clients.add(ws)
    logging.info("[IPC] Le mod Spider-Man (DLL) vient de se connecter en local !")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                data = json.loads(msg.data)
                if data.get("event") == "LOCATION_CHECKED":
                    loc_id = data.get("location_id")
                    if loc_id:
                        await ctx.handle_game_check(int(loc_id))
    finally:
        ctx.ipc_clients.remove(ws)
        logging.info("[IPC] Le mod Spider-Man s'est déconnecté.")

    return ws


async def run_ipc_server(ctx: SpidermanContext):
    app = web.Application()
    app["ctx"] = ctx
    app.router.add_get("/", websocket_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", LOCAL_IPC_PORT)
    await site.start()
    logging.info(f"[IPC] Serveur local en écoute sur ws://127.0.0.1:{LOCAL_IPC_PORT}")


async def main():
    ctx = SpidermanContext("localhost:38281", "")
    ctx.server_task = asyncio.create_task(server_loop(ctx))
    ipc_task = asyncio.create_task(run_ipc_server(ctx))

    # Commande console manuelle pour tester sans le jeu : 'check 8901001'
    loop = asyncio.get_event_loop()
    while not ctx.exit_event.is_set():
        await asyncio.sleep(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())