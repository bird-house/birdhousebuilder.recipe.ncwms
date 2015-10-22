*****************************
birdhousebuilder.recipe.ncwms
*****************************

.. image:: https://travis-ci.org/bird-house/birdhousebuilder.recipe.ncwms.svg?branch=master
   :target: https://travis-ci.org/bird-house/birdhousebuilder.recipe.ncwms
   :alt: Travis Build

.. contents::

Introduction
************

``birdhousebuilder.recipe.ncwms`` is a `Buildout <http://buildout.org/>`_ recipe to install and configure `ncWMS <http://reading-escience-centre.github.io/edal-java/ncWMS_user_guide.html>`_ server with `Anaconda <http://www.continuum.io/>`_.
This recipe is used by the `Birdhouse <http://bird-house.github.io/>`_ project. 


Usage
*****

The recipe requires that Anaconda is already installed. It assumes that the default Anaconda location is in your home directory ``~/anaconda``. Otherwise you need to set the ``ANACONDA_HOME`` environment variable or the Buildout option ``anaconda-home``.

It installs the ``ncWMS2`` and ``apache-tomcat`` package from a conda channel  in a conda enviroment named ``birdhouse``. The location of the birdhouse environment is ``.conda/envs/birdhouse``. It deploys a `Supervisor <http://supervisord.org/>`_ configuration for Tomcat in ``~/.conda/envs/birdhouse/etc/supervisor/conf.d/tomcat.conf``. Supervisor can be started with ``~/.conda/envs/birdhouse/etc/init.d/supervisord start``.

By default ``ncWMS2`` will be available on http://localhost:8080/ncWMS2.

The recipe depends on ``birdhousebuilder.recipe.conda``, ``birdhousebuilder.recipe.supervisor`` and ``birdhousebuilder.recipe.tomcat``.

Supported options
=================

This recipe supports the following options:

**anaconda-home**
   Buildout option with the root folder of the Anaconda installation. Default: ``$HOME/anaconda``.
   The default location can also be set with the environment variable ``ANACONDA_HOME``. Example::

     export ANACONDA_HOME=/opt/anaconda

   Search priority is:

   1. ``anaconda-home`` in ``buildout.cfg``
   2. ``$ANACONDA_HOME``
   3. ``$HOME/anaconda``

**data_dir**
  Root Path of data files (NetCDF) for ncWMS2 (sed in dynamic service ``outputs``). 
  Default: ``~/.conda/envs/birdhouse/var/lib/pywps/outputs``

**title**
  Title for this Web Map Service. Default: Birdhouse ncWMS2 Server

**abstract**
  More details about this Web Map Service. Default: ncWMS2 Web Map Service used in Birdhouse  

**contact**
  Name of server administrator. Default: Birdhouse Admin

**organization**
  Organization of server administrator. Default: Birdhouse

**url**
  Web site of the service provider. Default: http://bird-house.github.io/

**enablecache**
  Enable WMS caching: Default: false

Example usage
=============

The following example ``buildout.cfg`` installs ncWMS2 with Anaconda and default options:

.. code-block:: ini 

  [buildout]
  parts = ncwms

  anaconda-home = /home/myself/anaconda

  [ncwms]
  recipe = birdhousebuilder.recipe.ncwms
  organization = Birdhouse

An example ``GetCapabilities`` URL to access for an output NetCDF file in outputs (using DATASET param)::

   http://localhost:8080/ncWMS2/wms?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0&DATASET=outputs/malleefowl/tasmax.nc



