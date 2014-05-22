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

class cooperative_member(osv.osv):
    """(NULL)"""
    _name = 'cooperative.member'
    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'dni': fields.char('DNI', size=9, required=True),
        'code': fields.integer('Code',required=True),
        'number_actions': fields.integer('Number of actions',required=True),
        'fruits': fields.one2many('cooperativa.fruits','fruit_person','Fruits'),
    }
cooperative_member()

class cooperativa_fruits(osv.osv):
    def totalPesetas(self, cr, uid, ids, field_name,arg, context=None):
    	todo = {}
	for record in self.browse(cr, uid, ids, context=context):
        	d3 = record.kilo
    		d4 = record.price_kilo
		todo[record.id] = d3 * d4
	return todo

    def totalArrobas(self, cr, uid, ids, field_name,arg, context=None):
    	res = {}
	for record in self.browse(cr, uid, ids, context=context):
        	d3 = record.kilo
		res[record.id] = d3 * 13.5
	return res
    _name = 'cooperativa.fruits'
    _columns = {
        'variety': fields.char('Variety', size=64, required=True),
        'reference': fields.char('Reference', size=64, required=True),
        'price_kilo': fields.integer('Price / kilo',required=True),
        'kilo': fields.integer('Kilo',required=True),
        'total': fields.integer('Total'),
        'fruit_person': fields.many2one('cooperative.member','Member'),
        'total_pesetas': fields.function(totalPesetas,type='float', store=False,string='Total pesetas'),
        'kilo_arroba': fields.function(totalArrobas,type='float', store=False,string='Total Arrobas'),
	'type_fruit': fields.selection([('olives','Olives'),('oranges','Oranges'),('mandarins','Mandarins'),('lemons','Lemons'),('almonds','Almonds'),('persimmons','Persimmons')],'Type of fruit'),
    }
cooperativa_fruits()

