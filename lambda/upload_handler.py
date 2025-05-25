import json
import base64
from urllib.request import Request, urlopen
from requests_toolbelt.multipart import decoder
import json
from urllib.request import Request, urlopen

def parse_form_data(event):
    content_type = event["headers"].get("Content-Type") or event["headers"].get("content-type")
    body = base64.b64decode(event["body"]) if event.get("isBase64Encoded", False) else event["body"]

    form = decoder.MultipartDecoder(body, content_type)

    image_bytes = None
    model_id = None

    for part in form.parts:
        cd = part.headers.get(b"Content-Disposition", b"").decode()
        if 'name="image"' in cd:
            image_bytes = part.content
        elif 'name="model"' in cd:
            model_id = part.content.decode()

    return image_bytes, model_id


def query_huggingface(image_bytes, model_id, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream"
    }

    req = Request(
        url=f"https://api-inference.huggingface.co/models/{model_id}",
        data=image_bytes,
        headers=headers
    )

    with urlopen(req) as res:
        raw = res.read().decode()
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print("JSON decode failed:", e)
            print("Raw response from Hugging Face:", raw)
            return {"raw_output": base64.b64encode(raw.encode()).decode()}
