import os
import subprocess
import platform
import requests
import random

class AccountLaunch:
    def __init__(self, cookie, placeId):
        self.cookie = cookie
        self.placeId = placeId

    def get_xsrf(self):
        auth_url = "https://auth.roblox.com/v2/logout"
        xsrf_request = requests.post(auth_url, cookies={'.ROBLOSECURITY': self.cookie})
        print("x-csrf-token: ", xsrf_request.headers["x-csrf-token"])
        return xsrf_request.headers["x-csrf-token"]

    def get_authentication_ticket(self):
        launch_url = 'https://auth.roblox.com/v1/authentication-ticket/'
        response = requests.post(launch_url, headers={'X-CSRF-Token': self.get_xsrf(), "Referer": "https://www.roblox.com/games/4924922222/Brookhaven-RP"}, cookies={'.ROBLOSECURITY': self.cookie})
        ticket = response.headers.get("rbx-authentication-ticket", "")
        print("rbx-authentication-ticket: ", ticket)
        return ticket

    def job_id(self):
        try:
            response = requests.get("https://games.roblox.com/v1/games/10515146389/servers/0?sortOrder=1&excludeFullGames=true&limit=25").json()
            data = response["data"][7]
            print("Job-ID: ", data["id"])
            return data["id"]
        except KeyError:
            response = requests.get("https://games.roblox.com/v1/games/10515146389/servers/0?sortOrder=1&excludeFullGames=true&limit=25").json()
            data = response["data"][4]
            print("Job-ID: ", data["id"])
            return data["id"]

    def launch_roblox(self, ticket, job_id): # ticket, access_code, link_code, join_vip, follow_user, job_id
        roblox_executable_path = None
        current_version = requests.get("https://clientsettings.roblox.com/v1/client-version/WindowsPlayer").json()["clientVersionUpload"]
        print("Roblox Version: ", current_version)
        r_path = os.path.join("C:\\Program Files (x86)\\Roblox\\Versions", current_version)
        
        if not os.path.exists(r_path):
            r_path = os.path.join(os.environ.get("LocalAppData"), "Roblox\\Versions", current_version)

        if not os.path.exists(r_path):
            return "ERROR: Failed to find ROBLOX executable"

        roblox_executable_path = os.path.join(r_path, "RobloxPlayerBeta.exe")

        arguments = ""


        arguments = f"--app -t {ticket} -j \"https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame{'' if not job_id else 'Job'}&placeId={self.placeId}{'' if not job_id else '&gameId=' + job_id}&isPlayTogetherGame=false\""
        
        if platform.system() == "Windows":
            subprocess.Popen([roblox_executable_path, arguments])
        
        return "Success"
