#!/bin/bash
cd /root/code/mhzx_forum
git pull
uwsgi --reload /tmp/mhzx.pid