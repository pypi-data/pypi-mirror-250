import argparse

from hacktegic._internal.commands.assets.cidr.create import AssetsCIDRCreateCommand
from hacktegic._internal.commands.assets.cidr.delete import AssetsCIDRDeleteCommand
from hacktegic._internal.commands.assets.cidr.describe import AssetsCIDRDescribeCommand
from hacktegic._internal.commands.assets.cidr.list import AssetsCIDRListCommand
from hacktegic._internal.commands.assets.cidr.update import AssetsCIDRUpdateCommand
from hacktegic._internal.commands.auth.login import LoginCommand
from hacktegic._internal.commands.auth.logout import LogoutCommand
from hacktegic._internal.commands.auth.register import RegisterCommand
from hacktegic._internal.commands.config.get import ConfigGetCommand
from hacktegic._internal.commands.config.set import ConfigSetCommand
from hacktegic._internal.commands.projects.create import ProjectsCreateCommand
from hacktegic._internal.commands.projects.delete import ProjectsDeleteCommand
from hacktegic._internal.commands.projects.describe import ProjectsDescribeCommand
from hacktegic._internal.commands.projects.list import ProjectsListCommand
from hacktegic._internal.commands.projects.update import ProjectsUpdateCommand
from hacktegic._internal.commands.scanprofiles.create import ScanProfilesCreateCommand
from hacktegic._internal.commands.scanprofiles.delete import ScanProfilesDeleteCommand
from hacktegic._internal.commands.scanprofiles.describe import ScanProfilesDescribeCommand
from hacktegic._internal.commands.scanprofiles.list import ScanProfilesListCommand
from hacktegic._internal.commands.scanprofiles.update import ScanProfilesUpdateCommand
from hacktegic._internal.commands.scanprofiles.assets_cidr_list import ScanProfilesAssetCIDRListCommand
from hacktegic._internal.commands.scanprofiles.assets_cidr_attach import ScanProfilesAssetCIDRAttachCommand
from hacktegic._internal.commands.scanprofiles.assets_cidr_detach import ScanProfilesAssetCIDRDetachCommand

class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_arguments(self):
        subparsers = self.add_subparsers()

        # Authentication commands
        self._setup_auth_commands(subparsers)

        # Project commands
        self._setup_project_commands(subparsers)

        # Configuration commands
        self._setup_config_commands(subparsers)

        # Asset CIDR commands
        self._setup_asset_commands(subparsers)

        # Scan Profile commands
        self._setup_scanprofile_commands(subparsers)

    def _setup_auth_commands(self, subparsers):
        auth_parser = subparsers.add_parser("auth", help="authentication commands")
        auth_subparsers = auth_parser.add_subparsers(help="auth sub-command help")

        self._add_command(auth_subparsers, "login", LoginCommand)
        self._add_command(auth_subparsers, "logout", LogoutCommand)
        self._add_command(auth_subparsers, "register", RegisterCommand)

    def _setup_project_commands(self, subparsers):
        projects_parser = subparsers.add_parser("projects", help="project commands")
        projects_subparsers = projects_parser.add_subparsers(
            help="project sub-command help"
        )

        self._add_command(
            projects_subparsers, "create", ProjectsCreateCommand, "project_name"
        )
        self._add_command(
            projects_subparsers, "describe", ProjectsDescribeCommand, "project_id"
        )
        self._add_command(projects_subparsers, "list", ProjectsListCommand)
        self._add_command(
            projects_subparsers,
            "update",
            ProjectsUpdateCommand,
            "project_id",
            "--name",
        )
        self._add_command(
            projects_subparsers, "delete", ProjectsDeleteCommand, "project_id"
        )

    def _setup_config_commands(self, subparsers):
        config_parser = subparsers.add_parser("config", help="config help")
        config_subparsers = config_parser.add_subparsers(help="config sub-command help")

        self._add_command(config_subparsers, "get", ConfigGetCommand, "key")
        self._add_command(config_subparsers, "set", ConfigSetCommand, "key", "value")

    def _setup_asset_commands(self, subparsers):
        assets_parser = subparsers.add_parser(
            "assets", help="asset commands"
        )
        assets_subparsers = assets_parser.add_subparsers(
            help="asset sub-command help"
        )

        self._add_command(
            assets_subparsers,
            "create",
            AssetsCIDRCreateCommand,
            "address",
            "--description",
        )
        self._add_command(assets_subparsers, "list", AssetsCIDRListCommand)
        self._add_command(
            assets_subparsers, "describe", AssetsCIDRDescribeCommand, "asset_id"
        )
        self._add_command(
            assets_subparsers,
            "update",
            AssetsCIDRUpdateCommand,
            "asset_id",
            "--address",
            "--description",
        )
        self._add_command(
            assets_subparsers, "delete", AssetsCIDRDeleteCommand, "asset_id"
        )

    def _setup_scanprofile_commands(self, subparsers):
        scanprofiles_parser = subparsers.add_parser(
            "scanprofiles", help="scanprofiles commands"
        )

        scanprofiles_subparsers = scanprofiles_parser.add_subparsers(
            help="scanprofiles sub-command help"
        )

        self._add_command(
            scanprofiles_subparsers, "create", ScanProfilesCreateCommand, "--title", "--description", "--schedule", "--enabled", "--nmap_options", "--project_id"
        )
        self._add_command(
            scanprofiles_subparsers, "list", ScanProfilesListCommand
        )
        self._add_command(
            scanprofiles_subparsers, "describe", ScanProfilesDescribeCommand, "scanprofile_id"
        )
        self._add_command(
            scanprofiles_subparsers, "update", ScanProfilesUpdateCommand, "scanprofile_id", "--title", "--description", "--schedule", "--enabled", "--nmap_options"
        )
        self._add_command(
            scanprofiles_subparsers, "delete", ScanProfilesDeleteCommand, "scanprofile_id"
        )
        self._add_command(
            scanprofiles_subparsers, "assets_cidr_list", ScanProfilesAssetCIDRListCommand, "scanprofile_id"
        )
        self._add_command(
            scanprofiles_subparsers, "assets_cidr_attach", ScanProfilesAssetCIDRAttachCommand, "scanprofile_id", "assets_cidr_id"
        )
        self._add_command(
            scanprofiles_subparsers, "assets_cidr_detach", ScanProfilesAssetCIDRDetachCommand, "scanprofile_id", "assets_cidr_id"
        )

    def _add_command(self, subparsers, name, command_class, *args):
        parser = subparsers.add_parser(name, help=f"{name} help")
        parser.set_defaults(func=command_class.run)
        for arg in args:
            parser.add_argument(arg, type=str)
