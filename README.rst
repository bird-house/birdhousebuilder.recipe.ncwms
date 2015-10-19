*****************************
birdhousebuilder.recipe.ncwms
*****************************

.. image:: https://travis-ci.org/bird-house/birdhousebuilder.recipe.ncwms.svg?branch=master
   :target: https://travis-ci.org/bird-house/birdhousebuilder.recipe.ncwms
   :alt: Travis Build

.. contents::

Introduction
************

``birdhousebuilder.recipe.ncwms`` is a `Buildout`_ recipe to install and configure `ncWMS`_ server with `Anaconda`_.
This recipe is used by the `Birdhouse`_ project. 

.. _`Buildout`: http://buildout.org/
.. _`Anaconda`: http://www.continuum.io/
.. _`Supervisor`: http://supervisord.org/
.. _`Tomcat`: https://tomcat.apache.org/
.. _`Birdhouse`: http://bird-house.github.io/


Usage
*****

The recipe requires that Anaconda is already installed. It assumes that the default Anaconda location is in your home directory ``~/anaconda``. Otherwise you need to set the ``ANACONDA_HOME`` environment variable or the Buildout option ``anaconda-home``.

It installs the ``ncWMS2`` and ``apache-tomcat`` package from a conda channel  in a conda enviroment named ``birdhouse``. The location of the birdhouse environment is ``.conda/envs/birdhouse``. It deploys a `Supervisor`_ configuration for Tomcat in ``~/.conda/envs/birdhouse/etc/supervisor/conf.d/tomcat.conf``. Supervisor can be started with ``~/.conda/envs/birdhouse/etc/init.d/supervisord start``.

By default ``ncWMS2`` will be available on http://localhost:8080/ncWMS2.

The recipe depends on ``birdhousebuilder.recipe.conda``, ``birdhousebuilder.recipe.supervisor`` and ``birdhousebuilder.recipe.tomcat``.

Supported options
=================

This recipe supports the following options:

``anaconda-home``
   Buildout option with the root folder of the Anaconda installation. Default: ``$HOME/anaconda``.
   The default location can also be set with the environment variable ``ANACONDA_HOME``. Example::

     export ANACONDA_HOME=/opt/anaconda

   Search priority is:

   1. ``anaconda-home`` in ``buildout.cfg``
   2. ``$ANACONDA_HOME``
   3. ``$HOME/anaconda``

``data_root``
  Root Path of data files (NetCDF) for ncWMS2. Default: ``~/.conda/envs/birdhouse/var/lib/pywps/output``

``organization``
  The name of your organization. Default: Birdhouse

``url``
  The URL of your organization. Default: http://bird-house.github.io/

Example usage
=============

The following example ``buildout.cfg`` installs ncWMS2 with Anaconda and given ``data_root`` directory::

  [buildout]
  parts = ncwms

  anaconda-home = /home/myself/anaconda

  [ncwms]
  recipe = birdhousebuilder.recipe.ncwms
  organization = Birdhouse



