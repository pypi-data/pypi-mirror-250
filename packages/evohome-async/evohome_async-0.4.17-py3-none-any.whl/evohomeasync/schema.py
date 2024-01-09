#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""evohomeasync provides an async client for the *original* Evohome API."""

from typing import Any, TypeAlias

# TCC config, status dicts
_EvoLeafT: TypeAlias = bool | float | int | str | list[str]  # Any
_DeviceDictT: TypeAlias = dict[str, Any]  # '_EvoDeviceT' | _EvoLeafT]
_EvoDictT: TypeAlias = dict[str, Any]  # '_EvoDictT' | _EvoLeafT]
_EvoListT: TypeAlias = list[_EvoDictT]
_EvoSchemaT: TypeAlias = _EvoDictT | _EvoListT

# TCC identifiers (Usr, Loc, Gwy, Sys, Zon|Dhw)
_DhwIdT: TypeAlias = int
_GatewayIdT: TypeAlias = int
_LocationIdT: TypeAlias = int
_SystemIdT: TypeAlias = int
_UserIdT: TypeAlias = int
_ZoneIdT: TypeAlias = int
_ZoneNameT: TypeAlias = str

# TCC other
_ModeT: TypeAlias = str
_SystemModeT: TypeAlias = str

_TaskIdT: TypeAlias = str  # TODO: int or str?


SZ_SESSION_ID = "sessionId"  # id Id, not ID

# schema keys (start with a lower case letter)
SZ_ALLOWED_MODES = "allowedModes"
SZ_CHANGEABLE_VALUES = "changeableValues"
SZ_COOL_SETPOINT = "coolSetpoint"
SZ_DEVICE_ID = "deviceID"  # is ID, not Id
SZ_DEVICES = "devices"
SZ_DOMAIN_ID = "domainID"  # is ID, not Id
SZ_GATEWAY_ID = "gatewayId"  # is Id, not ID
SZ_HEAT_SETPOINT = "heatSetpoint"
SZ_ID = "id"  # is id, not Id/ID
SZ_INDOOR_TEMPERATURE = "indoorTemperature"
SZ_LOCATION_ID = "locationID"  # is ID, not Id
SZ_MAC_ID = "macID"  # is ID, not Id
SZ_MODE = "mode"
SZ_NAME = "name"
SZ_NEXT_TIME = "NextTime"
SZ_QUICK_ACTION = "QuickAction"
SZ_QUICK_ACTION_NEXT_TIME = "QuickActionNextTime"
SZ_SETPOINT = "setpoint"
SZ_SPECIAL_MODES = "SpecialModes"
SZ_STATE = "state"
SZ_STATUS = "status"
SZ_TEMP = "temp"
SZ_THERMOSTAT = "thermostat"
SZ_THERMOSTAT_MODEL_TYPE = "thermostatModelType"
SZ_USER_ID = "userID"  # is ID, not Id
SZ_USER_INFO = "userInfo"
SZ_VALUE = "value"

# schema values (start with an upper case letter)
SZ_AUTO = "Auto"
SZ_AUTO_WITH_ECO = "AutoWithEco"
SZ_AWAY = "Away"
SZ_CUSTOM = "Custom"
SZ_DAY_OFF = "DayOff"
SZ_HEATING_OFF = "HeatingOff"
#
SZ_DHW_OFF = "DHWOff"
SZ_DHW_ON = "DHWOn"
#
SZ_DOMESTIC_HOT_WATER = "DOMESTIC_HOT_WATER"
SZ_EMEA_ZONE = "EMEA_ZONE"
#
SZ_HOLD = "Hold"
SZ_SCHEDULED = "Scheduled"
SZ_TEMPORARY = "Temporary"
#
SZ_HEAT = "Heat"
SZ_OFF = "Off"
