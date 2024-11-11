from gui import SteamApp

from config import STEAM_API_KEY

print(f"Steam API Key: {STEAM_API_KEY}")


if __name__ == "__main__":
    app = SteamApp()
    app.run()
