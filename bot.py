import os
import random
import string
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import NetworkProfile, NetworkInterfaceReference, OSProfile, \
    HardwareProfile, StorageProfile, StorageAccountTypes, VirtualMachine, CachingTypes
from msrestazure.azure_exceptions import CloudError
import discord


DISCORD_TOKEN = 'tokenhere'
SUBSCRIPTION_ID = 'YOUR_SUBSCRIPTION_ID'
CLIENT_ID = 'YOUR_AZURE_CLIENT_ID'
CLIENT_SECRET = 'YOUR_AZURE_CLIENT_SECRET'
TENANT_ID = 'YOUR_AZURE_TENANT_ID'
LOCATION = 'southindia'  


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def create_compute_client():
    credentials = ServicePrincipalCredentials(
        client_id=CLIENT_ID,
        secret=CLIENT_SECRET,
        tenant=TENANT_ID
    )
    return ComputeManagementClient(credentials, SUBSCRIPTION_ID)


def create_virtual_machine(username, admin_password, ram_size, vcpu_size, storage_size):
    compute_client = create_compute_client()
    resource_group = f'{username}-rg'
    network_interface_name = f'{username}-nic'
    vm_name = f'{username}-vm'
    compute_client.resource_groups.create_or_update(resource_group, {'location': LOCATION})
    network_interface_params = {
        'location': LOCATION,
        'ip_configurations': [{
            'name': 'MyIPConfig',
            'subnet': {'id': f'/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{resource_group}/providers/Microsoft.Network/virtualNetworks/{resource_group}-vnet/subnets/default'}
        }]
    }
    network_interface = compute_client.network_interfaces.create_or_update(resource_group, network_interface_name, network_interface_params).result()
    vm_params = {
        'location': LOCATION,
        'os_profile': OSProfile(
            computer_name=vm_name,
            admin_username=username,
            admin_password=admin_password,
            windows_configuration={
                'enable_automatic_updates': True,
                'patch_settings': {'patch_mode': 'AutomaticByOS'},
                'additional_unattend_content': [{
                    'pass': 'oobesystem',
                    'component': 'Microsoft-Windows-Shell-Setup',
                    'setting_name': 'FirstLogonCommands',
                    'content': '<FirstLogonCommands>\n' +
                               '  <SynchronousCommand wcm:action="add">\n' +
                               '    <CommandLine>cmd.exe /c netsh advfirewall firewall add rule name="RDP" dir=in action=allow protocol=TCP localport=3389</CommandLine>\n' +
                               '    <Description>Open RDP Port</Description>\n' +
                               '    <Order>1</Order>\n' +
                               '    <RequiresUserInput>false</RequiresUserInput>\n' +
                               '  </SynchronousCommand>\n' +
                               '</FirstLogonCommands>'
                }]
            }
        ),
        'hardware_profile': HardwareProfile(vm_size=f'Standard_{vcpu_size}vCPUs_{ram_size}GB'),
        'storage_profile': StorageProfile(
            image_reference={
                'publisher': 'MicrosoftWindowsServer',
                'offer': 'WindowsServer',
                'sku': '2022-datacenter',
                'version': 'latest'
            },
            os_disk={
                'create_option': 'FromImage',
                'caching': CachingTypes.none,
                'managed_disk': {
                    'storage_account_type': StorageAccountTypes.standard_lrs
                },
                'disk_size_gb': storage_size
            }
        ),
        'network_profile': NetworkProfile(
            network_interfaces=[NetworkInterfaceReference(id=network_interface.id)]
        )
    }

    try:
        compute_client.virtual_machines.create_or_update(resource_group, vm_name, VirtualMachine(vm_params))
        return True
    except CloudError as e:
        print(f'Error creating virtual machine: {e}')
        return False
bot = discord.Client()

@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.event
async def on_message(message):
    if message.content.startswith('!createvm'):
        args = message.content.split()

        if len(args) != 6:
            await message.reply('Invalid command format. Usage: !createvm <username> <password> <ram_size> <vcpu_size> <storage_size>')
            return

        username = args[1]
        admin_password = args[2]
        ram_size = args[3]
        vcpu_size = args[4]
        storage_size = args[5]

        result = create_virtual_machine(username, admin_password, ram_size, vcpu_size, storage_size)

        if result:
            await message.reply(f'Virtual machine for {username} created successfully!')
        else:
            await message.reply(f'Error creating virtual machine for {username}.')


# Run the bot
bot.run(DISCORD_TOKEN)
