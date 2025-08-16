## Chatbot [Ryzenth]

[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/TeamKillerX/xv)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-green)](https://github.com/TeamKillerX/xv/graphs/commit-activity)
[![License](https://img.shields.io/badge/License-MIT-pink)](https://github.com/TeamKillerX/xv/blob/main/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/TeamKillerX/xv/main.svg)](https://results.pre-commit.ci/latest/github/TeamKillerX/xv/main)


![Image](public/xv.jpg)

## ⚠️ Warning: Blacklist Policy

- Using pirated or unauthorized repositories will result in **permanent blacklist**.  
- Hugging Face and other platforms may also restrict your access.  
- Even **Telegram API** can blacklist your bot if violations are detected.  

> Example: Tried using an invalid bot token connection failed.

## HF Secrets
```env
API_ID=0
API_HASH=""
BOT_TOKEN=""
MONGO_URL=""
GEMINI_API_KEY=""
```

Don't put secrets in **.env** or hardcode them in the image (it will leak) save them in hugging face secrets or another safe place.

## Dockerfile (Hugging Face)
- Hosting Unlimited Free
1. Go to [`huggingface.co`](https://huggingface.co/)
2. Click ➕ New
3. New Space
4. Select the Space SDK: Docker
5. Choose a Docker template: blank
6. Then add `Dockerfile` (only)

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

<div align="center">

### 🌟 Star us on GitHub if you find this project useful!

[![GitHub stars](https://img.shields.io/github/stars/TeamKillerX/xv?style=social)](https://github.com/TeamKillerX/xv)
[![GitHub forks](https://img.shields.io/github/forks/TeamKillerX/xv?style=social)](https://github.com/TeamKillerX/xv/fork)
[![GitHub watchers](https://img.shields.io/github/watchers/TeamKillerX/xv?style=social)](https://github.com/TeamKillerX/xv)

</div>
