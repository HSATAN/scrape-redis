# coding=utf8
from redis import Redis

tt = Redis()

with open('sound_url.txt') as f:
    for line in f:
        tt.sadd('mzhan:start_urls', line.strip('\n') )