import os, requests

T = os.environ["BOT_TOKEN"]
CHAT = os.environ["CHAT_ID"]
api = f"https://api.telegram.org/bot{T}"

requests.get(f"{api}/deleteWebhook")
offset = None
sent = 0

while True:
    params = {"allowed_updates": '["channel_post"]', "limit": 100}
    if offset:
        params["offset"] = offset
    updates = requests.get(f"{api}/getUpdates", params=params).json()["result"]
    if not updates:
        break
    for u in updates:
        offset = u["update_id"] + 1
        p = u.get("channel_post")
        if not p:
            continue
        doc = p.get("document", {})
        is_video = "video" in p or doc.get("mime_type", "").startswith("video/")
        if is_video:
            requests.post(f"{api}/copyMessage", data={
                "chat_id": CHAT,
                "from_chat_id": p["chat"]["id"],
                "message_id": p["message_id"],
            })
            sent += 1

if offset:  # подтверждаем, что обновления обработаны
    requests.get(f"{api}/getUpdates", params={"offset": offset})
print("Отправлено видео:", sent)