"""
Spider-Man Remastered — Client Archipelago
==========================================
Pont entre le serveur Archipelago (port 38281) et la DLL mod C++ injectée
dans le jeu (WebSocket local sur le port 51234).

Architecture :
  ┌──────────────────────┐     WebSocket     ┌───────────────────────┐
  │  Serveur Archipelago │ ◄───────────────► │  SpidermanClient.py   │
  │    (port 38281)      │                   │       (ce fichier)    │
  └──────────────────────┘                   └──────────┬────────────┘
                                                        │  WebSocket local
                                             ┌──────────▼────────────┐
                                             │   dxgi.dll (mod C++)  │
                                             │   dans le jeu         │
                                             └───────────────────────┘
"""

import asyncio
import json
import logging
import os
from typing import Set, List

from CommonClient import CommonContext, server_loop
from aiohttp import web, WSMsgType

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LOCAL_IPC_PORT: int = 51234
DEFAULT_AP_ADDRESS: str = "localhost:38281"

logger = logging.getLogger("SpiderManClient")


# ---------------------------------------------------------------------------
# Contexte principal Archipelago
# ---------------------------------------------------------------------------

class SpidermanContext(CommonContext):
    """Contexte Archipelago dédié au mod Spider-Man Remastered."""

    game = "Marvel's Spider-Man Remastered"
    items_handling = 0b111  # Recevoir tous les items (progression, useful, fillers)

    def __init__(self, server_address: str, password: str):
        super().__init__(server_address, password)
        self.checked_locations: Set[int] = set()
        self.received_item_ids: List[int] = []
        # Utiliser un set protégé contre les modifications concurrentes
        # via asyncio (mono-thread), on peut se permettre un set simple.
        self.ipc_clients: Set[web.WebSocketResponse] = set()

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.checked_locations = set(args.get("checked_locations", []))
            logger.info(
                "[Spider-Man] Connecté au Multiworld ! "
                f"({len(self.checked_locations)} checks déjà validés)"
            )

        elif cmd == "ReceivedItems":
            for item in args.get("items", []):
                item_id: int = item.item
                # Stocker pour pouvoir rejouer l'historique lors d'une reconnexion DLL
                if item_id not in self.received_item_ids:
                    self.received_item_ids.append(item_id)
                logger.info(f"[Item reçu] ID: {item_id}")
                asyncio.create_task(self.notify_game_give_item(item_id))

    async def notify_game_give_item(self, item_id: int):
        """Transmet un item à tous les clients DLL connectés."""
        if not self.ipc_clients:
            logger.debug(f"[IPC] Aucun mod connecté pour l'item {item_id} — mis en file d'attente.")
            return

        payload = json.dumps({"command": "GIVE_ITEM", "item_id": item_id})
        # Itérer sur une copie pour éviter les problèmes si le set est modifié
        for ws in list(self.ipc_clients):
            try:
                await ws.send_str(payload)
            except Exception as exc:
                logger.warning(f"[IPC] Échec d'envoi item {item_id} : {exc}")

    async def sync_all_items_to_game(self, ws: web.WebSocketResponse):
        """Rejoue tout l'historique d'items reçus vers une DLL qui vient de se connecter."""
        logger.info(f"[IPC] Synchronisation de {len(self.received_item_ids)} items vers le jeu…")
        for item_id in self.received_item_ids:
            payload = json.dumps({"command": "GIVE_ITEM", "item_id": item_id})
            try:
                await ws.send_str(payload)
            except Exception as exc:
                logger.warning(f"[IPC] Sync interrompue sur item {item_id} : {exc}")
                return
            await asyncio.sleep(0.02)  # Petit délai pour ne pas saturer le WebSocket

    async def handle_game_check(self, location_id: int):
        """Envoie un check au serveur Archipelago si pas déjà validé."""
        if location_id not in self.checked_locations:
            self.checked_locations.add(location_id)
            await self.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])
            logger.info(f"[Check] Emplacement envoyé au serveur : {location_id}")


# ---------------------------------------------------------------------------
# Serveur WebSocket local (écoute les connexions de la DLL C++)
# ---------------------------------------------------------------------------

async def websocket_handler(request: web.Request) -> web.WebSocketResponse:
    """Gère une connexion WebSocket entrante depuis la DLL C++ du jeu."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    ctx: SpidermanContext = request.app["ctx"]
    ctx.ipc_clients.add(ws)
    logger.info("[IPC] Le mod Spider-Man (DLL) vient de se connecter !")

    # Rejouer immédiatement tous les items déjà reçus pour gérer les reconnexions
    await ctx.sync_all_items_to_game(ws)

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                except json.JSONDecodeError:
                    logger.warning(f"[IPC] Message malformé reçu : {msg.data!r}")
                    continue

                if data.get("event") == "LOCATION_CHECKED":
                    loc_id = data.get("location_id")
                    if isinstance(loc_id, int):
                        await ctx.handle_game_check(loc_id)
                    else:
                        logger.warning(f"[IPC] location_id invalide : {loc_id!r}")

            elif msg.type == WSMsgType.ERROR:
                logger.warning(f"[IPC] Erreur WebSocket : {ws.exception()}")
    finally:
        # discard() ne lève pas d'erreur si l'élément n'est pas dans le set
        ctx.ipc_clients.discard(ws)
        logger.info("[IPC] Le mod Spider-Man s'est déconnecté.")

    return ws


async def run_ipc_server(ctx: SpidermanContext):
    """Démarre le serveur WebSocket local qui écoute les connexions de la DLL."""
    app = web.Application()
    app["ctx"] = ctx
    app.router.add_get("/", websocket_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", LOCAL_IPC_PORT)
    await site.start()
    logger.info(f"[IPC] Serveur local en écoute sur ws://127.0.0.1:{LOCAL_IPC_PORT}/")


# ---------------------------------------------------------------------------
# Boucle de console interactive (debug / tests sans la DLL)
# ---------------------------------------------------------------------------

async def console_input_loop(ctx: SpidermanContext):
    """
    Boucle de commandes console manuelle.
    Commandes disponibles :
      check <id>   — simule un check de location (ex: check 8901000)
      status       — affiche le nombre de checks et d'items reçus
      exit / quit  — arrête le client
    """
    # asyncio.get_running_loop() est l'API correcte depuis Python 3.10+
    loop = asyncio.get_running_loop()

    while not ctx.exit_event.is_set():
        try:
            cmd = await loop.run_in_executor(None, input)
        except EOFError:
            break

        cmd = cmd.strip()

        if cmd.startswith("check "):
            try:
                loc_id = int(cmd.split(" ", 1)[1])
                await ctx.handle_game_check(loc_id)
            except (ValueError, IndexError):
                print("Usage : check <ID entier>")

        elif cmd == "status":
            print(
                f"Checks validés : {len(ctx.checked_locations)} | "
                f"Items reçus : {len(ctx.received_item_ids)} | "
                f"DLL(s) connectée(s) : {len(ctx.ipc_clients)}"
            )

        elif cmd in ("exit", "quit"):
            ctx.exit_event.set()


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

async def main():
    ctx = SpidermanContext(DEFAULT_AP_ADDRESS, "")
    ctx.auth = os.environ.get("AP_PLAYER_NAME", "SpideyPlayer")

    ctx.server_task = asyncio.create_task(server_loop(ctx))
    asyncio.create_task(run_ipc_server(ctx))
    asyncio.create_task(console_input_loop(ctx))

    # Maintenir la boucle active jusqu'à l'événement de sortie
    await ctx.exit_event.wait()
    logger.info("[Spider-Man] Client arrêté proprement.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    asyncio.run(main())
