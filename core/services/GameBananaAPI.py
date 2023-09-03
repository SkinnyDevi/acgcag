import json
import requests
from urllib import parse
from pathlib import Path
from observable import Observable

ENDPOINT = "https://api.gamebanana.com/Core/Item/Data"


class GameBananaAPI:
    """
    API Class for requesting mod information from GameBanana.
    """

    @staticmethod
    def mod_from_url(url: str):
        parsed_uri = parse.urlparse(url)
        url_path = parsed_uri.path.split("/")
        del url_path[0]
        itemtype = url_path[0]
        itemid = url_path[1]

        if itemtype != "mods":
            raise RuntimeError("GameBanana post is not a mod")

        request_url = ENDPOINT + GameBananaAPI.__encode_params(
            itemid=itemid,
            itemtype="Mod",
            fields="name,Game().name,Nsfw().bIsNsfw(),RootCategory().name,Category().name,Files().aFiles()",
        )
        response = requests.get(request_url).json()
        return ModPost(itemid, response)

    @staticmethod
    def __encode_params(**kwargs):
        return f"?{parse.urlencode(kwargs, quote_via=parse.quote)}"


class ModPost:
    class Download:
        def __init__(self, download: dict, mod_info: "ModPost"):
            self._id: int = download["_idRow"]
            self._file_name: str = download["_sFile"]
            self._file_size: int = download["_nFilesize"]
            self._count: int = download["_nDownloadCount"]
            self._url: str = download["_sDownloadUrl"]
            self._mod_info: ModPost = mod_info
            self._dl_obs = Observable()

        @property
        def dl_id(self):
            return self._id

        @property
        def file_name(self):
            return self._file_name

        @property
        def file_size(self):
            self._file_size

        @property
        def dl_count(self):
            return self._count

        @property
        def url(self):
            return self._url

        @property
        def dl_obs(self):
            return self._dl_obs

        def download(self):
            dl_path = Path(f"acgcag_mods/{self._mod_info.itemid}")
            dl_path.mkdir()

            self.__download_mod_file(dl_path)
            self.__create_info_file(dl_path)

        def __create_info_file(self, mod_path: Path):
            file_path = mod_path.joinpath(f"{self._file_name}.json")

            data = self._mod_info.to_dict()
            data["file_name"] = self._file_name
            data["download_count"] = self._count
            data["download_url"] = self._url

            with open(file_path, "w") as f:
                f.write(json.dumps(data))

        def __download_mod_file(self, mod_path: Path):
            file_path = mod_path.joinpath(self._file_name)

            file_request = requests.get(self._url, stream=True)
            chunk_size = 65536

            with open(file_path, "wb") as mod:
                chunks = 0
                for chunk in file_request.iter_content(chunk_size):
                    chunks += chunk_size
                    self._dl_obs.trigger("mod_chunk_update", chunks / self._file_size)
                    mod.write(chunk)

            self._dl_obs.trigger("mod_dl_complete")

    def __init__(self, itemid: str, response: list):
        self._itemid: str = itemid
        self._mod_name: str = response[0]
        self._game: str = response[1]

        if self._game != "Genshin Impact":
            raise ValueError("Mod was not made for Genshin Impact")

        self._nsfw: bool = response[2]
        self._super_category: str = response[3]
        self._sub_category: str = response[4]

        self._downloads: list[self.Download] = []

        if response[3] is not None:
            self._downloads: list[self.Download] = [
                ModPost.Download(d, self.__download_info())
                for d in response[5].values()
            ]

    @property
    def itemid(self):
        return self._itemid

    @property
    def mod_name(self):
        return self._mod_name

    @property
    def nsfw(self):
        return self._nsfw

    @property
    def super_category(self):
        return self._super_category

    @property
    def sub_category(self):
        return self._sub_category

    @property
    def character(self):
        return self._sub_category if self._super_category == "Skins" else None

    def __download_info(self):
        info = [
            self._mod_name,
            self._game,
            self._nsfw,
            self._super_category,
            self._sub_category,
        ]
        return ModPost(self._itemid, info)

    def to_dict(self):
        return {
            "itemid": self._itemid,
            "mod_name": self._mod_name,
            "nsfw": self._nsfw,
            "character": self.character,
        }
