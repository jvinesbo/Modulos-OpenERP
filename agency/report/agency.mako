<html>
  <head>
  <style type="text/css">
  ${css}
  div.header {
  	 border-bottom: 2px solid black;
           width: 100%;
  	 }
  	 
  span.header {
  	display: inline-block;
  	text-align: left;
  	font-size: 12;
  	font-weight: bold;
  	padding-left: 6px;
  	 }
  div.list {
  	page-break-inside: avoid;
           width: 100%;
  	border-bottom:1px solid gray;
  	}
  
  span.list {
  	display: inline-block;
  	text-align: left;
  	font-size: 12;
  	padding-right: 6px;
          vertical-align: middle;
  	margin-top: 7px;
  	padding-bottom: 2px;
  	page-break-inside: avoid;
          min-height: 30px;
  	}
  </style>
  </head>
  <body>
  %for o in objects :
  
  <div class="address">
  	
	<p>
		<span class="header" style="width: 10%;">${_("Client Id: ")}${o.partner_id.name}</span>
	</p>

	<p>
		<span class="header" style="width: 10%;">${_("Total: ")}${o.amount_total}</span>
	</p>

  	<div class="header">
  		<span class="header" style="width: 10%;">${_("Day Start")}</span>
  		<span class="header" style="width: 10%;">${_("Day End")}</span>
  		<span class="header" style="width: 10%;">${_("Total Days")}</span>
  		<span class="header" style="width: 30%;">${_("Hotel Id")}</span>
  	</div>
  
  
  	%for line in o.scalas :
  
  	<div class="list">
  		<span class="list" style="width: 10%;">${line.day_start}</span>
  		<span class="list" style="width: 10%;">${line.day_end}</span>
  		<span class="list" style="width: 10%;">${line.total_days}</span>
  		<span class="list" style="width: 30%;">${line.hotel_id.name}</span>
  	</div>
  	%endfor
  
  
  </div>
  %endfor
  </body>
  </html>
