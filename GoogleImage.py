import argparse
import json
import os
import urllib
import urllib.request
from PIL import Image
import io
from bs4 import BeautifulSoup
import requests
import cv2
import numpy as np


class GoogleImage(object):
    def __init__(self):
        self.GOOGLE_SEARCH_URL = "https://www.google.co.jp/search"
        self.session = requests.session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) \
                    Gecko/20100101 Firefox/10.0"
            }
        )

    def search(self, keyword, maximum):
        print(f"Begining searching {keyword}")
        query = self.query_gen(keyword)
        return self.image_search(query, maximum)

    def query_gen(self, keyword):
        # search query generator
        page = 0
        while True:
            params = urllib.parse.urlencode(
                {"q": keyword, "tbm": "isch", "ijn": str(page)}
            )

            yield self.GOOGLE_SEARCH_URL + "?" + params
            page += 1

    def image_search(self, query_gen, maximum):
        results = []
        total = 0
        while True:
            # search
            html = self.session.get(next(query_gen)).text
            soup = BeautifulSoup(html, "lxml")
            elements = soup.select(".rg_meta.notranslate")
            jsons = [json.loads(e.get_text()) for e in elements]
            image_url_list = [js["ou"] for js in jsons]

            # add search results
            if not len(image_url_list):
                print("-> No more images")
                break
            elif len(image_url_list) > maximum - total:
                results += image_url_list[: maximum - total]
                break
            else:
                results += image_url_list
                total += len(image_url_list)

        print("-> Found", str(len(results)), "images")
        return results

def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


def main():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument("-t", "--target", help="target name", type=str, required=True)
    parser.add_argument(
        "-n", "--number", help="number of images", type=int, required=True
    )
    parser.add_argument(
        "-d", "--directory", help="download location", type=str, default="./data"
    )
    parser.add_argument(
        "-f",
        "--force",
        help="download overwrite existing file",
        type=bool,
        default=False,
    )

    args = parser.parse_args()

    data_dir = args.directory
    target_name = args.target

    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(os.path.join(data_dir, target_name), exist_ok=args.force)

    google = GoogleImage()

    # search images
    results = google.search(target_name, maximum=args.number)

    # download
    download_errors = []
    for i, url in enumerate(results):
        print("-> Downloading image", str(i + 1).zfill(4), end=" ")
        try:
            urllib.request.urlretrieve(
                url,
                os.path.join(*[data_dir, target_name, str(i + 1).zfill(4) + ".jpg"]),
            )
            print("successful")
        except BaseException:
            print("failed")
            download_errors.append(i + 1)
            continue

    print("-" * 50)
    print("Complete downloaded")
    print("├─ Successful downloaded", len(results) - len(download_errors), "images")
    print("└─ Failed to download", len(download_errors), "images", *download_errors)

def main_test():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument("-t", "--target", help="target name", type=str, required=True)
    parser.add_argument(
        "-n", "--number", help="number of images", type=int, required=True
    )
    parser.add_argument(
        "-d", "--directory", help="download location", type=str, default="./data"
    )
    parser.add_argument(
        "-f",
        "--force",
        help="download overwrite existing file",
        type=bool,
        default=False,
    )

    args = parser.parse_args()

    target_name = args.target

    google = GoogleImage()

    # search images
    results = google.search(target_name, maximum=args.number)
    print(results)
    f = io.BytesIO(urllib.request.urlopen(results[0]).read())
    img = Image.open(f)
    img = pil2cv(img)
    cv2.imshow('frame', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)



if __name__ == "__main__":
    # main()
    main_test()