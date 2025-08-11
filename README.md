## Chatbot [Ryzenth]

![Image](public/xv.jpg)

## HF Secrets
```env
API_ID=0
API_HASH=""
BOT_TOKEN=""
```

## Dockerfile (Hugging Face)
```Dockerfile
# syntax=docker/dockerfile:1.4
FROM python:3.10-slim

RUN apt-get update && apt-get install -y git \
    && git clone https://github.com/TeamKillerX/chatbot-ryzenth.git /app \
    && cd /app \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apt-get remove -y git \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

EXPOSE 7860

ENTRYPOINT ["sh", "-c", "python3 server.py & python3 -m xv"]
```

Don't put secrets in **.env** or hardcode them in the image (it will leak) save them in hugging face secrets or another safe place.

## Made By Solo Dev
- **[xtdevs](https://t.me/xtdevs)** - Lead Developer & Creator
- **[Kurigram](https://github.com/KurimuzonAkuma/pyrogram/tree/dev/pyrogram)** - Kurigram

## 📄 License

**MIT License © 2025 Ryzenth Developers from TeamKillerX**

This project is open source and available under the [MIT License](https://github.com/TeamKillerX/xv/blob/main/LICENSE).
