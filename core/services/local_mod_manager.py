import json
import os
import stat
from pathlib import Path
from PIL import Image

from core.utils import MultiExtensionExtractor
from core.services.gamebanana_api import MAIN_SITE


class LocalModManager(object):
    mod_path = Path("acgcag_mods")

    def __init__(self, mods: list["LocalMod"] = None):
        self._mods = mods or self.__default_mods()

    def refresh(self, mods: list["LocalMod"] = None):
        self._mods = mods or self.__default_mods()

    def __default_mods(self):
        id_sorted = sorted(LocalModManager.mod_path.glob("*"), key=lambda x: x.stem)
        return [LocalMod(modid.stem) for modid in id_sorted]

    @property
    def mods(self):
        return self._mods


class LocalMod:
    def __init__(self, mod_id: str):
        mod_path = LocalModManager.mod_path.joinpath(mod_id)
        mod_info = self.__load_mod_info_file(mod_path, mod_id)

        self._itemid: str = mod_info["itemid"]
        self._name: str = mod_info["mod_name"]
        self._nsfw: bool = mod_info["nsfw"]
        self._character: str = mod_info["character"]
        self._preview_image_url: str = mod_info["preview_image_url"]
        self._mod_file: Path = mod_path.joinpath(mod_info["file_name"])
        self._local_preview_file: Path = mod_path.joinpath(
            mod_info["local_preview_file"]
        )
        self._download_url: str = mod_info["download_url"]
        self._mod_page: str = f"{MAIN_SITE}/mods/{mod_id}"

    def __load_mod_info_file(self, path: Path, id: str) -> dict:
        with open(path.joinpath(f"{id}.json"), "r") as f:
            return json.load(f)

    @property
    def itemid(self):
        return self._itemid

    @property
    def name(self):
        return self._name

    @property
    def nsfw(self):
        return self._nsfw

    @property
    def character(self):
        return self._character

    @property
    def preview_image_url(self):
        return self._preview_image_url

    @property
    def mod_preview_image(self):
        image = Image.open(self._local_preview_file)
        _, height = image.size

        image = image.crop((20, 0, 170, 3 * height / 5))
        image = image.resize((110, 110))

        return image

    @property
    def is_installed(self):
        return Path(f"3dmigoto/Mods/{self._itemid}").exists()

    def install(self):
        extractor = MultiExtensionExtractor(self._mod_file, self._itemid)
        extractor.extract()

    def uninstall(self):
        path = Path(f"3dmigoto/Mods/{self._itemid}")

        if path.exists():
            self.__super_rmtree(path)

    def delete(self):
        if self.is_installed:
            self.uninstall()

        mod_path = Path(f"acgcag_mods/{self._itemid}")
        self.__super_rmtree(mod_path)

    def __super_rmtree(self, path: Path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                filename = os.path.join(root, name)
                os.chmod(filename, stat.S_IWUSR)
                os.remove(filename)
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)
