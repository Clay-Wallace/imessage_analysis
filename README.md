# iMessage Analysis

iMessage Analysis is a MacOS terminal script which generates an analysis report of your iMessage data.

## Project Overview

In the digital age, text message data serves as the most robust repository of interpersonal communications available for historical review, often spanning many years with content ranging from casual to professional communication. With iMessage Analysis, you can generate insights from your text messages within minutes. Using iMessage data stored on your Mac computer, iMessage analysis generates a report that displays your messaging habits, describes your communication style, and examines how your communication tendencies vary between message recipients. 

## Features

- (Must have) Generates a PDF or HTML report analyzing iMessage data, inclduing:
    - (Must Have) Statistical Overview (message figures, unique conversations, sent vs recieved, etc.)
    - (Must Have) Habit Overview (temporal analysis, message length, media, etc.)
    - (Must Have) Social Network (summary and habit data for top correspondents)
        - (Nice to Have) Network analysis vizualization of correspondent mentions and group chat inclusion
    - (Should Have) Rhetoric Analysis (AI-driven analysis of rhetorical style and emotional disposition)
        - (Nice to have) Rhetorical analysis of correspondance with top correspondents
- (Nice to Have) CLI interface allowing customization of report information (toggle sections, index specific correspondents for inclusion, select output format, etc.)

## Installation

1. Download repository
2. Ensure Python 3.x is installed
3. Generate OpenAI API key
4. Launch terminal and type "python3 [filepath]/imessage_analysis.py"
5. Follow the instructions in the terminal to generate report

## Credits

- Created by Clay Wallace
- Rhetoric Analysis and code-generation assistance powered by GPT
- Ideation and technical assistance from Professor Mark Johson
- iMessage and Contacts app data retrieval code adapted from Gold, K. (2023, July 27). Extract iMessage Data For Analytics and Conversational AI projects. Better Programming. https://medium.com/better-programming/extracting-imessage-and-address-book-data-b6e2e5729b21