#!/usr/bin/env python
#
# Copyright 2012 Jeremy Pack
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
import os

import jinja2
import webapp2
from webapp2_extras import routes


# Local libraries.
import authentication_handler
import base
import delete_handler
import edit_handler
import export_handler
import export_bulk_handler
import form_handler
import import_handler
import key
import map_handler
import print_handler 
import problem_handler
import refresh_handler
import blobstore_delete_handler
import scripts_handler
import site_ajax_handler
import site_api_handler
import sites_handler
import new_organization_handler
import welcome_handler
import organization_ajax_handler
import export_all_handler
from admin_handler import admin_handler
import organization_info_handler
import contact_info_handler
import organization_settings_handler
import export_contacts_handler
import organization_add_contacts_handler
import organization_edit_contacts_handler
import organization_edit_info_handler
import see_all_contacts_handler
import js_logs_handler
import page_handler
import about_handler
import terms_handler
import privacy_handler
import contact_us_handler
import public_map_handler
import public_map_ajax_handler
import get_event_ajax_handler
import import_co_handler
import change_password_handler
import messaging

from handlers import incident_definition
from handlers import incident_form_creator
from handlers import incident_definition_ajax
from handlers import incident_create_first_phase
from handlers import incident_save_form
from handlers import incident_list
from handlers import incident_edit_phase
from handlers import incident_edit
from handlers import incident_create_definition_version
from handlers import incident_add_phase
from handlers import incident_edit_phases
from handlers import incident_edit_map_definition
from handlers import incident_edit_communications_definition
from handlers import incident_definition_legacy
from handlers import check_similar_by_phase_api
from handlers import incident_definition_home


from admin_handler import admin_create_organization_handler
from admin_handler import admin_new_organization_handler
from admin_handler import admin_organization_requests_handler
from admin_handler import admin_all_organizations_handler
from admin_handler import admin_inactive_organizations_handler
from admin_handler import admin_create_admin_handler
from admin_handler import admin_create_contact_handler
from admin_handler import admin_display_contacts_handler
from admin_handler import admin_single_contact_handler
from admin_handler import admin_create_incident_handler
from admin_handler import admin_see_admins_handler
from admin_handler import admin_incident_add_admin_handler
from admin_handler import admin_make_admin_handler
from admin_handler import admin_import_csv_handler
from admin_handler import admin_edit_pages_handler


from admin_handler import admin_single_organization_handler as admin_single_organization_handler
from admin_handler import admin_edit_organization_handler as admin_edit_organization_handler
from admin_handler import admin_edit_contact_handler as admin_edit_contact_handler
from admin_handler import admin_import_contacts_handler as admin_import_contacts_handler

from admin_handler import admin_create_incident_form_handler

from api import private_map_handler
from api import get_incident_definition
from api import private_site_handler

import form_ajax_handler
import update_csv_handler
from admin_handler import admin_create_incident_csv_handler
from admin_handler import admin_stats_handler


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

MAP_URL = "http://maps.google.com/?q=http://www.aarontitus.net/maps/sandy_work_orders.kmz"
SPREADSHEET_URL = "https://docs.google.com/spreadsheet/ccc?key=0AhBdPrWyrhIfdFVHMDFOc0NCQjNNbmVvNHJybTlBUXc#gid=0"

class LogoutHandler(base.RequestHandler):
  def get(self):
    self.response.headers.add_header("Set-Cookie",
                                     key.GetDeleteCookie())
    self.redirect("/authentication")

class Route(routes.RedirectRoute):
  def __init__(self, *args, **kwargs):
    # This causes a URL to redirect to its canonical version without a slash.
    # See http://webapp-improved.appspot.com/api/webapp2_extras/routes.html#webapp2_extras.routes.RedirectRoute
    if 'strict_slash' not in kwargs:
      kwargs['strict_slash'] = True
    routes.RedirectRoute.__init__(self, *args, **kwargs)

app = webapp2.WSGIApplication([
    Route(r'/contact', contact_us_handler.ContactUsHandler, 'dev'),
    Route(r'/update_csv_handler', update_csv_handler.UpdateCSVHandler, 'dev'),

    Route(r'/public-map', public_map_handler.PublicMapHandler, 'dev'),
    Route(r'/public_map_ajax_handler', public_map_ajax_handler.PublicMapAjaxHandler, 'dev'),

    Route(r'/home', page_handler.PageHandler, 'dev'),
    Route(r'/about', about_handler.AboutHandler, 'about'),
    Route(r'/terms', terms_handler.TermsHandler, 'terms'),
    Route(r'/privacy', privacy_handler.PrivacyHandler, 'privacy'),
    Route(r'/donate', redirect_to='http://www.crowdrise.com/CrisisCleanup', name='donate'),
    Route(r'/refresh_counties', refresh_handler.RefreshHandler, name='refresh_counties'),
    Route(r'/old', redirect_to=SPREADSHEET_URL, name='spreadsheet_redirect'),
    Route(r'/api/site', site_api_handler.SiteApiHandler, 'site_api'),
    Route(r'/api/site_ajax', site_ajax_handler.SiteAjaxHandler, 'site_ajax'),
    Route(r'/authentication', authentication_handler.AuthenticationHandler,
          'auth'),
    Route(r'/export', export_handler.ExportHandler, 'export'),
    Route(r'/export_all', export_all_handler.ExportAllHandler, 'export_all'),
    Route(r'/export_bulk', export_bulk_handler.ExportBulkHandler, 'export_bulk'),
    Route(r'/export_bulk_worker', export_bulk_handler.ExportBulkWorker, 'export_bulk_worker'),
    Route(r'/export_bulk_download', export_bulk_handler.DownloadBulkExportHandler, 'export_bulk_download'),
    Route(r'/get_event_ajax', get_event_ajax_handler.GetEventAjaxHandler, 'get_event_ajax'),
    Route(r'/change_password', change_password_handler.ChangePasswordHandler, 'change_password'),

    Route(r'/logout', LogoutHandler, 'logout'),
    Route(r'/delete', delete_handler.DeleteHandler, 'delete'),
    Route(r'/dev', form_handler.FormHandler, 'dev'),
    Route(r'/', form_handler.FormHandler, 'dev'),
    Route(r'/dev/map', map_handler.MapHandler, 'map'),
    Route(r'/phase/', form_handler.FormHandler, 'dev'),

    Route(r'/dev/maps', redirect_to_name='map', name='maps_redirect'),
    Route(r'/map', map_handler.MapHandler, 'map'),
    Route(r'/maps', redirect_to_name='map', name='maps_redirect'),
    Route(r'/edit', edit_handler.EditHandler, 'edit'),
    Route(r'/import', import_handler.ImportHandler, 'import'),
    Route(r'/old/map', redirect_to=MAP_URL, name='external_map_redirect'),
    Route(r'/old/maps', redirect_to_name=MAP_URL, name='external_maps_redirect'),
    Route(r'/print', print_handler.PrintHandler, 'print'),
    Route(r'/problems', problem_handler.ProblemHandler, 'problems'),
    Route(r'/sites', sites_handler.SitesHandler, 'sites'),
    Route(r'/signup', new_organization_handler.NewOrganizationHandler, 'new_organization'),
    Route(r'/admin-create-incident', admin_create_incident_handler.AdminCreateIncidentHandler, 'admin-create-incident'),
    Route(r'/admin', admin_handler.AdminHandler, 'admin_handler'),
    Route(r'/admin-create-organization', admin_create_organization_handler.AdminHandler, 'admin_create_organization_handler'),
    Route(r'/admin-new-organization', admin_new_organization_handler.AdminHandler, 'admin_new_organization_handler'),
    Route(r'/admin-organization-requests', admin_organization_requests_handler.AdminHandler, 'admin_organization_requests_handler'),
    Route(r'/admin-all-organizations', admin_all_organizations_handler.AdminHandler, 'admin_all_organizations_handler'),
    Route(r'/admin-all-organizations', admin_all_organizations_handler.AdminHandler, 'admin_all_organizations_handler'),
    Route(r'/admin-inactive-organizations', admin_inactive_organizations_handler.AdminHandler, 'admin_all_organizations_handler'),
    Route(r'/admin-create-admin', admin_create_admin_handler.AdminHandler, 'admin_create_admin_handler'),
    Route(r'/admin-create-contact', admin_create_contact_handler.AdminHandler, 'admin_create_contact_handler'),
    Route(r'/admin-display-contacts', admin_display_contacts_handler.AdminHandler, 'admin_display_contacts_handler'),
    Route(r'/admin-single-contact', admin_single_contact_handler.AdminHandler, 'admin_single_contact_handler'),
    Route(r'/admin-single-organization', admin_single_organization_handler.AdminHandler, 'admin_single_organization_handler'),
    Route(r'/admin-edit-organization', admin_edit_organization_handler.AdminHandler, 'admin_edit_organization_handler'),
    Route(r'/admin-edit-contact', admin_edit_contact_handler.AdminHandler, 'admin_edit_contact_handler'),
    Route(r'/admin-see-admins', admin_see_admins_handler.AdminHandler, 'admin_see_admins_handler'),
    Route(r'/admin-incident-add-admin', admin_incident_add_admin_handler.AdminHandler, 'admin_incident_add_admin_handler'),
    Route(r'/admin-make-admin', admin_make_admin_handler.AdminHandler, 'admin_make_admin_handler'),
    Route(r'/admin-import-contacts', admin_import_contacts_handler.ImportContactsHandler, 'admin_import_contacts_handler'),
    Route(r'/admin-import-csv', admin_import_csv_handler.ImportCSVHandler, 'admin_import_csv_handler'),
    Route(r'/admin-import-csv/template.csv', admin_import_csv_handler.DownloadCSVTemplateHandler, 'admin_import_csv_handler'),
    Route(r'/admin-import-csv/active', admin_import_csv_handler.ActiveCSVImportHandler, 'admin_import_csv_handler'),
    Route(r'/admin-import-csv/active/invalids.csv', admin_import_csv_handler.ActiveCSVImportHandler, 'admin_import_csv_handler'),
    Route(r'/admin-edit-pages', admin_edit_pages_handler.AdminEditPagesHandler, 'admin_edit_pages_handler'),
    Route(r'/admin-edit-pages/download/defaults', admin_edit_pages_handler.AdminDownloadPageBlocks, 'admin_edit_pages_handler'),
    Route(r'/admin-create-incident-csv', admin_create_incident_csv_handler.AdminCreateIncidentCSVHandler, 'admin_edit_pages_handler'),

    Route(r'/admin-stats', admin_stats_handler.AdminStatsHandler, 'admin_stats_handler'),
    Route(r'/import-co-flood-handler', import_co_handler.ImportCOHandler, 'import-co-flood'),

    Route(r'/organization-info', organization_info_handler.OrganizationInfoHandler, 'organization_info_handler'),
    Route(r'/contact-info', contact_info_handler.ContactInfoHandler, 'contact_info_handler'),
    Route(r'/organization-settings', organization_settings_handler.OrganizationSettingsHandler, 'organization_settings_handler'),
    Route(r'/export_contacts_handler', export_contacts_handler.ExportContactsHandler, 'export_contacts_handler'),
    Route(r'/organization-add-contact', organization_add_contacts_handler.OrganizationAddContactsHandler, 'organization_add_contacts_handler'),   
    Route(r'/organization-edit-contact', organization_edit_contacts_handler.OrganizationEditContactsHandler, 'organization_edit_contacts_handler'),   
    Route(r'/welcome', welcome_handler.WelcomeHandler, 'welcome_handler'),
    Route(r'/organization_ajax_handler', organization_ajax_handler.OrganizationAjaxHandler, 'organization_ajax_handler'),
    Route(r'/organization-edit-info', organization_edit_info_handler.OrganizationEditInfoHandler, 'new_organization'),
    Route(r'/see-all-contacts', see_all_contacts_handler.SeeAllContactsHandler, 'see_all_contacts_handler'),
    Route(r'/js-logs', js_logs_handler.JsLogsHandler, 'js_logs_handler'),
    Route(r'/blobstore-delete', blobstore_delete_handler.BlobstoreDeleteHandler, 'blobstore_delete_handler'),

    Route(r'/script/run', scripts_handler.ScriptsHandler, 'scripts_handler'),
    Route(r'/form_ajax_handler', form_ajax_handler.FormAjaxHandler, 'form_ajax_handler'),

    Route(r'/incident_definition', incident_definition.IncidentDefinition, 'incident_definition'),
    Route(r'/incident_definition_home', incident_definition_home.IncidentDefinitionHome, 'incident_definition_home'),
    Route(r'/incident_definition_legacy', incident_definition_legacy.IncidentDefinitionLegacy, 'incident_definition_legacy'),
    Route(r'/incident_definition_ajax', incident_definition_ajax.IncidentDefinitionAjax, 'incident_definition_ajax'),
    Route(r'/incident_create_first_phase', incident_create_first_phase.IncidentCreateFirstPhase, 'incident_create_first_phase'),
    Route(r'/incident_save_form', incident_save_form.IncidentSaveForm, 'incident_save_form'),
    Route(r'/incident_form_creator', incident_form_creator.IncidentFormCreator, 'incident_form_creator'),
    Route(r'/incident_list', incident_list.IncidentList, 'incident_list'),
    Route(r'/incident_edit_phase', incident_edit_phase.IncidentEditPhase, 'incident_edit_phase'),
    Route(r'/incident_add_phase', incident_add_phase.IncidentAddPhase, 'incident_add_phase'),
    Route(r'/incident_edit', incident_edit.IncidentEdit, 'incident_edit'),
    Route(r'/incident_edit_phases', incident_edit_phases.IncidentEditPhases, 'incident_edit_phases'),
    Route(r'/incident_edit_map_definition', incident_edit_map_definition.IncidentEditMapDefinition, 'incident_edit_map_definition'),
    Route(r'/incident_edit_communications_definition', incident_edit_communications_definition.IncidentEditCommunicationsDefinition, 'incident_edit_communications_definition'),
    
    Route(r'/check_similar_by_phase_api', check_similar_by_phase_api.CheckSimilarByPhaseAPI, "check_similar_by_phase_api"),
    Route(r'/api/private_map_handler', private_map_handler.PrivateMapHandler, "private_map_handler"),
    Route(r'/api/get_incident_definition', get_incident_definition.GetIncidentDefinition, "get_incident_definition"),
    Route(r'/api/private_site_handler', private_site_handler.PrivateSiteHandler, "private_site_handler"),

    Route(r'/incident_create_definition_version', incident_create_definition_version.IncidentCreateDefinitionVersion, 'incident_create_definition_version'),


    Route(r'/admin-create-incident-form', admin_create_incident_form_handler.AdminCreateIncidentFormHandler, 'admin_create_incident_form_handler'),

    ## DISABLED ## Route(r'/test-email', messaging.EmailTestHandler, 'email_test_handler'),
    
], debug=True)
