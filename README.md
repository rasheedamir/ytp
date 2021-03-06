
# Yhteentoimivuuspalvelut (YTP)

Main repository for Yhteentoimivuuspalvelut (_Interoperability services_ in Finnish). This service combines three related subservices: a metadata catalog of open data, a catalog of interoperability tools and guidelines, and a catalog of public services. The first phase of the service is the open data catalog Avoindata.fi. A public beta release of the service is available at [beta.avoindata.fi](http://beta.avoindata.fi) or [beta.opendata.fi](http://beta.opendata.fi).

This repository contains:

- Automated Deployment ([Ansible](http://www.ansible.com))
- Local Development Tools ([Vagrant](http://www.vagrantup.com))
- Continuous Integration ([Travis](https://travis-ci.org/yhteentoimivuuspalvelut/ytp)) [![Build Status][travis-image]][travis-url]
- Rest of the project code tied together as subtree modules under the _modules_ directory

## Getting started

To try out the service, visit [beta.avoindata.fi](http://beta.avoindata.fi) and register a user account to create new datasets.

To get started in developing the software, install a local development environment as described in the [documentation](doc/local-installation.md), and then see the [development documentation](doc/local-development.md).

## Documentation

Please refer to the [documentation directory](doc). [API documentation](https://github.com/yhteentoimivuuspalvelut/ytp-tools/tree/master/api_ckan) is currently under the ytp-tools project.

## Contact

Please file [issues at Github](https://github.com/yhteentoimivuuspalvelut/ytp/issues) or join the discussion at [avoindata.net](http://avoindata.net/questions/suomen-avoimen-datan-portaalin-rakentaminen).

## Copying and License

This material is copyright (c) 2014 Valtori Government ICT Centre, Finland.

It is open and licensed under the GNU Affero General Public License (AGPL) v3.0
whose full text may be found at: http://www.fsf.org/licensing/licenses/agpl-3.0.html

[travis-url]: https://travis-ci.org/yhteentoimivuuspalvelut/ytp
[travis-image]: https://travis-ci.org/yhteentoimivuuspalvelut/ytp.png?branch=master
