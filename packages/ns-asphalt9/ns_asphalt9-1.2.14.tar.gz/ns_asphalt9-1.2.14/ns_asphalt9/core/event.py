import requests


class Event(object):
    def __init__(self) -> None:
        self.s = requests.Session()
        self.url = "https://unedge.myds.me:28080/api/tracking/update"

    def update(self, name: str, content: dict = None) -> None:
        if not content:
            content = {}
        try:
            data = {
                "name": name,
                "content": content,
            }
            r = self.s.post(self.url, json=data)
        except Exception as err:
            pass


event = Event()


if __name__ == "__main__":
    track = Event()
    track.update(name="test", content={"a": 1})
