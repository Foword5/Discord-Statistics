# Discord Statistics v1.0

Discord allows user to download all the data they collected from you, Using this data, this script create statistics, graphs and more on you.

## Getting started

Follow these instruction to get your own statistics

### Prerequisites

Python 3.x

### Installing

Installing the requirements

```
pip install -r requirements.txt
```

### Downloading the data

To get your discord data, follow these steps : 
1. Go to your "user settings"
2. Go in the "Privacy & Safety" tab
3. At the bottom you will find "Request all of my data"
4. Wait for a couple days to receive the data by email
5. Once you received the data add the unzipped folder to the root of the project

### Running

```
python3 main.py
```

### Configuration

You can edit the result by going in the "config.py" file where you can change the configuration:
- PACKAGE_PATH : the path to your discord data
- NEW_DATA_FOLDER : the path to the new data (csv file, images, ect...)
- FONT : the font you want to use
- REMOVED_PREFIX : a list of prefixes whose messages strating with them will be disgarded (in case you use a bot too often)

## Example

You can find a example of the pdf that is generated by the script [here](ResultExample.pdf).
