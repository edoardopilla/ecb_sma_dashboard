# The Survey of Monetary Analysts Aggregate Dashboard

Enable user-friendly visualizations of SMA data, as published by European Central Bank staff at https://www.ecb.europa.eu/stats/ecb_surveys/sma/html/index.en.html

To run the dashboard:

1) Clone the repository by opening Git Bash to the desired location and typing:
   ```
   git clone https://github.com/edoardopilla/ecb_sma_dashboard 
   ```

2) Set up a new environment using ecb_sma_dashboard.yml by opening the Conda terminal and typing:

   ```
   conda env create -f ecb_sma_dashboard.yml
   ```

   (Assuming that ecb_sma_dashboard.yml is moved to default terminal path, i.e. C:/Users/YOUR_NAME)

3) Activate the newly defined environment by typing:

   ```
   conda activate ecb_sma_dashboard
   ```

   in the Conda terminal.

4) Download the correct version of chromedriver.exe from https://googlechromelabs.github.io/chrome-for-testing/#stable by checking your Chrome browser version (Open a new Chrome webpage, click on the vertical dots on the top right, click on 'Information on Chrome' on the bottom left and the version information will be displayed on top of the page)

5) Define the parameters as listed in ecb_sma_dash_user_params.py, noting that scrape_data_flag shall always be True for the first run after having cloned the repository:

   ```
   scrape_data_flag = True

   custom_driver_path = 'C:/Users/YOUR_NAME/chromedriver.exe'

   ```

   (Assuming that chromedriver.exe is mvoed to C:/Users/YOUR_NAME)

6) Run the file app.py from terminal or from your preferred IDE.

The dashboard is normally hosted at localhost:8050