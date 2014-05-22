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

    def name_get (self, cr, uid, ids, context=None):
    	res = []
    	records = self.browse(cr,uid,ids)
    	for r in records:
     		res.append((r['id'], r.city_id.name + ", " + r.name))
    	return res

    _name = 'agency.hotel'
    _columns = {
        'code': fields.integer('Code',required=True),
        'name': fields.char('Name', size=64, required=True),
        'number_of_rooms': fields.integer('Number Of Rooms', required=True),
        'address': fields.char('Address', size=64, required=True),
        'telephone_number': fields.char('Telephone Number', size=16, required=True),
        'city_id': fields.many2one('agency.city', 'City'),
        'hotel_id': fields.one2many('sale.order.line','hotel_id','Scale'),
        'image_id': fields.one2many('agency.image','image_id','Image'),
	'price': fields.float('Price / Night',required=True),
        'image': fields.binary('Hotel image'),
	'room_id': fields.one2many('product.product','room_id','Room'),
    }
agency_hotel()

class agency_travel(osv.osv):
    _name = 'sale.order'
    _inherit = "sale.order"
    _columns = {
	'scalas': fields.one2many('sale.order.line','order_id',''),
    }
agency_travel()

class agency_scale(osv.osv):

    def onchange_city(self, cr, uid, ids, city_id, context=None):
    	return { 'domain' : {'hotel_id' : [('city_id','=',city_id)]}}
    
    def onchange_hotel(self, cr, uid, ids, hotel_id, context=None):
    	return { 'domain' : {'product_id' : [('room_id','=',hotel_id)]}}

    def onchange_end(self, cr, uid, ids, day_end, order_id, context=None):
	res = {}
	DATETIME_FORMAT = '%Y-%m-%d'
	
    	date = datetime.strptime(day_end, DATETIME_FORMAT)

	viajes = self.pool.get('sale.order');
		
	r = viajes.browse(cr,uid,order_id,context)

	for record in r.scalas:
		d1 = datetime.strptime(record.day_start, DATETIME_FORMAT)
    		d2 = datetime.strptime(record.day_end, DATETIME_FORMAT)

		if(date > d1):
			if(date < d2):
				return {'value' : {'day_end' : record.day_start},'warning' : {'title' : 'Error', 'message' : 'Incompatible date'}}
	
	return {'value' : {'day_end' : day_end}}

    def onchange_start(self, cr, uid, ids, day_start, order_id, context=None):
    	res = {}
	DATETIME_FORMAT = '%Y-%m-%d'
	
    	date = datetime.strptime(day_start, DATETIME_FORMAT)

	viajes = self.pool.get('sale.order');
		
	r = viajes.browse(cr,uid,order_id,context)

	for record in r.scalas:
		d1 = datetime.strptime(record.day_start, DATETIME_FORMAT)
    		d2 = datetime.strptime(record.day_end, DATETIME_FORMAT)

		if(date > d1):
			if(date < d2):
				return {'value' : {'day_start' : record.day_end},'warning' : {'title' : 'Error', 'message' : 'Incompatible date'}}
	
	return {'value' : {'day_start' : day_start}}

    def totalDias(self, cr, uid, ids, field_name,arg, context=None):
    	res = {}
	DATETIME_FORMAT = '%Y-%m-%d'
	
	for record in self.browse(cr, uid, ids, context=context):
		if record.isScale == True:
			d1 = datetime.strptime(record.day_start, DATETIME_FORMAT)
    			d2 = datetime.strptime(record.day_end, DATETIME_FORMAT)
			resultado = (d2 - d1).days
		
			if resultado > 0:
				res[record.id] = resultado
				d3 = resultado
	    			d4 = record.precio
				print d4
				#res[record.id] = d3 * d4
				self.write(cr, uid,record.id,{'product_uom_qty' : d3, 'price_unit' : d4})
			else:
				raise osv.except_osv(('Warning'), ('The day end can not be greater than the start day'))
	return res

    #def totalPrecio(self, cr, uid, ids, field_name,arg, context=None):
    	#todo = {}
	#for record in self.browse(cr, uid, ids, context=None):
		#if record.isScale == True:
			#d3 = record.total_days
	    		#d4 = record.precio
			#todo[record.id] = d3 * d4
			#self.write(cr, uid,record.id,{'product_uom_qty' : d3, 'price_uni' : d4})

	#return todo

    _name = 'sale.order.line'
    _inherit = "sale.order.line"
    _columns = {
        'day_start': fields.date('Day Start'),
        'day_end': fields.date('Day End'),
	#'scalas' : fields.many2one('sale.order' ,'Scales', ondelete='cascade'),
        'total_days': fields.function(totalDias,type='integer',string='Total Days',store=False),
        'hotel_id': fields.many2one('agency.hotel','Hotel'),
	'city_id': fields.many2one('agency.city','City'),
	'habi_id': fields.many2one('product.product','Room', ondelete='restrict'),
	'precio': fields.related('hotel_id','price',relation='agency.hotel',type='float',string='Total price', store=False, readonly=True),
	#'total_price': fields.function(totalPrecio,type='float', store=False ,string='Total Price'),
	'isScale':  fields.boolean('Is Scale', required=True),
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

class agency_room(osv.osv):
    _name = 'product.product'
    _inherit = "product.product"
    _columns = {
        'm2': fields.integer('Square meters', required=True),
	'rooms': fields.selection([('one','One'),('two','Two'),('marriage','Double bed'),('extrabed','Extra Bed Marriage')],'Rooms'),
	'imagebed': fields.binary('Bed Image'),
	'imagebathroom': fields.binary('Bathroom Image'),
	'ac' : fields.boolean('A / C', required=True),
	'isroom' : fields.boolean('Is Room', required=True),
	'room_id': fields.many2one('agency.hotel', 'Hotel',ondelete='cascade'),
    }
agency_room()


