# ===============================================================================
#
# Copyright (c) 2010, 2011 by Thomas Hauth and Stephan Riedel
# 
# This file is part of ROCED.
# 
# ROCED is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ROCED is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with ROCED.  If not, see <http://www.gnu.org/licenses/>.
#
# ===============================================================================
from __future__ import unicode_literals, absolute_import

try:
    import boto
    # see http://docs.pythonboto.org/
    from euca2ools import Euca2ool
except ImportError:
    pass


class E2basedUtil(object):
    def __init__(self):
        self.imagesCache = None

    def loadImages(self, euca_conn):
        if self.imagesCache is None:
            self.imagesCache = euca_conn.get_all_images()

    def getImageByImageName(self, euca_conn, image_name):
        self.loadImages(euca_conn)

        for i in self.imagesCache:
            if i.location.startswith(image_name + "/"):
                return i

        raise LookupError("No image with name %s found." % image_name)

    def getImageIdByImageName(self, euca_conn, image_name):
        return self.getImageByImageName(euca_conn, image_name).id

    def getImageNameByImageId(self, euca_conn, id_):
        self.loadImages(euca_conn)

        for i in self.imagesCache:
            if i.id == id_:
                return i.location.partition("/")[0]

        raise LookupError("No image with id %s found." % id_)

    def openConnection(self):
        raise NotImplementedError("This method must be implemented by the concrete derived class")


class Ec2Util(E2basedUtil):
    def openConnection(self):
        e_conn = boto.connect_ec2(self.aws_access_key_id,
                                  self.aws_secret_access_key)
        return e_conn


class EucaUtil(E2basedUtil):
    def openConnection(self):
        euca = Euca2ool()
        euca_conn = euca.make_connection()
        return euca_conn
