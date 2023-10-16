from subprocess import call
import submit_wg
import json
import os.path
import time
from datetime import datetime

fname = "wg_offer.json"


def scrape_site():
    call(
        [
            "scrapy",
            "crawl",
            "wg-gesucht",
            "-o",
            "wg_offer.json",
            "-s",
            "LOG_ENABLED=false",
        ]
    )

    with open("wg_offer.json") as data_file:
        data = json.load(data_file)
    data_list = list(set([i["data-id"] for i in data]))

    if not os.path.isfile("wg_offer_old.json"):
        call(["cp", "wg_offer.json", "wg_offer_old.json"])

    with open("wg_offer_old.json") as data_old_file:
        data_old = json.load(data_old_file)
    data_old_list = list(set([i["data-id"] for i in data_old]))

    return data_list, data_old_list


while True:
    if os.path.isfile(fname):
        if os.path.isfile("wg_offer_old.json"):
            with open("wg_offer_old.json") as data_old_file:
                data_old = json.load(data_old_file)

        else:
            data_old = []

        with open("wg_offer.json") as data_file:
            data = json.load(data_file)

        data.extend(data_old)
        unique = set([tuple(d.items()) for d in data])
        unique_data = [dict(pairs) for pairs in unique]
        with open("wg_offer_old.json", "w") as data_old_file:
            json.dump(unique_data, data_old_file)
        call(["rm", fname])
    data, data_old = scrape_site()

    if os.path.isfile("wg_blacklist.json"):
        with open("wg_blacklist.json") as blacklist:
            blacklist = json.load(blacklist)
        blacklist = list(set([i["data-id"] for i in blacklist]))
        print("Blacklist: ", blacklist)
    else:
        blacklist = []

    diff_id = list(set(data) - set(data_old) - set(blacklist))
    with open("wg_sent_request.dat", "a") as sent, open("wg_diff.dat", "a") as diff:
        if len(diff_id) != 0:
            print(len(diff_id), "new offers found")
            print("New offers id:", diff_id)
            print("Time: ", datetime.now())
            for new in diff_id:
                print("Sending message to: ", new)
                submit_wg.submit_app(new)
                sent.write("ID: %s \n" % new)
                sent.write(str(datetime.now()) + "\n")
                diff.write(str(new) + "\n")
        else:
            print("No new offers.")
            print("Time: ", datetime.now())
    time.sleep(60)
