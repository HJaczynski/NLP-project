# NLP-project
Regular project - traffic accident news analysis – automatic  understanding of news articles

The goal is to extract information concerning accidents: 
- Exact place where it occurred.
- When did it occur?
- What kinds of vehicles were involved?
- How many causalities were the consequences of an accident? What was their age?
- How many persons were injured? 
- What was the reason for the accident?
- Sequence of actions (if applicable).

The project will consist of the following elements:
1. Data acquisition module
2. Data processing module
3. GUI application

The GUI needs to have two features:
1. Display and filter data saved in the CSV file that is the output of data processing mode.
2. Access the website via hyperlinks, process and display data.

Use cases for the GUI application
- I can filter accidents by the publication date of the news article that contained its description.
The application displays only these accidents that are within a specified date range. The default behaviour is to display all. 
- I can zoom in and zoom out the map. The application displays only information concerning accidents within selected regions. 
The default behaviour is to display the map of Dhaka and all accidents in a visible rectangle. If time will be an issue, you may leave the map as a static component.
- Each detected accident will be displayed as a pin on the map, upon clicking more information is revealed. 
Information can be displayed as a box extending from the pin, on the map, movable with a mouse or in some side panel.

Deadlines
April 23rd, 2024 – intermediate deadline. Required advancement:
- data acquisition must be completed;
- complete GUI, information to be displayed can be mocked at this point;
- data processing module should be completed in 25%;
May 28th, 2024 – project presentation. Required advancement: the entire 
programming work must be completed in 95%. 
June 11th, 2024 – project submission (via email as a link to OneDrive folder with 
project to be downloaded). The submission includes the project and its documentation. 
Documentation should cover in detail the algorithm for information extraction. 
Analysis of quality and properties of text processing. The project must contain a readme 
file with instructions on how to run it.
