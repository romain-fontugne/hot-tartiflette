import requests
import sys

if len(sys.argv) < 2:
    print("usage: %s asn" % sys.argv[0])
    sys.exit()

asn = int(sys.argv[1])
url = "http://ihr.iijlab.net/ihr/api/delay_alarms/?asn=%s" % asn

while url is not None:
    resp = requests.get(url)
    if (resp.ok):
        data = resp.json()
        for res in data["results"]:
            print(",".join(
                [res["timebin"], res["link"], str(res["diffmedian"]), str(res["deviation"]), str(res["nbprobes"])]
                ))

        if "next" in data:
            url = data["next"]
        else:
            url = None
    else:
        resp.raise_for_status()
