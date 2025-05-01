# import custom user parameters
import ecb_sma_dash_user_params

# pass user parameters from imported file
user_custom_driver_path = ecb_sma_dash_user_params.custom_driver_path

user_custom_scrape_data_flag = ecb_sma_dash_user_params.scrape_data_flag

# import necessary libraries
from bs4 import BeautifulSoup
from dash import Dash, dcc, html, Input, Output, State
from pathlib import Path
from plotly.subplots import make_subplots
from PyPDF2 import PdfReader
from selenium import webdriver
from selenium.webdriver.common.by import By

import ctypes
import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import requests
import time

# define ECB color palette
ecb_colormap = {'ecb_blue': '#003299',
                'yellow': '#FFB400',
                'orange': '#FF4B00',
                'light_green': '#65B800',
                'cyan': '#00B1EA',
                'dark_green': '#007816',
                'purple': '#8139C6',
                'dark_gray': '#5C5C5C',
                'ecb_blue_2': '#98A1D0',
                'yellow_2': '#FDDDA7',
                'orange_2': '#F6B183',
                'light_green_2': '#CEE1AF',
                'cyan_2': '#D7EEF8',
                'dark_green_2': '#8DB58D',
                'purple_2': '#AE97C7',
                'gray': '#A9A9A9'}

# define ECB chart element color palette
ecb_chart_elem_colormap = {'grid': '#D9D9D9',
                           'labels': '#535353',
                           'axes': '#7D7D7D'}

# define ecb logo path
ecb_header_logo = 'assets/logo-ecb-resized.png'

# define name appearing in browser tab
browser_tab_name = 'The SMA at a glance'

# define dashboard header name
dash_header_name = 'The Survey of Monetary Analysts Aggregate Dashboard'

# define error message to be displayed when callbacks params are missing
display_error_msg = 'Enter all required parameters using the dropdown menus to output the figure correctly.'

# get scale factor that depends on zoom level of display to normalize figure size
scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

# get PPI from active window
ppi = ctypes.windll.user32.GetDpiForWindow(ctypes.windll.user32.GetForegroundWindow())

# set width and height for standalone figures in cm
width_standalone_cm = 30
height_standalone_cm = 12

# set width and height for coupled figures in cm
width_coupled_cm = 15
height_coupled_cm = 12

# define class to prepare dataset
class ecb_sma_scraper:
    def __init__(self,
                 chromedriver_path = user_custom_driver_path,
                 ecb_root_url = 'https://www.ecb.europa.eu',
                 ecb_govc_url = '/press/calendars/mgcgc/html/index.en.html',
                 ecb_sma_url = '/stats/ecb_surveys/sma/html/all-releases.en.html'):
        
        self.chromedriver_path = chromedriver_path
        self.ecb_root_url = ecb_root_url
        self.ecb_govc_url = ecb_govc_url
        self.ecb_sma_url = ecb_sma_url

        self.scrape_flag = None
        self.sma_data_full = None
        self.reference_data = None
        self.respondent_data = None

    def scrape_sma_data(self,
                        scrape_data = False):

        # create data folder if necessary
        Path("data").mkdir(parents = True,
                           exist_ok = True)

        # if scraping
        if scrape_data:

            # initialize ChromeService
            serv = webdriver.ChromeService(executable_path = self.chromedriver_path)

            # initialize ChromeOptions
            opts = webdriver.ChromeOptions()

            #opts.add_argument('--headless')
            opts.add_argument("start-maximized")

            # add detach option to prevent garbage collection leading to browser page closing automatically
            opts.add_experimental_option("detach", True)

            # initialize Chrome with set chromedriver path and options
            driver = webdriver.Chrome(service = serv,
                                      options = opts)

            # access SMA page on ECB website
            driver.get(url = self.ecb_root_url + self.ecb_govc_url)

            # sleep for 3 seconds
            time.sleep(3)

            # click on reject cookies button
            driver.find_element(By.CSS_SELECTOR,
                                "button.cross.linkButton.linkButtonLarge.floatRight.highlight-medium").click()

            # Get the page source
            page_source = driver.page_source

            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')

            # close driver
            driver.close()

            # sleep for 3 seconds
            time.sleep(3)

            # extract all date tags from soup
            date_tags = soup.findAll("dt")

            dates_notags = [re.search(r'<dt> \t\n(.*?)\n</dt>', str(elem)).group(1) for elem in date_tags]

            # extract titles linked to dates from soup
            titles_tags = soup.findAll("dd")

            titles_notags = [re.search(r'<dd>        \n(.*?)<br/>\n</dd>', str(elem)).group(1) for elem in titles_tags]

            df_cal = pd.concat([pd.Series(dates_notags), pd.Series(titles_notags)], axis = 1)
            df_cal = df_cal.rename(columns = {0: 'date', 1: 'title'})

            # find first index of title matching desired pattern to identify upcoming governing council press conference
            df_cal_govc = df_cal[(df_cal.title.str.startswith('Governing Council of the ECB: monetary policy meeting')) & (df_cal.title.str.endswith('followed by press conference'))].reset_index(drop = True)

            next_release = df_cal_govc.date[0]

            # convert to datetime and format to parse month first, as format from GovC schedule is
            # different from that of SMA schedule
            next_release = pd.to_datetime(next_release,
                                          format = '%d/%m/%Y',
                                          utc = True)

            # add 4 days as SMA is scheduled to be released on Monday after GovC
            next_release = next_release + pd.Timedelta(days = 4)

            # convert to Europe/Amsterdam timezone
            next_release = (next_release + pd.Timedelta(hours = 8)).tz_convert('Europe/Amsterdam')

            # initialize Chrome with set chromedriver path and options
            driver = webdriver.Chrome(service = serv,
                                      options = opts)

            # access SMA page on ECB website
            driver.get(url = self.ecb_root_url + self.ecb_sma_url)

            # sleep for 3 seconds
            time.sleep(3)

            # click on reject cookies button
            driver.find_element(By.CSS_SELECTOR,
                                "button.cross.linkButton.linkButtonLarge.floatRight.highlight-medium").click()

            # Get the page source
            page_source = driver.page_source

            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')

            # close driver
            driver.close()

            # extract all date tags from soup
            date_tags = soup.findAll("div", {"class": "date"})

            # extract latest date as string from previously defined tag array
            latest_release = re.search(r'<div class="date">(.*?)</div>', str(date_tags[0])).group(1)

            # convert to datetime for Europe/Amsterdam timezone
            latest_release = pd.to_datetime(latest_release + ' 08:00', utc = True).tz_convert('Europe/Amsterdam')

            # define current time as update check
            last_update = pd.to_datetime(time.time(),
                                         unit = 's',
                                         utc = True).tz_convert('Europe/Amsterdam')

            # write dates to csv for update recommendation when not scraping
            ref_data = pd.DataFrame([[latest_release, next_release, last_update]],
                                    columns = ['latest_release', 'next_release', 'last_update'])

            # write reference data to csv for update recommendation when not scraping
            ref_data.to_csv('data/reference_data.csv',
                            index = False)

            # store reference data as attribute
            self.reference_data = ref_data

            # define empty list to store csv file URLs
            csv_urls = []

            # for each download CSV button, get and store URL
            for link in soup.find_all('a', class_ = 'csv'):
                csv_url = link.get('href')
                csv_urls.append(self.ecb_root_url + csv_url)

            # create empty dataframe to store individual dataframes
            sma_dump_full = pd.DataFrame()

            # for each stored URL, read file into a pandas dataframe and append to previous
            for sma_csv_url in csv_urls:
                sma_data = pd.read_csv(sma_csv_url)
                sma_dump_full = pd.concat([sma_dump_full, sma_data], axis = 0)

            # reset index
            sma_dump_full = sma_dump_full.reset_index(drop = True)

            # store full dataset in local drive
            sma_dump_full.to_csv('data/sma_dump_full.csv',
                                 index = False)

            # store full dataset in object instance
            self.sma_data_full = sma_dump_full

            # define URL to request PDF content
            url_resps_lst = 'https://www.ecb.europa.eu/stats/ecb_surveys/sma/shared/pdf/ecb.sma_survey_respondents.en.pdf'

            # request PDF file
            resp_resps_lst = requests.get(url = url_resps_lst, timeout = 120)

            # parse request object into pdfreader-readable content
            resps_lst_cont = io.BytesIO(resp_resps_lst.content)

            # read PDF content
            resps_lst_pdf = PdfReader(resps_lst_cont)

            # index first page of PDF
            resps_lst_pag = resps_lst_pdf.pages[0]

            # extract text from PDF, replace empty spaces from raw text with newlines, drop additional text elements
            resps_lst = resps_lst_pag.extract_text().replace('  ', '\n').split('\n')[10:]

            # drop empty strings and whitespace strings
            resps_lst_noblank = [resp for resp in resps_lst if len(resp) > 1]

            # sort case-insensitive, not robust to locale language conventions as per https://stackoverflow.com/questions/36139/how-to-sort-a-list-of-strings
            resps_lst_noblank_sort = sorted(resps_lst_noblank, key = str.lower)

            # store respondents in dataframe
            resps_df = pd.DataFrame()

            # define length of sublist for each column of respondents
            len_sublst = 15

            # define number of iterations to generate columns of length 15
            batches = round(len(resps_lst_noblank_sort) / len_sublst)

            # loop over batches to fill dataframe columns
            for i in range(batches):
                resps_df = pd.concat([resps_df, pd.Series(resps_lst_noblank_sort[(i * len_sublst):((i + 1) * len_sublst)])], axis = 1)

            # replace last two missing values with '' as loop expects 75 values, while 73 participants exist
            resps_df = resps_df.fillna('')

            # rename columns
            resps_df.columns = ['col_0', 'col_1', 'col_2', 'col_3', 'col_4']

            # store respondent data in local drive
            resps_df.to_csv('data/respondent_data.csv', index = False)

            # store respondent df in object instance
            self.respondent_data = resps_df

            return
        
        # if NOT scraping
        else:
            # store full dataset in object instance
            self.sma_data_full = pd.read_csv('data/sma_dump_full.csv')

            # store reference data in object instance
            self.reference_data = pd.read_csv('data/reference_data.csv',
                                              parse_dates = ['latest_release', 'next_release', 'last_update'])

            # store respondent data in object instance, replace once again NaNs as reading csv yields them
            # tried to pass na_values = [''] but not working, hence used fillna('') again
            self.respondent_data = pd.read_csv('data/respondent_data.csv').fillna('')

            return