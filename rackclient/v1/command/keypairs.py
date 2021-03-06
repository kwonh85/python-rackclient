# Copyright (c) 2014 ITOCHU Techno-Solutions Corporation.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import argparse

from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne

from rackclient import client


def _make_print_data(keypair_id, name, nova_keypair_id, is_default, private_key,
                     gid, user_id, project_id, status=None):
    columns = ['keypair_id', 'name', 'nova_keypair_id', 'is_default',
               'private_key', 'gid', 'user_id', 'project_id']
    data = [keypair_id, name, nova_keypair_id, is_default,
            private_key, gid, user_id, project_id]

    if status is not None:
        columns.append('status')
        data.append(status)

    return columns, data


class ListKeypairs(Lister):
    """
    Print a list of all keypairs in the specified group.
    """
    def __init__(self, app, app_args):
        super(ListKeypairs, self).__init__(app, app_args)

        # When the help command is called,
        # the type of 'app_args' is list.
        if isinstance(app_args, argparse.Namespace):
            self.client = client.Client(app_args.rack_api_version,
                                        rack_url=app_args.rack_url,
                                        http_log_debug=app_args.debug)
            self.gid = app_args.gid

    def take_action(self, parsed_args):
        keypairs = self.client.keypairs.list(self.gid)
        return (
            ('keypair_id', 'name', 'is_default', 'status'),
            ((k.keypair_id, k.name, k.is_default, k.status) for k in keypairs)
        )


class ShowKeypair(ShowOne):
    """
    Show details about the given keypair.
    """
    def __init__(self, app, app_args):
        super(ShowKeypair, self).__init__(app, app_args)

        # When the help command is called,
        # the type of 'app_args' is list.
        if isinstance(app_args, argparse.Namespace):
            self.client = client.Client(app_args.rack_api_version,
                                        rack_url=app_args.rack_url,
                                        http_log_debug=app_args.debug)
            self.gid = app_args.gid

    def get_parser(self, prog_name):
        parser = super(ShowKeypair, self).get_parser(prog_name)
        parser.add_argument('keypair_id', metavar='<keypair-id>',
                            help="Keypair ID")
        return parser

    def take_action(self, parsed_args):
        keypair = self.client.keypairs.get(self.gid,
                                           parsed_args.keypair_id)
        return _make_print_data(
            keypair.keypair_id,
            keypair.name,
            keypair.nova_keypair_id,
            keypair.is_default,
            keypair.private_key,
            keypair.gid,
            keypair.user_id,
            keypair.project_id,
            keypair.status
        )


class CreateKeypair(ShowOne):
    """
    Create a new keypair.
    """
    def __init__(self, app, app_args):
        super(CreateKeypair, self).__init__(app, app_args)

        # When the help command is called,
        # the type of 'app_args' is list.
        if isinstance(app_args, argparse.Namespace):
            self.client = client.Client(app_args.rack_api_version,
                                        rack_url=app_args.rack_url,
                                        http_log_debug=app_args.debug)
            self.gid = app_args.gid

    def get_parser(self, prog_name):
        parser = super(CreateKeypair, self).get_parser(prog_name)
        parser.add_argument('--name', metavar='<name>',
                            help="Name of the new keypair")
        parser.add_argument('--is-default', metavar='<true/false>',
                            default=False,
                            help=("Defaults to the default keypair of"
                                  " the group"))
        return parser

    def take_action(self, parsed_args):
        keypair = self.client.keypairs.create(self.gid, parsed_args.name,
                                              parsed_args.is_default)
        return _make_print_data(
            keypair.keypair_id,
            keypair.name,
            keypair.nova_keypair_id,
            keypair.is_default,
            keypair.private_key,
            keypair.gid,
            keypair.user_id,
            keypair.project_id,
        )


class UpdateKeypair(ShowOne):
    """
    Update the specified keypair.
    """
    def __init__(self, app, app_args):
        super(UpdateKeypair, self).__init__(app, app_args)

        # When the help command is called,
        # the type of 'app_args' is list.
        if isinstance(app_args, argparse.Namespace):
            self.client = client.Client(app_args.rack_api_version,
                                        rack_url=app_args.rack_url,
                                        http_log_debug=app_args.debug)
            self.gid = app_args.gid

    def get_parser(self, prog_name):
        parser = super(UpdateKeypair, self).get_parser(prog_name)
        parser.add_argument('keypair_id', metavar='<keypair-id>',
                            help="Keypair ID")
        parser.add_argument('--is-default', metavar='<true/false>',
                            required=True,
                            help="Defaults to the default keypair of the group")
        return parser

    def take_action(self, parsed_args):
        keypair = self.client.keypairs.update(self.gid,
                                              parsed_args.keypair_id,
                                              parsed_args.is_default)
        return _make_print_data(
            keypair.keypair_id,
            keypair.name,
            keypair.nova_keypair_id,
            keypair.is_default,
            keypair.private_key,
            keypair.gid,
            keypair.user_id,
            keypair.project_id,
        )


class DeleteKeypair(Command):
    """
    Delete the specified keypair.
    """
    def __init__(self, app, app_args):
        super(DeleteKeypair, self).__init__(app, app_args)

        # When the help command is called,
        # the type of 'app_args' is list.
        if isinstance(app_args, argparse.Namespace):
            self.client = client.Client(app_args.rack_api_version,
                                        rack_url=app_args.rack_url,
                                        http_log_debug=app_args.debug)
            self.gid = app_args.gid

    def get_parser(self, prog_name):
        parser = super(DeleteKeypair, self).get_parser(prog_name)
        parser.add_argument('keypair_id', metavar='<keypair-id>',
                            help="Keypair ID")
        return parser

    def take_action(self, parsed_args):
        self.client.keypairs.delete(self.gid, parsed_args.keypair_id)
