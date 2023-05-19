import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from urllib.request import urlopen


def downloadVideo(link, id):
    print(f"Downloading video {id} from: {link}")

    # Get the cookies and headers from the TikTok website
    cookies = {}
    headers = {}

    # Make a request to the TikTok website to get the download link
    response = requests.post('https://ssstik.io/abc', params={'url': link}, cookies=cookies, headers=headers)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]
    videoTitle = downloadSoup.p.getText().strip()

    # Save the video
    mp4File = urlopen(downloadLink)
    with open(f"videos/{id}-{videoTitle}.mp4", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break


def main():
    # Get the TikTok video URL
    video_url = "https://www.tiktok.com/@muhammadzahid340/video/6918687903329701121"

    # Open a Chrome browser
    driver = webdriver.Chrome()
    driver.get(video_url)

    # Scroll down to the bottom of the page
    scroll_pause_time = 1
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if (screen_height) * i > scroll_height:
            break

    # Get the video links
    soup = BeautifulSoup(driver.page_source, "html.parser")
    videos = soup.find_all("div", {"class": "tiktok-yz6ijl-DivWrapper"})

    # Download the videos
    for index, video in enumerate(videos):
        print(f"Downloading video: {index}")
        downloadVideo(video.a["href"], index)
        time.sleep(10)


if __name__ == "__main__":
    main()
