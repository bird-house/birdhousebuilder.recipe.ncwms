# -*- coding: utf-8 -*-

"""
Recipe ncwms

http://reading-escience-centre.github.io/edal-java/ncWMS_user_guide.html
"""

import os
import pwd
import logging
from mako.template import Template

import zc.buildout
import zc.recipe.deployment
from zc.recipe.deployment import Configuration
import birdhousebuilder.recipe.conda
import birdhousebuilder.recipe.tomcat
from birdhousebuilder.recipe.tomcat import make_dirs, unzip

config_props = Template(filename=os.path.join(os.path.dirname(__file__), "config.properties"))
wms_config = Template(filename=os.path.join(os.path.dirname(__file__), "config.xml"))

class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs ncWMS2/tomcat with conda and setups the WMS configuration."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']

        self.options['name'] = self.options.get('name', self.name)
        self.name = self.options['name']

        self.logger = logging.getLogger(name)

        # tomcat
        self.options['pkgs'] = self.options.get('pkgs', 'apache-tomcat ncwms2')
        self.tomcat = birdhousebuilder.recipe.tomcat.Recipe(self.buildout, self.name, self.options)
            
        # ncwms config options
        #self.options['config_dir'] = self.options.get(
        #    'config_dir', os.path.join(tomcat.content_root(self.prefix), 'ncWMS2'))
        self.options['data_dir'] = self.options.get(
            'data_dir', os.path.join(self.tomcat.prefix, 'var', 'lib', 'pywps', 'outputs'))
        self.options['contact'] = self.options.get('contact', 'Birdhouse Admin')
        self.options['email'] = self.options.get('email', '')
        self.options['organization'] = self.options.get('organization', 'Birdhouse')
        self.options['title'] = self.options.get('title', 'Birdhouse ncWMS2 Server')
        self.options['abstract'] = self.options.get('abstract', 'ncWMS2 Web Map Service used in Birdhouse')
        self.options['keywords'] = self.options.get('keywords', 'birdhouse,ncwms,wms')
        self.options['url'] = self.options.get('url', 'http://bird-house.github.io/')
        self.options['allowglobalcapabilities'] = self.options.get('allowglobalcapabilities', 'true')
        self.options['enablecache'] = self.options.get('enablecache', 'false')
        self.options['updateInterval'] = self.options.get('updateInterval', '1')

    def install(self, update=False):
        installed = []
        installed += list(self.tomcat.install(update))
        installed += list(self.install_config())
        installed += list(self.install_wms_config())
        return installed

    def install_config(self):
        text = config_props.render(**self.options)

        # make sure ncWMS2.war is unpacked
        unzip(
            os.path.join(self.tomcat.options['catalina-base']),
            os.path.join(self.tomcat.options['catalina-home'], 'webapps', 'ncWMS2.war'))

        config = Configuration(self.buildout, 'config.properties', {
            'deployment': self.tomcat.deployment_name,
            'directory': os.path.join(self.options['catalina-base'], 'webapps', 'ncWMS2', 'WEB-INF', 'classes' ),
            'text': text})
        return [config.install()]

    def install_wms_config(self):
        text = wms_config.render(**self.options)
        #output = os.path.join(tomcat.content_root(self.prefix), 'ncWMS2', 'config.xml')
        make_dirs(os.path.join(self.options['catalina-base'], 'conf', 'ncWMS2' ), self.options['etc-user'], mode=0o755)
        config = Configuration(self.buildout, 'config.xml', {
            'deployment': self.tomcat.deployment_name,
            'directory': os.path.join(self.options['catalina-base'], 'conf', 'ncWMS2' ),
            'text': text})
        return [config.install()]

    def update(self):
        return self.install(update=True)

def uninstall(name, options):
    pass

