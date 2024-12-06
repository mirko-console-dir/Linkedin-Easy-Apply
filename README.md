# EasyApply-Linkedin

With this tool you can easily automate the process of applying for jobs on LinkedIn!

## Setup

    open terminal navigate to the project folder
    fire up anaconda
    To ensure that the environment variables and settings associated with a particular virtual environment are properly loaded into your current terminal session
    for Zsh sheell

    source ~/.zshrc

    for Bash sheell

    source ~/.bashrc

         Windows:

        check your virtual env in powershell
        echo %VIRTUAL_ENV%

        cd path\to\your\name_virtualenv

        Activate the envoirment with powershell

        .\Scripts\Activate.ps1

    create an envoirment to isolate project dependencies and ensure that your project runs smoothly without conflicts with other Python packages installed on your system

    Check your python version to ensure that is installed

    python -V

    Create a new virtual env called selenium_py

    conda create -n selenium_py python=3.9.7

    then run the following command to use the envoirment

    conda activate selenium_py

    It is gonna ask to download some packeges type Y

      conda create: This part of the command instructs Conda to create a new virtual environment.

    -n selenium_py: -n is used to specify the name of the new virtual environment, which in this case is "selenium_py."

    python3.9.7 : This specifies the Python version for the new environment. In this case, Python 3.9.7 will be installed as the default Python interpreter within the "selenium_py" virtual environment.


    then run:
    conda activate selenium_py
    the directory of the new env is gonna appear like this
    (selenium_py) nameUser@nameUser Linkedin-Easy-Apply
    before was
    (base) nameUser@nameUser Linkedin-Easy-Apply

    conda install selenium
    Y

    1. Selenium requires a driver to interface with the chosen browser. Make sure the driver is in your path, you will need to add your `driver_path` to the `config.json` file.

    I used the Chrome driver, you can download it [here](https://sites.google.com/chromium.org/driver/?pli=1).
    Click on downloads and find your version or tipy on google chrome driver your_version

    If you don't know the version do you have click on the 3 vertical buttons next to your chrome profile icon, then help and about

    After download the zip file Create a Folder in the main project folder called driver and past the put the unzip chrome driver

    You can also download [Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/), [Firefox](https://github.com/mozilla/geckodriver/releases) or [Safari](https://webkit.org/blog/6900/webdriver-support-in-safari-10/). Depends on your preferred browser.

    config the json file config.json

    Import the ChromeService from selenium.webdriver.chrome.service to properly configure the Chrome WebDriver service.

### Usage

Fork and clone/download the repository and change the configuration file with:

- Your email linked to LinkedIn.
- Your password.
- Keywords for finding specific job titles fx. Machine Learning Engineer, Data Scientist, etc.
- The location where you are currently looking for a position.
- The driver path to your downloaded webdriver.

Run `python main.py`.

Please feel free to comment or give suggestions/issues.

**RPA Robotic Process Automation:**

    Handle high volume repetable tasks

**Selinium**

    Framework wester web application

**Explaination code functionality**

login_email = self.driver.find_element_by_name('session_key') finds an HTML element on the page with the name attribute set to 'session_key' and assigns it to the login_email variable.
login_email.clear() clears any existing text within the login_email input field.
After clearing the field, you can use .send_keys() to enter new text into it. For example:

login_email = self.driver.find_element_by_name('session_key')
login_email.clear()
login_email.send_keys('your_email@example.com')

**To bypass linkedin sospictius activity**

linkedin insert a enter the code sent to your email for suspicius activity, to bypass it allow in your browser cookies third part and when we are login verify the chapca manually than all is done the script is gonna keep to be run

**Set up Linkedin Account for apply**
Profile Icon
Security and Privacy
Data Privacy
Job seeking preferences -> Job Application Settings -> Upload a resume and ability to share and Save uploaded resumes and answers to application questions

**FIREFOX & CHROME**
Due to speed priority I change to Firefox driver more faster than Chrome
