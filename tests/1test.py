from scrapers.x1337 import Scraper1337, Params1337, Category1337, Order1337

scraper = Scraper1337()

params = Params1337(
    name="HITMAN",
    category=Category1337.GAMES,
    order_ascending=False
)


results = scraper.find_torrents(params, (1,2,3))
tops = ["fitgirl", "mechanic", "gog", "catalyst", "repack", "dodi", "xatab"]
for torrent in results:
    if any(top in torrent.name.lower() for top in tops) and torrent.seeders > 0:
        scraper.get_torrent_info(torrent)
        print(torrent.name)
        # print(torrent.name, torrent.size, torrent.seeders)