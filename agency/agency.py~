##############################################################################
#
# Copyright (c) 2004 TINY SPRL. (http://tiny.be) All Rights Reserved.
#                    Fabien Pinckaers <fp@tiny.Be>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from osv import osv, fields
from datetime import datetime
import openerp.exceptions

class agency_city(osv.osv):
    _name = 'agency.city'
    _columns = {
        'code': fields.integer('Code',required=True),
        'name': fields.char('Name', size=64, required=True),
        'number_of_inhabitants': fields.integer('Number Of Inhabitants',required=True),
        'country': fields.many2one('res.country', 'Country'),
        'hotels': fields.one2many('agency.hotel', 'city_id', 'Hotels' ),
        'image': fields.binary('City image'),
    }
agency_city()

class agency_hotel(osv.osv):
    _name = 'agency.hotel'
    _columns = {
        'code': fields.integer('Code',required=True),
        'name': fields.char('Name', size=64, required=True),
        'number_of_rooms': fields.integer('Number Of Rooms', required=True),
        'address': fields.char('Address', size=64, required=True),
        'telephone_number': fields.char('Telephone Number', size=16, required=True),
        'city_id': fields.many2one('agency.city', 'City'),
        'hotel_id': fields.one2many('agency.scale','hotel_id','Scale'),
        'image_id': fields.one2many('agency.image','image_id','Image'),
	'price': fields.float('Price / Night',required=True),
        'image': fields.binary('Hotel image'),
    }
agency_hotel()

class agency_travel(osv.osv):
    _name = 'agency.travel'
    _columns = {
        'code': fields.integer('Code', required=True),
	'name': fields.char('Travel Name', size=64,required=True),
        'day_start': fields.date('Day Start',required=True),
        'day_end': fields.date('Day end',required=True),
        'scale_id': fields.one2many('agency.scale','travel_id','Scale'),
        'client_id': fields.many2one('res.partner','Client'),
    }
agency_travel()

class agency_scale(osv.osv):
    def totalDias(self, cr, uid, ids, field_name,arg, context=None):
    	res = {}
	DATETIME_FORMAT = "%Y-%m-%d"
	for record in self.browse(cr, uid, ids, context=context):
        	d1 = datetime.strptime(record.day_start, DATETIME_FORMAT)
    		d2 = datetime.strptime(record.day_end, DATETIME_FORMAT)
		resultado = (d2 - d1).days

		if resultado > 0:
			res[record.id] = resultado
		else:
			raise osv.except_osv(('Warning'), ('The day end can not be greater than the start day'))
	return res

    def totalPrecio(self, cr, uid, ids, field_name,arg, context=None):
    	todo = {}
	for record in self.browse(cr, uid, ids, context=context):
        	d3 = record.total_days
    		d4 = record.precio
		todo[record.id] = d3 * d4

	return todo

    _name = 'agency.scale'
    _columns = {
        'code': fields.integer('Code', required=True),
        'day_start': fields.date('Day Start',required=True),
        'day_end': fields.date('Day End',required=True),
        'total_days': fields.function(totalDias,type='integer',string='Total Days'),
        'hotel_id': fields.many2one('agency.hotel','hotel'),
	'precio': fields.related('hotel_id','price',relation='agency.hotel',type='float',string='Total price', store=False, readonly=True),
	'total_price': fields.function(totalPrecio,type='float', store=True ,string='Total Price'),
	'travel_id': fields.many2one('agency.travel','Travel'),
    }
agency_scale()

class agency_image(osv.osv):
    _name = 'agency.image'
    _columns = {
        'code': fields.integer('Code', required=True),
        'imatge': fields.binary('Imatge',required=True),
        'image_id': fields.many2one('agency.hotel','Hotel'),
    }
agency_image()

