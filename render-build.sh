#!/usr/bin/env bash
# 這是 Render 的安裝腳本
apt-get update
apt-get install -y chromium chromium-driver
pip install -r requirements.txt