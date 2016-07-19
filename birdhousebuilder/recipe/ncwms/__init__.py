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
from zc.recipe.deployment import make_dir
import birdhousebuilder.recipe.conda
from birdhousebuilder.recipe import tomcat

config = Template(filename=os.path.join(os.path.dirname(__file__), "config.properties"))
wms_config = Template(filename=os.path.join(os.path.dirname(__file__), "config.xml"))

def make_dirs(name, user, mode=0o755):
    etc_uid, etc_gid = pwd.getpwnam(user)[2:4]
    created = []
    make_dir(name, etc_uid, etc_gid, mode, created)

class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs ncWMS2/tomcat with conda and setups the WMS configuration."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']

        self.options['name'] = self.options.get('name', self.name)
        self.name = self.options['name']

        self.logger = logging.getLogger(name)

        # deployment layout
        def add_section(section_name, options):
            if section_name in buildout._raw:
                raise KeyError("already in buildout", section_name)
            buildout._raw[section_name] = options
            buildout[section_name] # cause it to be added to the working parts

        self.deployment_name = self.name + "-ncwms-deployment"
        self.deployment = zc.recipe.deployment.Install(buildout, self.deployment_name, {
            'name': "ncwms",
            'prefix': self.options['prefix'],
            'user': self.options['user'],
            'etc-user': self.options['etc-user']})
        add_section(self.deployment_name, self.deployment.options)

        self.options['etc-prefix'] = self.options['etc_prefix'] = self.deployment.options['etc-prefix']
        self.options['var-prefix'] = self.options['var_prefix'] = self.deployment.options['var-prefix']
        self.prefix = self.options['prefix']

        # conda environment path
        self.options['env'] = self.options.get('env', '')
        self.options['pkgs'] = self.options.get('pkgs', 'ncwms2')
        self.options['channels'] = self.options.get('channels', 'defaults birdhouse')
        self.conda = birdhousebuilder.recipe.conda.Recipe(self.buildout, self.name, {
            'env': self.options['env'],
            'pkgs': self.options['pkgs'],
            'channels': self.options['channels'] })
        self.options['conda-prefix'] = self.options['conda_prefix'] = self.conda.options['prefix']

        # config options
        #self.options['config_dir'] = self.options.get(
        #    'config_dir', os.path.join(tomcat.content_root(self.prefix), 'ncWMS2'))
        self.options['data_dir'] = self.options.get(
            'data_dir', os.path.join(self.prefix, 'var', 'lib', 'pywps', 'outputs'))
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
        if not update:
            installed += list(self.deployment.install())
        installed += list(self.conda.install(update))
        installed += list(self.install_tomcat(update))
        #installed += list(self.install_config())
        #installed += list(self.install_wms_config())
        return installed

    def install_tomcat(self, update):
        script = tomcat.Recipe(
            self.buildout,
            self.name,
            self.options)
        return script.install(update)

    def install_config(self):
        result = config.render(**self.options)

        # make sure ncWMS2.war is unpacked
        #tomcat.unzip(self.env_path, 'ncWMS2.war')

        output = os.path.join(tomcat.tomcat_home(self.env_path), 'webapps', 'ncWMS2', 'WEB-INF', 'classes', 'config.properties')
        make_dirs(os.path.dirname(output))

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_wms_config(self):
        result = wms_config.render(**self.options)

        output = os.path.join(tomcat.content_root(self.prefix), 'ncWMS2', 'config.xml')
        make_dirs(os.path.dirname(output))

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def update(self):
        return self.install(update=True)

def uninstall(name, options):
    pass

