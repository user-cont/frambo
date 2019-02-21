# Frambo, Framework for automation bots.
# Copyright (C) 2019  Red Hat, inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import jsl


class Notifications(jsl.Document):
    email_addresses = jsl.ArrayField(jsl.EmailField(), required=True)
    irc = jsl.ArrayField(jsl.StringField())


class Common(jsl.Document):
    enabled = jsl.BooleanField()
    notifications = jsl.DocumentField(Notifications, as_ref=True)


class DockerfileLinter(Common):
    """
    https://github.com/user-cont/zdravomil
    """
    pass


class BotCfg(jsl.Document):
    """
    bot-cfg.yml
    """
    version = jsl.StringField()
    global_ = jsl.DocumentField(Common, name="global")
    dockerfile_linter = jsl.DocumentField(DockerfileLinter, name="dockerfile-linter")


if __name__ == "__main__":
    from pprint import pprint
    pprint(BotCfg.get_schema())
