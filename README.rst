*****************************
birdhousebuilder.recipe.ncwms
*****************************

.. image:: https://travis-ci.org/bird-house/birdhousebuilder.recipe.ncwms.svg?branch=master
   :target: https://travis-ci.org/bird-house/birdhousebuilder.recipe.ncwms
   :alt: Travis Build

Introduction
************

``birdhousebuilder.recipe.ncwms`` is a `Buildout`_ recipe to install and configure `ncWMS`_ server with `Anaconda`_.
This recipe is used by the `Birdhouse`_ project. 

.. _`Buildout`: http://buildout.org/
.. _`Anaconda`: http://continuum.io/
.. _`Supervisor`: http://supervisord.org/
.. _`Birdhouse`: http://bird-house.github.io/
.. _`ncWMS`: https://www.gitbook.com/book/reading-escience-centre/ncwms-user-guide/details


Usage
*****

The recipe requires that Anaconda is already installed. You can use the buildout option ``anaconda-home`` to set the prefix for the anaconda installation. Otherwise the environment variable ``CONDA_PREFIX`` (variable is set when activating a conda environment) is used as conda prefix. 

The recipe will install the ``ncWMS2`` and ``apache-tomcat`` package from a conda channel in a conda enviroment defined by ``CONDA_PREFIX``. The intallation folder is given by the ``prefix`` buildout option. It deploys a `Supervisor`_ configuration for Tomcat in ``${prefix}/etc/supervisor/conf.d/tomcat.conf``. Supervisor can be started with ``${prefix}/etc/init.d/supervisord start``.

By default ``ncWMS2`` will be available on http://localhost:8080/ncWMS2.

The configuration files of ``ncWMS2`` are in ``${prefix}/var/lib/tomcat/conf/ncWMS2``.

The recipe depends on ``birdhousebuilder.recipe.conda``, ``birdhousebuilder.recipe.supervisor`` and ``birdhousebuilder.recipe.tomcat``.

Supported options
=================

This recipe supports the following options:

**anaconda-home**
  Buildout option pointing to the root folder of the Anaconda installation. Default: ``$HOME/anaconda``.

**dynamic_services**
  List of dynamic service configurations with name and root path to data files. Dynamic service configurations 
  are seperated by space or newlines. Service name and path is seperated by ``=``.
  Default: ``outputs=${prefix}/var/lib/pywps/outputs``

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

Cache options:

**enablecache**
  Enable WMS caching: Default: true

**inMemorySizeMB**
  Size in MB of in-memory cache. Default: 256

**elementLifetimeMinutes**
  Life-time of cache elements. Default: 0.0 (unlimited)

To configure tomcat see the options in the `tomcat recipe <https://pypi.python.org/pypi/birdhousebuilder.recipe.tomcat>`_. For example:

**http_port**
    HTTP Port for Tomcat service. Default: 8080

**ncwms_password**
    Enable ncWMS2 admin web interface by setting a password: Default: disabled


Example usage
=============

The following example ``buildout.cfg`` installs ncWMS2 with Anaconda and default options:

.. code-block:: ini 

  [buildout]
  parts = ncwms

  [ncwms]
  recipe = birdhousebuilder.recipe.ncwms
  organization = Birdhouse
  http_port = 8080

An example ``GetCapabilities`` URL to access a NetCDF file in outputs (using DATASET param)::

   http://localhost:8080/ncWMS2/wms?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0&DATASET=outputs/malleefowl/tasmax.nc



