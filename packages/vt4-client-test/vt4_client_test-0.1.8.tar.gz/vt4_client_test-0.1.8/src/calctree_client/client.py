import json
import ssl
from urllib import request


class CalctreeClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def run_calculation(self, page_id, ct_cells):
        url = "https://api.calctree.com/api/calctree-cell/run-calculation"
        headers = {
            "x-api-key": self.api_key,  # local
            "content-type": "application/json"
        }
        body = {
            "pageId": page_id,
            "ctCells": ct_cells

        }
        data = json.dumps(body).encode("utf8")
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = request.Request(url, data, headers)
        res = request.urlopen(req, context=ctx)
        output = res.read()

        if if 200 <= res.status  <= 299::
            return json.loads(output)
        else:
            raise Exception(f"Error-: {res.status_code}, {res.text}")
