import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def download_video(url, download_path):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://en.savefrom.net/")

    input_field = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.NAME, "sf_url"))
    )
    input_field.clear()
    input_field.send_keys(url)

    download_button = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.NAME, "sf_submit"))
    )
    download_button.click()

    download_link = WebDriverWait(driver, 20).until(
        ec.presence_of_element_located((By.CLASS_NAME, "link-download"))
    )
    video_ref = download_link.get_attribute("href")
    driver.quit()

    if video_ref:
        response = requests.get(video_ref)
        if response.status_code == 200:
            with open(download_path, 'wb') as file:
                file.write(response.content)
            print("Video downloaded successfully!")
        else:
            print("Failed to download video.")
    else:
        print("Failed to retrieve video download link.")


if __name__ == '__main__':
    # Example usage
    video_url = "https://www.tiktok.com/@muhammadzahid340/video/6918687903329701121"
    output_path = "downloads/video.mp4"
    download_video(video_url, output_path)
