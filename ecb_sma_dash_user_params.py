# define scrape_data_flag to pass into instance of ecb_sma_scraper within ecb_sma_dash_utils.py
# should always be True on first run after cloning repository
scrape_data_flag = True

# define desired path to chromedriver to pass into instance of ecb_sma_scraper within ecb_sma_dash_utils.py
# below defined for Chromedriver downloaded to C:/Users/YOUR_NAME
# if experiencing version conflict between Chrome and chromedriver.exe, check that versions match
# by opening Chrome web page -> vertical dots (top right) -> Information on Chrome (bottom left)
# and in case download appropriate version of chromedriver.exe at
# https://googlechromelabs.github.io/chrome-for-testing/#stable
custom_driver_path = 'C:/Users/YOUR_NAME/chromedriver.exe'