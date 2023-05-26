import requests
from tqdm import tqdm
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
        response = requests.get(video_ref, stream=True)
        total_size = int(response.headers.get('Content-Length', 0))

        with open(download_path, 'wb') as file:
            with tqdm(total=total_size, unit='B', unit_scale=True) as progress_bar:
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    progress_bar.update(len(data))

        print("Video downloaded successfully!")
    else:
        print("Failed to retrieve video download link.")


if __name__ == '__main__':
    # sample url 1: "https://www.tiktok.com/@muhammadzahid340/video/6918687903329701121"
    # sample url 2: "https://www.tiktok.com/@zaryab_tiger/video/7221456453595352325?q=zaryab%20tiger&t=1684527181611"
    # sample url 3: blah

    video_url = input('url: ')
    output_path = "downloads/video_3.mp4"
    download_video(video_url, output_path)
