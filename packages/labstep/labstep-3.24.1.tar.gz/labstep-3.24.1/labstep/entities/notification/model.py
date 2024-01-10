#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Labstep <dev@labstep.com>

from labstep.generic.entity.model import Entity
from labstep.constants import UNSPECIFIED
from labstep.service.helpers import getTime

class Notification(Entity):
    __entityName__='notification'
    __unSearchable__=True