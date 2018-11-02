#!/bin/bash
cd /root/mhzx_forum
git pull
uwsgi --reload /tmp/mhzx.pid