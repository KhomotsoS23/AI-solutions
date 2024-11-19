# Watson-KeyNotes

Watson-KeyNotes is a Flask-based application designed to help users get a comprehensive summary of all the discussion,decision, action items and conclusion of a meeting. The application uses IBM Watson Speech to Text and Watsonx.ai services to transcribe audio files and generate summaries, respectively.


# Instructions for Running the application locally

**Pre-requisites:**

To run this application, you need the following installed on your system:
- Create an IBM Cloud account if you don't have one.
- Install Docker on your machine.
- Install Python 3.11 on your machine.
- Install Git on your machine.

**Clone the repository:** 

Note: run the commands in the terminal or CL of your machine.

```bashh
git clone https://github.com/KhomotsoS23/AI-Solutions.git 
cd AI-Solutions
```
**Update the .env file with your own credentials:** 

**Steps to Edit the `.env` File**
1. **Locate the `.env` File:**
   - After cloning the repository, navigate to the folder where the `.env` file is stored.

2. **Open the `.env` File:**
   - **On Windows:**
     - Use Notepad:
       - Right-click on the `.env` file and select **Open With** > **Notepad**.
     - Use Visual Studio Code (if installed):
       - Right-click on the `.env` file and choose **Open With Code**.

   - **On Mac/Linux:**
     - Use the built-in `nano` editor:
       ```bash
       nano .env
       ```
     - Or open with a GUI editor like TextEdit on macOS or Gedit on Linux.

3. **Edit the File:**
   - Update the values for the environment variables, such as API keys, service URLs, or any other credentials:
     
        - SPEECH_TO_TEXT_API_KEY= your_speech_to_text_api_key
        - SPEECH_TO_TEXT_URL= your_speech_to_text_url
        - WATSONX_API_KEY= your_watsonx_api_key
        - WATSONX_URL= your_watsonx_url
        - PROJECT_ID= your_project_id

**Access your credentials: APIs, URLs and Project_ID**

**a. Watson Speech to Text credentials:**

- Go to IBM Cloud and search for Speech-to-text service, it will open up to this: 

<img src="/images/Screenshot%202024-11-18%20at%2015.49.34.png" width=500px hight=500 >

- Select a location and create a new instance of the service.
- Go to Manage tab and copy the API key and URL and paste it in the `.env` file.

<img src="/images/Screenshot%202024-11-18%20at%2014.56.16.png" width=500px hight=500 >

**b. Watsonx.ai credentials:**
- On IBM Cloud search for Watsonx.ai service and the search will return a list similar to the following. Click watsonx.

<img src="/images/Screenshot%202024-11-18%20at%2019.20.48.png" width=500px hight=500 >

- You will now see the AI and data platform page. click get started on watsonx.ai tile, select location and login with your w3id.
- Watsonx.ai console will open up. Click on the hamburger icon on the top left corner and select project.
- View all projects , select new project and give your project a name and click create.
- select the Chat and build prompts with foundation models tile 
- If asked to associate service, select associate service and the servece provided and click associate.
- Click overview and select the Chat and build prompts with foundation models tile again. 
- Select view code 

<img src="/image/viewcode.png" width=500px hight=500 >

- Select python and copy the code and paste it in the `.env` file.

<img src="/images/Screenshot%202024-11-18%20at%2019.49.08.png" width=500px hight=300 >

- Copy the project_id and url, and paste it in the .env file.

<img src="/images/Watsonx-url&pid.png" width=300px hight=300px >

- Click the huamburger icon on the top left corner and select Access(IAM) under administration :

<img src="/images/Screenshot%202024-11-18%20at%2019.51.59.png" width=200px hight=200px >

- The Manage access and users panel page will open. Find and select the API keys item from the left-hand panel, create a new API key and copy the API key and pase it in the .env file.

<img src="/images/Screenshot%202024-11-18%20at%2019.53.20.png" width=500px hight=500 >

Note: It is recommended that you download your key. This key will be downloaded to
a file called apikey.json. You might want to rename this file to ensure you
remember what it is. If necessary, you can always create another API key.

4. **Save the File:**
   - After editing, save and overwrite. Ensure there are no extra spaces or formatting issues.

Make sure you in the correct dictory before running the below commands.
If not run  `cd AI-Solutions` in the terminal first.

**Build the Docker image:**
```bash
docker build -t watson-keynotes .
```
**Run the Docker container:**
```bash
docker run -p 5000:5000 watson-keynotes
```
**Note:** The next time you want to run the application without opening VS just open Docker the run the above command in your local terminal. Use the same link to access the application, you can even bookmark the link and open it after running the command. 

Access the app on `http://localhost:5000` in your browser.

This is what you should see when you open the application : 

![Reference Image](/images/Screenshot%202024-11-17%20at%2015.20.51.png)

To run the application :
<iframe width="560" height="315" src="/Demo/Watson-Keynotes Demo.mp4" title="Demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

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
