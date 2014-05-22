{
        "name" : "Agency",
        "version" : "0.1",
        "author" : "Juan Viñes Bordera",
        "website" : "http://accesoadatos.freeiz.com/",
        "category" : "Agency Travel",
        "description":  """ 
Module for travel management course developed by the institute 2nd DAM IES Dr.Lluis Simarro Lacabra . 
A travel agency needs a module for OpenERP that can fulfill their needs:
Customers want the agency to organize tours to various European cities. The agency wants to
Plan your trip with OpenERP to then be able to estimate and invoice these tours.""",
        "depends" : ['base','report_webkit','product','sale'],
        "init_xml" : [ ],
        "demo_xml" : [ ],
        "update_xml" : ['agency_view.xml','report/agency_report_header.xml','agency_report.xml'],
        "installable": True
}
