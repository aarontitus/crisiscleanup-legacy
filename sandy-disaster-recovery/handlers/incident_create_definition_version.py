#!/usr/bin/env python
#
# Copyright 2013 Andy Gimma
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
import jinja2
import os
import webapp2_extras
from datetime import datetime
from google.appengine.ext import db

# Local libraries.
import base
import key
from models import incident_definition
import event_db
import cache

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname( __file__ ), '..', 'templates')))
template = jinja_environment.get_template('/incident_create_definition_version.html')

read_template = jinja_environment.get_template('/incident_definition_read.html')

CASE_LABELS = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

def make_date_object(date_string):
  pass

class IncidentCreateDefinitionVersion(base.AuthenticatedHandler):
  def AuthenticatedGet(self, org, event):
    id = self.request.get("id")
    if id:
      incident_definition_object = incident_definition.IncidentDefinition.get_by_id(int(id))
      data = {
	"incident_definition_object": incident_definition_object,
      }
      self.response.out.write(read_template.render(data))
    else:
      q = incident_definition.IncidentDefinition.all()
      q.filter("is_version =", True)
      versions = q.count()
      form = incident_definition.IncidentDefinitionForm()
      work_order_prefix = "Set from event_db"
      query_string = "SELECT * FROM Event"
      events_list = db.GqlQuery(query_string)
      count = events_list.count()
      current_date = None
      data = {
	"work_order_prefix": CASE_LABELS[count],
	"current_date": current_date,
	"form": form,
	"version": versions + 1
      }
      self.response.out.write(template.render(data))

  def AuthenticatedPost(self, org, event):
    data = incident_definition.IncidentDefinitionForm(self.request.POST)
    timezone = data.timezone.data
    if not data.validate():
      self.response.out.write(template.render(
	{
	  "form": data,
	  "errors": data.errors,
      }))
    else:
      #incident_version = self.request.get("incident_version")
      incident_full_name = data.full_name.data
      incident_short_name = data.short_name.data
      
      incident_date = data.incident_date.data
      start_date = data.start_date.data
      end_date = data.end_date.data
      work_order_prefix = data.work_order_prefix.data
      centroid_latitude = data.centroid_lat.data
      centroid_longitude = data.centroid_lng.data
      camera_latitude = data.camera_lat.data
      camera_longitude = data.camera_lng.data
      developer_mode = data.developer_mode.data
      ignore_validation = data.ignore_validation.data
      
      local_admin_name = data.local_admin_name.data
      local_admin_title = data.local_admin_title.data
      local_admin_organization = data.local_admin_organization.data
      local_admin_email = data.local_admin_email.data
      local_admin_cell_phone = data.local_admin_cell_phone.data
      local_admin_password = data.local_admin_password.data
    
    
      public_map_title = data.public_map_title.data
      public_map_url = data.public_map_url.data
      public_map_cluster = data.public_map_cluster.data
      public_map_zoom = data.public_map_zoom.data
      
      internal_map_title = data.internal_map_title.data
      internal_map_url = data.internal_map_url.data
      internal_map_cluster = data.internal_map_cluster.data
      internal_map_zoom = data.internal_map_zoom.data
    
      start_date_object = datetime.strptime(start_date, "%m/%d/%Y").date()
      end_date_object = datetime.strptime(end_date, "%m/%d/%Y").date()
      incident_date_object = datetime.strptime(incident_date, "%m/%d/%Y").date()
      
      # create new version and associate with inc def
      #if incident_version == "New":
	#inc_def = incident_definition.IncidentDefinition(is_schema_version = True, version = incident_version, full_name = incident_full_name, short_name = incident_short_name, timezone = timezone, start_date = start_date_object, end_date = end_date_object, incident_date = incident_date_object, work_order_prefix = work_order_prefix, centroid_lat = centroid_latitude, centroid_lng = centroid_longitude, camera_latitude = camera_latitude, camera_longitude = camera_longitude, developer_mode = developer_mode, ignore_validation = ignore_validation, local_admin_name = local_admin_name, local_admin_title = local_admin_title, local_admin_organization = local_admin_organization, local_admin_email = local_admin_email, local_admin_cell_phone = local_admin_cell_phone, local_admin_password = local_admin_password, public_map_cluster = public_map_cluster, public_map_title = public_map_title, public_map_url = public_map_url, public_map_zoom = public_map_zoom, internal_map_cluster = internal_map_cluster, internal_map_title = internal_map_title, internal_map_url = internal_map_url, internal_map_zoom = internal_map_zoom)
	


      ### TODO
      # Make this happen atomically
	  
      query_string = "SELECT * FROM Event"
      events_list = db.GqlQuery(query_string)
      count = events_list.count()
      this_event = event_db.Event(name = incident_full_name,
			  short_name = incident_short_name,
			  case_label = data.work_order_prefix.data,
			)
      ten_minutes = 600
      cache.PutAndCache(this_event, ten_minutes)
      
      # add this version = incident_version
      inc_def = incident_definition.IncidentDefinition(is_version = True, full_name = incident_full_name, short_name = incident_short_name, timezone = timezone, start_date = start_date_object, end_date = end_date_object, incident_date = incident_date_object, work_order_prefix = work_order_prefix, centroid_lat = centroid_latitude, centroid_lng = centroid_longitude, camera_latitude = camera_latitude, camera_longitude = camera_longitude, developer_mode = developer_mode, ignore_validation = ignore_validation, local_admin_name = local_admin_name, local_admin_title = local_admin_title, local_admin_organization = local_admin_organization, local_admin_email = local_admin_email, local_admin_cell_phone = local_admin_cell_phone, local_admin_password = local_admin_password, public_map_cluster = public_map_cluster, public_map_title = public_map_title, public_map_url = public_map_url, public_map_zoom = public_map_zoom, internal_map_cluster = internal_map_cluster, internal_map_title = internal_map_title, internal_map_url = internal_map_url, internal_map_zoom = internal_map_zoom, incident = this_event.key())
      inc_def.put()

      
      self.redirect("/incident_definition?id=" + str(inc_def.key().id()))

      
  
    # make dates date objects
    # use make_date_object
    
    
    
    #hash a password
    #webapp2_extras.security.hash_password(password, method, salt=None, pepper=None)
    #get password hash
    #webapp2_extras.security.check_password_hash(password, pwhash, pepper=None)
    