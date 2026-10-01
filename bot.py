import os, requests

T = os.environ["BOT_TOKEN"]
CHAT = os.environ["CHAT_ID"]
api = f"https://api.telegram.org/bot{T}"

print("webhook:", requests.get(f"{api}/getWebhookInfo").json()["result"].get("url") or "нет")
requests.get(f"{api}/deleteWebhook")

offset = None
sent = 0
total = 0

while True:
    params = {"allowed_updates": '["channel_post"]', "limit": 100}
    if offset:
        params["offset"] = offset
    data = requests.get(f"{api}/getUpdates", params=params).json()
    if not data.get("ok"):
        print("Ошибка getUpdates:", data)
        break
    updates = data["result"]
    if not updates:
        break
    for u in updates:
        total += 1
        offset = u["update_id"] + 1
        p = u.get("channel_post")
        if not p:
            continue
        doc = p.get("document", {})
        if "video" in p or doc.get("mime_type", "").startswith("video/"):
            r = requests.post(f"{api}/copyMessage", data={
                "chat_id": CHAT,
                "from_chat_id": p["chat"]["id"],
                "message_id": p["message_id"],
            }).json()
            print("copyMessage:", r)
            if r.get("ok"):
                sent += 1

if offset:
    requests.get(f"{api}/getUpdates", params={"offset": offset})
print(f"Получено обновлений: {total}, отправлено видео: {sent}")