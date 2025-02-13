from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count
from server.models import *
from django.shortcuts import get_object_or_404
import server.utils as utils

class MunkiVersion(IPlugin):
    def plugin_type(self):
        return 'builtin'

    def widget_width(self):
        return 4
        
    def widget_content(self, page, machines=None, theid=None):
        # The data is data is pulled from the database and passed to a template.
        
        # There are three possible views we're going to be rendering to - front, bu_dashbaord and group_dashboard. If page is set to bu_dashboard, or group_dashboard, you will be passed a business_unit or machine_group id to use (mainly for linking to the right search).
        if page == 'front':
            t = loader.get_template('munkiversion/templates/front.html')
        
        if page == 'bu_dashboard':
            t = loader.get_template('munkiversion/templates/id.html')
        
        if page == 'group_dashboard':
            t = loader.get_template('munkiversion/templates/id.html')
        
        try:
            munki_info = machines.values('munki_version').annotate(count=Count('munki_version')).order_by('munki_version')
        except:
            munki_info = []

        c = Context({
            'title': 'Munki Version',
            'data': munki_info,
            'theid': theid,
            'page': page
        })
        return t.render(c)
    
    def filter_machines(self, machines, data):
        # You will be passed a QuerySet of machines, you then need to perform some filtering based on the 'data' part of the url from the show_widget output. Just return your filtered list of machines and the page title.
        
        machines = machines.filter(munki_version__exact=data)
        
        title = 'Machines running version '+data+' of MSC'
        return machines, title
        