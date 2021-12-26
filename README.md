# Automated Monthly Contribution Bot

Discord bot created to automate tracking and recording of 150 - 200 monthly contributors each month for the Index Coop. 

Technologies:

Python
SQL
Discord API
Google Cloud API
Google Sheets API

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


