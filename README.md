# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/rafkha12/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/rafkha12/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A program that writes one image summing up the world's news of Wednesday 18 November 2026.

## Run it

```sh
python3 main.py
```

## How it works

`build_image.py` draws `image.png` (1024x1024) with PIL: a newspaper front
page with the day's five biggest stories — Iran's strikes on US bases in
Kuwait and Bahrain, Xi and Putin meeting in Shenzhen, Ukraine hitting the
Kerch Bridge, Peltola winning Alaska, and Voyager 1 reaching one light-day —
plus an "Also today" strip. `main.py` copies that image to
`/output/entry.png`, so the entry is deterministic and needs no network.
