from netmiko import ConnectHandler

class AutoNet:
    """
    A class to automate network operations.
    """

    def __init__(self, device_type: str, ip: str, username: str, password: str, secret: str):
        """
        Initialize AutoNet with the necessary credentials.

        :param device_type: The type of the device.
        :param ip: The IP address of the device.
        :param username: The username for authentication.
        :param password: The password for authentication.
        :param secret: The secret for authentication.
        """
        self.connection = ConnectHandler(device_type=device_type, ip=ip, username=username, password=password, secret=secret)

    def send_command(self, command: str) -> str:
        """
        Send a command to the device.

        :param command: The command to send.
        :return: The output of the command.
        """
        return self.connection.send_command(command)

    def send_config_set(self, config_commands: list) -> str:
        """
        Send a set of configuration commands to the device.

        :param config_commands: The list of configuration commands to send.
        :return: The output of the commands.
        """
        return self.connection.send_config_set(config_commands)

    def close_connection(self) -> None:
        """
        Close the network connection.
        """
        self.connection.disconnect()

    def disable_paging(self) -> None:
        """
        Disable paging on the device.
        """
        self.connection.send_command('terminal length 0')

    def enable_paging(self) -> None:
        """
        Enable paging on the device.
        """
        self.connection.send_command('terminal length 30')

    def is_alive(self) -> bool:
        """
        Check if the network connection is alive.

        :return: True if the connection is alive, False otherwise.
        """
        return self.connection.is_alive()

    def save_config(self) -> None:
        """
        Save the current configuration on the device.
        """
        self.connection.save_config()
