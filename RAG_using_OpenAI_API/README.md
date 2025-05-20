### Steps to Run the Q\&A System Project

Follow these steps in order to set up and run the project:

### Navigate to the Project Folder:

* Open a terminal on the Raspberry Pi.
* Go to the project directory.

**Command:**

```bash
cd project
```

### Install Virtual Environment:

* Create a virtual environment named `venv` in the project folder.

**Command:**

```bash
python3 -m venv venv
```

### Activate Virtual Environment:

* Activate the virtual environment to isolate project dependencies.

**Command:**

```bash
source venv/bin/activate
```

### Install Required Libraries:

* Install the necessary Python libraries for the project.

**Command:**

```bash
pip install openai mysql-connector-python python-dotenv
```

### Set Up .env File with API Key:

* Create or edit the `.env` file to store the OpenAI API key.
* Open the `.env` file in a text editor.

**Command:**

```bash
nano .env
```

* Add the following line, replacing `your_key_here` with your actual OpenAI API key:

```
OPENAI_API_KEY=your_key_here
```

* Save and exit (in nano, press **Ctrl+O**, **Enter**, then **Ctrl+X**).

### Run `main.py`:

* Run the main program to start the Q\&A system.

**Command:**

```bash
python3 main.py
```

* Expect the welcome message:
  **“Welcome to the College Q\&A System! Ask about student GPA, fees, or general topics. Type 'quit' to exit.”**

* Test by asking:

  * **“What is Peter Pandey’s GPA in semester 1?”**
    *(should return “Peter Pandey's GPA in semester 1 is 3.70.”)*

  * **“What is the capital of France?”**
    *(should return “The capital of France is Paris.”)*

* Type **“quit”** to exit.
