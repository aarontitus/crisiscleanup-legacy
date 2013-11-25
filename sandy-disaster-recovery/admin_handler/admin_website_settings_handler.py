#!/usr/bin/env python
#
# Copyright 2013 Chris Wood
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# System libraries.


# Local libraries.
import base

GLOBAL_ADMIN_NAME = "Admin"


class AdminWebsiteSettingsHandler(base.AuthenticatedHandler):

    def AuthenticatedGet(self, org, event):
        global_admin = False
        local_admin = False
	if org.name == GLOBAL_ADMIN_NAME:
            global_admin = True
        if global_admin == False and local_admin == False:
            self.redirect("/")
            return

        self.response.out.write("To be implemented.")