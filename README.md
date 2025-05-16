# trckd
A Magic the Gathering collection tracking and analysis tool. A CITS3403 - Agile Web Development Project.

## 🌟 Project Overview

**trckd** allows users to:
- Create a personal account within the app
- Add new cards (obtained via the Scryfall API) to a personal collection
- View, search, and sort through their collection
- Track cards by name, type, colour, rarity, etc.
- Visualise collection insights (e.g. rarity distribution, card colour breakdown, price changes, etc.)
- Share their collection with others

## 👥 Team Members
| Student ID |       Name       | GitHub Username  |
|------------|------------------|------------------|
| 24371251   | J-Ern Sia        | @jern2004        |
| 23761044   | Dan Clayton      | @KingTako44      |
| 24042324   | Saniya Chawla    | @Saniya14-skectch|
| 23630652   | Zac Doruk Maslen | @mas-ruk         |

## 🧰 Tech Stack
- **Frontend**: HTML, CSS, Bootstrap, WTForms, JavaScript, jQuery
- **Backend**: Python Flask
- **Database**: SQLite via SQLAlchemy

## 🚀 Running the Application
1. Unzip the repository file and cd into it through your terminal.
2. Install the required packages by running `pip install -r requirements.txt` in your terminal. (NOTE: in some cases, running this command may print an error message telling you to run a different command. If this happens, run that command instead.)
3. Run the Flask app using the command `flask run`.
4. Open the webpage by navigating to `http://127.0.0.1:5000` in a web browser of your choice (the link should be printed in the terminal).

## 🧪 Running the Tests
1. Ensure you are in the top-level directory of the repository (i.e. you can see the `app` directory when you run the `ls` command).
2. Ensure you have installed the required packages by running `pip install -r requirements.txt` in your terminal.
3. Ensure you have Google Chrome installed.
4. Run the tests using the command `python -m unittest run_test.py` - test results will be printed to the terminal.

## 🗓️ Sprint Logs
- [Sprint 1](docs/sprints/sprint1.md)
- [Sprint 2](docs/sprints/sprint2.md)
- [Sprint 3](docs/sprints/sprint3.md)

## References
In regard to AI, various tools including that of ChatGPT, Claude AI, and GitHub Copilot were all utilised in this project. It was used in multiple cases throughout the project including that of breaking down Scryfalls API querying functionality, assisting in the production of the dynamic_search.js file as well as various bug fixes and head-scratching issues. It was also utilised in our documentation in the means of fleshing out our ideas and providing achieveable, maintable goals. 


