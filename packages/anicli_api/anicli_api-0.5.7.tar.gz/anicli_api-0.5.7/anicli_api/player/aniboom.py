import re
from typing import List

from parsel import Selector

from anicli_api.player.base import BaseVideoExtractor, Video, url_validator

__all__ = ["Aniboom"]

_URL_EQ = re.compile(r"https://(www.)?aniboom\.one/")
player_validator = url_validator(_URL_EQ)


class Aniboom(BaseVideoExtractor):
    URL_RULE = _URL_EQ
    DEFAULT_HTTP_CONFIG = {"headers": {"referer": "https://animego.org/"}}
    VIDEO_HEADERS = {
        # KEYS SHOULD BE STARTED IN Title case, else hls/mpd return 403 error
        "Referer": "https://aniboom.one/",
        "Accept-Language": "ru-RU",  # INCREASE DOWNLOAD SPEED with this static value lol
        "Origin": "https://aniboom.one",
    }

    @player_validator
    def parse(self, url: str, **kwargs) -> List[Video]:
        response = self.http.get(url).text
        return self._extract(response)

    @player_validator
    async def a_parse(self, url: str, **kwargs) -> List[Video]:
        async with self.a_http as client:
            response = (await client.get(url)).text
            return self._extract(response)

    def _extract(self, response: str) -> List[Video]:
        # if pre unescape response - parsel selector incorrect get data-parameters attr
        sel = Selector(response)
        jsn = sel.xpath('//*[@id="video"]/@data-parameters')
        # TODO create m3u8, dash URL parsers in another qualities
        videos: List[Video] = []
        if dash := jsn.jmespath("dash"):
            videos.append(
                Video(
                    type="mpd",
                    quality=1080,
                    url=dash.re(r"https:.*\.mpd")[0].replace("\\", ""),
                    headers=self.VIDEO_HEADERS,
                )
            )
        if hls := jsn.jmespath("hls"):
            videos.append(
                Video(
                    type="m3u8",
                    quality=1080,
                    url=hls.re(r"https:.*\.m3u8")[0].replace("\\", ""),
                    headers=self.VIDEO_HEADERS,
                )
            )
        return videos


if __name__ == '__main__':
    links = [
        "https://aniboom.one/embed/PQmM34oXDlG?episode=1&translation=2",
        "https://aniboom.one/embed/PQmM34oXDlG?episode=2&translation=2",
        "https://aniboom.one/embed/PQmM34oXDlG?episode=3&translation=2",
        "https://aniboom.one/embed/PQmM34oXDlG?episode=4&translation=2"
        "https://aniboom.one/embed/PQmM34oXDlG?episode=5&translation=2"
    ]
    for l in links:
        print(*[v.url for v in Aniboom().parse(l)])
# https://evie.yagami-light.com/qv/QVWMB7QAXxD/64395e3f9b286.mpd https://evie.yagami-light.com/qv/QVWMB7QAXxD/master.m3u8
# https://emily.yagami-light.com/38/38kMRQlzqEO/64399ca5a6197.mpd https://emily.yagami-light.com/38/38kMRQlzqEO/master.m3u8
# https://amelia.yagami-light.com/ln/lNmqVWaYMoQ/6441a08661caf.mpd https://amelia.yagami-light.com/ln/lNmqVWaYMoQ/master.m3u8
# https://calcium.yagami-light.com/ln/lNmqVOxlMoQ/645266f77d86f.mpd https://calcium.yagami-light.com/ln/lNmqVOxlMoQ/master.m3u8