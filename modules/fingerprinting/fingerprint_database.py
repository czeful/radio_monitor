import json 
from pathlib import Path
'''
    в начале думал все записывать в json file но 
    так получилось что файлов и запписей потенциально
    можнет быть очень много по этой причине сразу перешли
    на postgreSql, но на всякий оставил этот файл с json
'''
class FingerprintDatabase:

    def __init__(self, database_path: str):

        self.database_path = Path(database_path)

        if not self.database_path.exists():
            self.database_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )
            with open(self.database_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load(self):
        with open(self.database_path, "r", encoding="utf-8") as f:
            return json.load(f)

    
    def save_song(self, title: str, artist: str, fingerprint:str):
        songs = self.load()

        songs.append(
            {
                "title": title,
                "artist": artist,
                "fingerprint": fingerprint
            }
        )

        with open(self.database_path, "w", encoding="utf-8") as f:
            json.dump(songs, f, ensure_ascii=False, indent=4)
