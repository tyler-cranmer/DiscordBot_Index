# Automated Monthly Contribution Bot

Discord bot created to automate tracking and recording of 150 - 200 monthly contributors each month for the Index Coop. This bot allows Index Coops contributors to submit their work for each month. To interact with the bot, you will send a direct message with the appropriate commands. 

This Bot has a SQLite Database to hold each contributors work for the month. At the end of each month, the bot will up date a master google sheet with everyones data. 

Technologies:

- Python
- SQL
- Discord API
- Google Cloud API
- Google Sheets API

## Contributor Commands

#### !newContributor
- Creates new google work sheet.
- Command syntax: !newContributor
#### !submitForm (google sheet url)
- Submits google sheet to database.
- Command syntax: !submitForm (google sheet url) with no brackets
#### !help
- Brings up list of commands
!adminHelp (Administrator only)
- Displays list of Admin controls
If there are any problems with the bot, please DM TeeWhy

## Administrator Commands

#### !activate
- Activates bot for Submissions
#### !deactivate
- Dectivates bot for Submissions
#### !updateMaster
- Updates Master Sheet with current months contribution
#### !changeWallet
- Changes wallet address of user.
- Command syntax: !changeWallet "owlID" "new wallet address"
#### !clearMaster
- Clears Master Sheet Data
#### !adminHelp
- Displays list of Admin controls


