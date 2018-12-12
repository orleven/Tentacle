#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

"""
Copyright (c) 2006-2017 Tentacle developers (http://Tentacle.org/)
See the file 'doc/COPYING' for copying permission
"""

class TentacleBaseException(Exception):
    pass

class TentacleCompressionException(TentacleBaseException):
    pass

class TentacleConnectionException(TentacleBaseException):
    pass

class TentacleDataException(TentacleBaseException):
    pass

class TentacleFilePathException(TentacleBaseException):
    pass

class TentacleGenericException(TentacleBaseException):
    pass

class TentacleInstallationException(TentacleBaseException):
    pass

class TentacleMissingDependence(TentacleBaseException):
    pass

class TentacleMissingMandatoryOptionException(TentacleBaseException):
    pass

class TentacleMissingPrivileges(TentacleBaseException):
    pass

class TentacleNoneDataException(TentacleBaseException):
    pass

class TentacleNotVulnerableException(TentacleBaseException):
    pass

class TentacleSilentQuitException(TentacleBaseException):
    pass

class TentacleUserQuitException(TentacleBaseException):
    pass

class TentacleShellQuitException(TentacleBaseException):
    pass

class TentacleSkipTargetException(TentacleBaseException):
    pass

class TentacleSyntaxException(TentacleBaseException):
    pass

class TentacleSystemException(TentacleBaseException):
    pass

class TentacleThreadException(TentacleBaseException):
    pass

class TentacleTokenException(TentacleBaseException):
    pass

class TentacleUndefinedMethod(TentacleBaseException):
    pass

class TentacleUnsupportedDBMSException(TentacleBaseException):
    pass

class TentacleUnsupportedFeatureException(TentacleBaseException):
    pass

class TentacleValueException(TentacleBaseException):
    pass
