# LLM Watch Expert

LLM Watch Expert is a system that scrapes watch information from Amazon stores, providing detailed insights into various watches. It allows users to explore watches, view images, prices, and ratings, and read customer reviews. Additionally, users can interact with an LLM-powered chatbot to ask detailed questions about watch features.

## Features
-   **Watch Scraping**: The system scrapes watch data including title, image, price, rating, and customer reviews from Amazon stores using Selenium and Beautiful Soup.
-   **LLM Interaction**: Users can interact with a powerful language model (Meta-LLAMA3 8b) to inquire about specific features of a watch.
-   **User Interface**: On the watch details page, a chat option is available for users to ask queries about watches and get precise, informative answers.
-   **Real-Time Data**: The system continually updates its watch database, ensuring the latest information is available.
-   **Filtering Data**: Users can filter based on models, rating, price and other parameters.

## Technologies Used
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
    `git clone https://github.com/yourusername/llm-watch-expert.git
    cd llm-watch-expert`

2.  Create and activate a Python virtual environment:

    `python3 -m venv venv
    source venv/bin/activate`

3.  Install the required dependencies:

    `pip install -r requirements.txt`

4.  Set up PostgreSQL:

    -   Ensure PostgreSQL is installed and running on your machine.
    -   Create a database for storing scraped watch data and customer reviews.
    -   Update the database connection details in the `.env` file.
5.  Scrape Watch Data:

    -   Run the scraping script to gather watch data from Amazon:

        `python scrape_watches.py`

6.  Run the Flask App:

    `flask run`

## Usage
Once the Flask app is running:

1.  Navigate to `http://localhost:5000` in your browser.
2.  Browse through the available watches, view detailed information on each, including price, rating, and reviews.
3.  On the watch details page, use the built-in chat feature to ask specific questions about the watch. The integrated Meta-LLAMA3 8b model will provide accurate responses.

Example Interaction
On the watch details page:

-   User: *"What is the water resistance of this watch?"*
-   LLM Response: *"This watch has a water resistance of up to 50 meters, making it suitable for swimming and light water activities."*



## Contact

For any inquiries or support, feel free to reach out via email: your.email@example.com.
