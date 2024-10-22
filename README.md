# LLM Watch Expert

LLM Watch Expert is a system that scrapes watch information from Amazon stores, providing detailed insights into various watches. It allows users to explore watches, view images, prices, and ratings, and read customer reviews. Additionally, users can interact with an **LLM-powered chatbot** to ask detailed questions about watch features.

## Features
-   **Watch Scraping**: The system scrapes watch data including title, image, price, rating, and customer reviews from Amazon stores using Selenium and Beautiful Soup.
-   **LLM Interaction**: Users can interact with a powerful language model (Meta-LLAMA3 8b) to inquire about specific features of a watch.
-   **User Interface**: On the watch details page, a chat option is available for users to ask queries about watches and get precise, informative answers.
-   **Real-Time Data**: The system continually updates its watch database, ensuring the latest information is available.
-   **Filtering Data**: Users can filter based on models, rating, price and other parameters.

## Technologies / Hardwares Used
-   **Backend**:
    -   Python 3.11
    -   Flask
    -   Meta-LLAMA3-8b for ChatBot
-   **Web Scraping**:
    -   Selenium
    -   Beautiful Soup
-   **Frontend**:
    -   HTML, CSS, JavaScript for the user interface
-   **Database**: PostgreSQL for storing watch data and customer reviews
-   **Hardware Requirement**: Minimum GPU with 8GB VRAM for running the LLM.

## Installation
To set up the LLM Watch Expert on your local machine:

1.  Clone the repository:
    
    `git clone https://github.com/rukon-uddin/LLM-watch-expert.git`
    
    `cd LLM-watch-expert`

2.  Create and activate a conda environment:

    `conda create --name myenv python==3.11 pytorch-cuda==12.1 pytorch cudatoolkit xformers -c pytorch -c nvidia -c xformers -y`

    `conda activate myenv`

3.  Install the required dependencies:

    `pip install -r requirements.txt`

4.  Set up PostgreSQL:

    -   Ensure PostgreSQL is installed and running on your machine.
    -   Create a database for storing scraped watch data and customer reviews.
    -   Table informations are provided in the helper.txt.

## Usage
Follow the steps to run the system

1.  First you have to run the scraping which will scrap and store in your databset.
    
    `python scrapAmazonWatch.py`

2.  Second you have to run the LLM api.
    
    1. To run the LLama API you first need to download the model file [Download Link](https://drive.google.com/file/d/1iaQPzWBt-0D-Ot_xFZIxzHgvXrabuBGF/view?usp=sharing). 
    
    2. Extract the zip file and store it inside models directory

    3. Run `python llama_api.py`

3.  Finally run `python app.py`


## Contact

For any inquiries or support, feel free to reach out via email: your.email@example.com.
