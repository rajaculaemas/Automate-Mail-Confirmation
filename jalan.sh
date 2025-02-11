#!/bin/bash

# Menampilkan pesan bahwa kedua proses sedang dijalankan
echo "Menjalankan API fetcher dan server Flask..."

# Menjalankan api_fetcher.py (akan menampilkan output di terminal)
python3 api_fetcher.py

# Menjalankan confirmation_server.py (akan menampilkan output di terminal)
python3 confirmation_server.py
