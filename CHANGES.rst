Changes
*******

0.4.1 (2016-08-19)
==================

* create .h2 dir with run-user permissions.
* update conda package ncwms2=2.2.2

0.4.0 (2016-08-15)
==================

* disable support for ncWMS <2.2.x.
* replaced ``data_dir`` options by ``dynamic_services`` option.
* added ``inMemorySizeMB`` and ``elementLifetimeMinutes``.

0.3.2 (2016-07-27)
==================

* added data2 dynamic service.

0.3.1 (2016-07-26)
==================

* prepared for ncWMS 2.2.x.
* config files are now in var/lib/tomcat/conf/ncWMS2.

0.3.0 (2016-07-25)
==================

* using zc.recipe.deployment.
* updated doctests.
* updated travis.

0.2.0 (2015-12-17)
==================

* added tomcat installation.
* using ncWMS2 2.0.4
* added empty datasets tag in config.xml template.

0.1.2 (2015-10-22)
==================

* added more options: title, abstract, ...
* renamed option data_root to data_dir
* updated to ncWMS2 2.0.3

0.1.1 (2015-10-20)
==================

* added Dataset config for PyWPS outputs.

0.1.0 (2015-10-19)
==================

* Initial Release.
