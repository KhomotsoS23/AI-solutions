# Watson-KeyNotes

Watson-KeyNotes is a Flask-based application designed to help users interact with IBM Watsonx.ai using their own API credentials. The app allows users to input their data and retrieve insights powered by IBM Watson's capabilities.



# Instructions for Running the application locally

## Requirements

To run this application, you need the following installed on your system:

- Python 3.11
- Docker
- Git (optional)

**Clone the repository:** 

`git clone https://github.com/KhomotsoS23/AI-Solutions.git 
cd AI-Solutions`

Update the .env file with your own credentials: 

    - SPEECH_TO_TEXT_API_KEY= your_speech_to_text_api_key
    - SPEECH_TO_TEXT_URL= your_speech_to_text_url
    - WATSONX_API_KEY= your_watsonx_api_key
    - WATSONX_URL= your_watsonx_url
    - PROJECT_ID= your_project_id

**Build the Docker image:**

`docker build -t watson-keynotes .`

**Run the Docker container:**

`docker run -p 5000:5000 watson-keynotes`

**Note:** The next time you want to run the application without opening VS just open Docker the run the above command in your local terminal. Use the same link to access the application. 

Access the app on `http://localhost:5000` in your browser.

This is what you should see when you open the application : 

![Reference Image](/images/Screenshot%202024-11-17%20at%2015.20.51.png)

To run the application :
- you can choose the type of input you have (manual text or audio)
- if you choose manual text, you can input your text and click on the "Submit" button to get the insights
- if you choose audio, you can record your audio and click on the "Submit" button to get the insights

# Features

- **Speech-to-Text Conversion:** Convert audio input into text using IBM Watson Speech-to-Text service.
- **Watsonx.ai Integration:** Utilize IBM Watsonx.ai for generating insights and summaries based on the input data.
- **Dockerized Application:** The application is containerized using Docker for easy deployment and scalability.

# Technologies Used

- **Python:** The primary programming language used for the backend of the application.
- **Flask:** A lightweight web framework for building the application's backend.
- **IBM Watson Speech-to-Text:** Used for converting audio input into text.
- **IBM Watsonx.ai:** Leveraged for generating insights and summaries based on the input data.
- **Docker:** Used for containerizing the application for easy deployment and scalability.

# Contact

For any questions or inquiries, please contact [Khomotso Semono](mailto:khomotso.semono@ibm.com).
