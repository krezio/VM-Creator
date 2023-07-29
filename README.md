# Azure VM Creation Bot
* This Discord bot allows you to create virtual machines (VMs) on Microsoft Azure using a simple command. It automates the process & allows certain configurations.

___
## Prerequisites
Before using the bot, please make sure you have the following:

- Azure subscription
- Azure Subscription ID, Client ID, Client Secret, and Tenant ID.
- Discord bot token
- A brain

___
## Setup

1. Clone the repo
`git clone https://github.com/your-username/vm-creation-discord-bot.git`

2. Install the required dependencies:
* `cd vm-creation-discord-bot`
* `pip install -r requirements.txt`
* `pip install -r requirements.txt`

3. Open the bot.py file and replace the placeholder values for Azure credentials and Discord Bot Token with your own credentials.

4. Run the bot through `python bot.py`

___
## Usage
The command format to create a VM is:
**!createvm** `<username>` `<password>` `<ram>` `<cpu>` `<storage>`
* `<username>`: The desired username for the VM.
* `<password>`: The password for the administrator account.
* `<ram>`: The RAM size in gigabytes for the VM.
* `<cpu>`: The number of virtual CPUs (vCPUs) for the VM.
* `<storage>`: The storage size in gigabytes for the VM.

For example, to create a VM with 32GB RAM, 4 vCPUs, and 128GB storage, you would use the following command:
- `!createvm johnsmith P@ssw0rd123 32 4 128`

If your VM requires futher configurations, modification of the code will be required.