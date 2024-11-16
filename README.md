# Thesis Topic Selection System

## Project Overview

This project aims to provide a simple and user-friendly platform for obtaining and displaying graduation thesis topic information. Due to the complexity and lack of intuitiveness of the thesis topic selection system provided by a certain website, this system uses a Python web scraper to collect thesis topic information from the website and presents it through a clean and simple front-end interface.

## Features

- **Data Crawling**: A Python-based web scraper that automatically retrieves thesis topic information.
- **Frontend Display**: A simple and intuitive HTML page that displays the scraped thesis topic data.
- **Configuration Management**: The system uses a `config.json` file to store environment variables required by the scraper (such as cookies and auth tokens), ensuring that the scraper runs smoothly.

## Project Structure

```
.
├── config.json       # Stores environment variables for the scraper, such as cookie and auth token
├── crawl.py          # Python script that crawls thesis topic information from the website
├── index.html        # Simple front-end page to display the scraped thesis topic data
├── README.md         # Project description file
```

## Installation and Configuration

### 1. Install Dependencies

First, ensure that you have Conda installed on your system.

Navigate to the location where the source code is downloaded:

```shell
cd .../where_source_download/
```

Create a new Python environment:

```shell
conda create -n myEnv python
```

Install the necessary Python packages:

```shell
conda install requests
```

### 2. Configure `config.json`

The `config.json` file contains environment variables required for the scraper to run (such as cookies, auth tokens, and user agents). Ensure that this file is correctly configured. Example:

```json
{
  "COOKIE": "your_cookie_here",
  "AUTH_TOKEN": "your_auth_token_here",
  "USER_AGENT": "your_user_agent_here"
}
```

Replace `your_cookie_here`, `your_user_agent_here`, and `your_auth_token_here` with the valid information obtained from the website.

### 3. Run the Scraper

After configuring the environment variables, run the scraper script to collect thesis topic data:

```bash
python crawl.py
```

Once the scraper has successfully run, the thesis topic information will be stored in a local JSON file. You can view the data via the `index.html` page.

### 4. View Frontend Display Page

Open the `index.html` file in a browser to view the displayed thesis topic information.

## Usage Instructions

1. **Data Updates**: Every time the scraper script is run, it will automatically fetch the latest thesis topic data and update the local storage.
2. **Frontend Display**: By opening the `index.html` file, you can view a simple display of the thesis topics, making it easy to browse and choose the desired topic.

## Project Mockups

### Original Thesis Topic Page

- The original website's thesis topic page is quite complex, making it difficult to quickly find the desired topic information.

### Frontend Display Page (This Project)

- This project provides a clean and intuitive display interface that helps users quickly browse and select a suitable thesis topic.

## Contributions

We welcome suggestions or contributions to this project. You can participate in the following ways:

1. Fork the repository and submit a Pull Request.
2. Submit an Issue to report bugs or propose new features.

## Acknowledgments

Thanks to the website for providing thesis topic data, and thanks to the open-source community for the tools and support provided for this project.

---

### Project Display Mockups

Here, you can provide screenshots or mockups to help users better understand how the project works.

---

## Additional Notes

### Web Scraping Legal Disclaimer

This project is intended solely for educational and research purposes. Please comply with relevant laws and intellectual property regulations. Unauthorized use of the scraper in production environments or for commercial purposes is prohibited.

