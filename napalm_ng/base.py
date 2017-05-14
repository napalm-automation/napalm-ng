# Copyright 2016 Dravetech AB. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

# Python3 support
from __future__ import print_function
from __future__ import unicode_literals

# stdlib
import sys

# local modules
from napalm_ng import exceptions


class BaseNetworkDriver(object):

    def __init__(self, hostname, username, password, **kwargs):
        """
        This is the base class you have to inherit from when writing your own Network Driver to
        manage any device. You will, in addition, have to override most of the methods specified on
        this class. Make sure you follow the guidelines for every method and that you return the
        correct data.

        Args:

            hostname (str): IP or FQDN of the device you want to connect to.
            username (str): Username you want to use
            password (str): Password
            kwargs: Optional arguments that might tweak certain behaviors (see docs)
        """
        raise NotImplementedError

    def __enter__(self):
        """ Do not implement this. """
        try:
            self.open()
        except Exception:
            exc_info = sys.exc_info()
            self.__raise_clean_exception(exc_info[0], exc_info[1], exc_info[2])
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ Do not implement this. """
        self.close()
        if exc_type is not None:
            self.__raise_clean_exception(exc_type, exc_value, exc_traceback)

    @staticmethod
    def __raise_clean_exception(exc_type, exc_value, exc_traceback):
        """
        This method is going to check if the exception exc_type is part of the builtins exceptions
        or part of the napalm exceptions. If it is not, it will print a message on the screen
        giving instructions to fill a bug.

        Finally it will raise the original exception.

        Args:
            exc_type: Exception class.
            exc_value: Exception object.
            exc_traceback: Traceback.

        Raises:
            Exception: The original exception
        """
        if (exc_type.__name__ not in dir(exceptions) and
                exc_type.__name__ not in __builtins__.keys()):
            epilog = ("NAPALM didn't catch this exception. Please, fill a bugfix on "
                      "https://github.com/napalm-automation/napalm/issues\n"
                      "Don't forget to include this traceback.")
            print(epilog)
        # Traceback should already be attached to exception; no need to re-attach
        raise exc_value

    def open(self):
        """
        Opens a connection to the device.

        Raises:
            (we should define here which exception we want to raise and in which cases)
        """
        raise NotImplementedError

    def close(self):
        """
        Closes the connection to the device. If connection is already closed this is a no-op

        Raises:
            (we should define here which exception we want to raise and in which cases)
        """
        raise NotImplementedError

    def is_alive(self):
        """
        Returns a flag with the connection state.
        Depends on the nature of API used by each driver.
        The state does not reflect only on the connection status (when SSH), it must also take into
        consideration other parameters, e.g.: NETCONF session might not be usable, althought the
        underlying SSH session is still open etc.
        """
        raise NotImplementedError

    def load_replace_candidate(self, filename=None, config=None):
        """
        Populates the candidate configuration. You can populate it from a file or from a string.
        If you send both a filename and a string containing the configuration, the file takes
        precedence.
        If you use this method the existing configuration will be replaced entirely by the
        candidate configuration once you commit the changes. This method will not change the
        configuration by itself.

        Args:
            filename (str): Path to the file containing the desired configuration. Defaults to None.
            config (str): String containing the desired configuration. Defaults to None.

        Raises:

            LoadConfigException: If there is an error on the configuration sent.
        """
        raise NotImplementedError

    def load_merge_candidate(self, filename=None, config=None):
        """
        Populates the candidate configuration. You can populate it from a file or from a string.
        If you send both a filename and a string containing the configuration, the file takes
        precedence.
        If you use this method the existing configuration will be merged with the candidate
        configuration once you commit the changes. This method will not change the configuration
        by itself.

        Args:

            filename (str): Path to the file containing the desired configuration. Defaults to None.
            config (str): String containing the desired configuration. Defaults to None.

        Raises:

            LoadConfigException: If there is an error on the configuration sent.
        """
        raise NotImplementedError

    def compare_config(self):
        """

        Returns:

            str: A string showing the difference between the running configuration and the
            candidate configuration. The running_config is loaded automatically just before doing
            the comparison so there is no need for you to do it.
        """
        raise NotImplementedError

    def commit_config(self):
        """
        Commits the changes requested by the method load_replace_candidate or load_merge_candidate.

        Raises:

            ???
        """
        raise NotImplementedError

    def discard_config(self):
        """
        Discards the configuration loaded into the candidate.

        Raises:

            ???
        """
        raise NotImplementedError

    def rollback(self):
        """
        If changes were made, revert changes to the original state.

        Raises:

            ???
        """
        raise NotImplementedError

    def cli(self, commands):
        """
        Will execute a list of commands and return the output in a dictionary format.

        Examples:

            >>> print(device.cli(['show version and haiku', 'show chassis fan'])
            {
                u'show version and haiku':  u'''Hostname: re0.edge01.arn01
                                                Model: mx480
                                                Junos: 13.3R6.5
                                                        Help me, Obi-Wan
                                                        I just saw Episode Two
                                                        You're my only hope''',
                u'show chassis fan'     :   u'''
                    Item               Status  RPM     Measurement
                    Top Rear Fan       OK      3840    Spinning at intermediate-speed
                    Bottom Rear Fan    OK      3840    Spinning at intermediate-speed
                    Top Middle Fan     OK      3900    Spinning at intermediate-speed
                    Bottom Middle Fan  OK      3840    Spinning at intermediate-speed
                    Top Front Fan      OK      3810    Spinning at intermediate-speed
                    Bottom Front Fan   OK      3840    Spinning at intermediate-speed'''
            }
        """
        raise NotImplementedError
