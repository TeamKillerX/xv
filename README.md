## Chatbot [Ryzenth]

![Image](public/xv.jpg)

## HF Secrets
```env
API_ID=0
API_HASH=""
BOT_TOKEN=""
```

Don't put secrets in **.env** or hardcode them in the image (it will leak) save them in hugging face secrets or another safe place.

## Dockerfile (Hugging Face)
- Hosting Unlimited Free
1. Go to [`huggingface.co`](https://huggingface.co/)
2. Click ➕ New
3. New Space
4. Select the Space SDK: Docker
5. Choose a Docker template: blank
6. Create files `Dockerfile` (only)

Enjoy Done 😎

If using [`uptimerobot`](https://uptimerobot.com) for cron job anti mode sleep

Add url `https://{username}-{repo}.hf.space/status` in uptimerobot

```Dockerfile
# syntax=docker/dockerfile:1.4
FROM python:3.10-slim

RUN apt-get update && apt-get install -y git \
    && git clone https://github.com/TeamKillerX/xv.git /app \
    && cd /app \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apt-get remove -y git \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

EXPOSE 7860

ENTRYPOINT ["sh", "-c", "python3 server.py & python3 -m xv"]
```

## Made By Solo Dev
- **[xtdevs](https://t.me/xtdevs)** - Lead Developer & Creator
- **[Kurigram](https://github.com/KurimuzonAkuma/pyrogram/tree/dev/pyrogram)** - Kurigram

## 📄 License

**MIT License © 2025 Ryzenth Developers from TeamKillerX**

This project is open source and available under the [MIT License](https://github.com/TeamKillerX/xv/blob/main/LICENSE).
