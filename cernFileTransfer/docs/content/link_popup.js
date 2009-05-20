var xForRefIcon = 0;
var yForRefIcon = 0;

var xForSubDiagramIcon = 0;
var yForSubDiagramIcon = 0;

var fileLinks = [];
var folderLinks = [];
var urlLinks = [];
var diagramLinks = [];
var shapeLinks = [];
var subdiagramLinks = [];

function showReferenceIcon(modelValues) {
	if (modelValues != ''){
		var xyValueArray = modelValues.split(",");
		var shapeWidth = xyValueArray[2]*1 - xyValueArray[0]*1;
		if (shapeWidth > 24){
			var diagram = document.getElementById("diagram");
			var xOffset = findPosX(diagram);
			var yOffset = findPosY(diagram);
			
			var shapeX = xyValueArray[0]*1;
			var shapeY = xyValueArray[1]*1;
			var x = shapeX + xOffset*1;
			var y = shapeY + yOffset*1 - 13;
			var h = xyValueArray[3]*1 - xyValueArray[1]*1;
			var url = xyValueArray[4];
	
			var referenceIconLayer = document.getElementById("referenceIconLayer");
		
			N = (document.all) ? 0 : 1;
			if (N) {
				referenceIconLayer.style.left = x - 3;
				referenceIconLayer.style.top = y + h;
			} else {
				referenceIconLayer.style.posLeft = x - 3;
				referenceIconLayer.style.posTop = y + h;
			}
			referenceIconLayer.style.visibility="visible"
		}
	}
}

function showSubdiagramIcon(modelValues) {
	if (modelValues != ''){
		var xyValueArray = modelValues.split(",");
		var shapeWidth = xyValueArray[2]*1 - xyValueArray[0]*1;
		if (shapeWidth > 24){
			var diagram = document.getElementById("diagram");
			var xOffset = findPosX(diagram);
			var yOffset = findPosY(diagram);
			
			var shapeRightX = xyValueArray[2]*1;
			var shapeRightY = xyValueArray[1]*1;
			var x = shapeRightX + xOffset*1 - 10;
			var y = shapeRightY + yOffset*1 - 13;
			var h = xyValueArray[3]*1 - xyValueArray[1]*1;
			var url = xyValueArray[4];
	
			var subdiagramIconLayer = document.getElementById("subdiagramIconLayer");
		
			N = (document.all) ? 0 : 1;
			if (N) {
				subdiagramIconLayer.style.left = x - 3;
				subdiagramIconLayer.style.top = y + h;
			} else {
				subdiagramIconLayer.style.posLeft = x - 3;
				subdiagramIconLayer.style.posTop = y + h;
			}
			subdiagramIconLayer.style.visibility="visible"
		}
	}
}

function storeReferenceAndSubdiagramInfos(coords, fileRefs, folderRefs, urlRefs, diagramRefs, shapeRefs, subdiagrams) {
	if (coords != ''){
	  	var xyValueArray = coords.split(",");
		var shapeWidth = xyValueArray[2]*1 - xyValueArray[0]*1;
		if (shapeWidth > 24){
			fileLinks = [];
			folderLinks = [];
			urlLinks = [];
			diagramLinks = [];
			shapeLinks = [];
			subdiagramLinks = [];
			
		  	var popup = document.getElementById("linkPopupMenuTable");
		  	
		  	for (i = 0 ; i < fileRefs.length ; i++) {
		  		fileLinks[i] = fileRefs[i];
		  	}
		  	for (i = 0 ; i < folderRefs.length ; i++) {
		  		folderLinks[i] = folderRefs[i];
		  	}
		  	for (i = 0 ; i < urlRefs.length ; i++) {
		  		urlLinks[i] = urlRefs[i];
		  	}
		  	for (j = 0 ; j < diagramRefs.length ; j++) {
		  		diagramLinks[j] = diagramRefs[j]
		  	}
		  	for (j = 0 ; j < shapeRefs.length ; j++) {
		  		shapeLinks[j] = shapeRefs[j]
		  	}
		  	for (j = 0 ; j < subdiagrams.length ; j++) {
		  		subdiagramLinks[j] = subdiagrams[j]
		  	}
		  	
		  	var diagram = document.getElementById("diagram");
		  	var xOffset = findPosX(diagram);
		  	var yOffset = findPosY(diagram);
		  	
		  	var shapeX = xyValueArray[0]*1;
		  	var shapeY = xyValueArray[1]*1;
		  	var x = shapeX + xOffset*1;
		  	var y = shapeY + yOffset*1 + 2;
		  	var w = xyValueArray[2]*1 - xyValueArray[0]*1;
		  	var h = xyValueArray[3]*1 - xyValueArray[1]*1;
		  	var url = xyValueArray[4];
		  
		  	xForRefIcon = x;
		  	yForRefIcon = y + h;

		  	shapeX = xyValueArray[2]*1;
		  	shapeY = xyValueArray[1]*1;
		  	x = shapeX + xOffset*1 - 12;
		  	y = shapeY + yOffset*1 + 2;
		  	w = xyValueArray[2]*1 - xyValueArray[0]*1;
		  	h = xyValueArray[3]*1 - xyValueArray[1]*1;
		  	url = xyValueArray[4];

		  	xForSubDiagramIcon = x;
		  	yForSubDiagramIcon = y + h;
		}
	}
}

function resetPopupForReference() {
	clearLinkPopupContent();

  	var popup = document.getElementById("linkPopupMenuTable");
  	
  	// file references
  	for (i = 0 ; i < fileLinks.length ; i++) {
	  	var fileNameUrl = fileLinks[i].split("*");
  		var name = fileNameUrl[0];
  		var url = fileNameUrl[1];

  		var row = popup.insertRow(popup.rows.length)
  		var imgPopupCell = row.insertCell(0);
  		imgPopupCell.innerHTML="<div style=\"float: left; width: 18px !important;height: 18px !important;background-image:url(../images/icons/FileReference.png) !important; background-image:url(''); filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(src='../images/icons/FileReference.png');\"></div>&nbsp;"+name
  		imgPopupCell.valign="middle"
  		imgPopupCell.destination=url
  		imgPopupCell.className="PopupMenuRowDeselected";
  		imgPopupCell.onmouseover= function onmouseover(event) { this.className="PopupMenuRowSelected"; };
  		imgPopupCell.onmouseout= function onmouseover(event) { this.className="PopupMenuRowDeselected"; };
  		imgPopupCell.onclick= function onclick(event) { window.open(this.destination) };
      
  	}

    // folder reference
  	for (i = 0 ; i < folderLinks.length ; i++) {
	  	var folderNameUrl = folderLinks[i].split("*");
  		var name = folderNameUrl[0];
  		var url = folderNameUrl[1];

  		var row = popup.insertRow(popup.rows.length)
  		var imgPopupCell = row.insertCell(0);
  		imgPopupCell.innerHTML="<div style=\"float: left; width: 18px !important;height: 18px !important;background-image:url(../images/icons/FolderReference.png) !important; background-image:url(''); filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(src='../images/icons/FolderReference.png');\"></div>&nbsp;"+name
  		imgPopupCell.valign="middle"
  	  	imgPopupCell.destination=url
  	  	imgPopupCell.className="PopupMenuRowDeselected";
  		imgPopupCell.onmouseover= function onmouseover(event) { this.className="PopupMenuRowSelected"; };
  		imgPopupCell.onmouseout= function onmouseover(event) { this.className="PopupMenuRowDeselected"; };
  		imgPopupCell.onclick= function onclick(event) { window.open(this.destination) };
  	}

    // url reference
  	for (i = 0 ; i < urlLinks.length ; i++) {
  	  var row = popup.insertRow(popup.rows.length)
  	  var imgPopupCell = row.insertCell(0);
      imgPopupCell.innerHTML="<div style=\"float: left; width: 18px !important;height: 18px !important;background-image:url(../images/icons/UrlReference.png) !important; background-image:url(''); filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(src='../images/icons/UrlReference.png');\"></div>&nbsp;"+urlLinks[i]
  	  imgPopupCell.valign="middle"
      imgPopupCell.destination=urlLinks[i]
      imgPopupCell.className="PopupMenuRowDeselected";
      imgPopupCell.onmouseover= function onmouseover(event) { this.className="PopupMenuRowSelected"; };
      imgPopupCell.onmouseout= function onmouseover(event) { this.className="PopupMenuRowDeselected"; };
      imgPopupCell.onclick= function onclick(event) { window.open(this.destination) };

  	}

    // diagram reference
  	for (j = 0 ; j < diagramLinks.length ; j++) {
	  	var diagramUrlNameType = diagramLinks[j].split("/");
  		var url = diagramUrlNameType[0];
  		var name = diagramUrlNameType[1];
  		var type = diagramUrlNameType[2];
  		var imgSrc = '../images/icons/'+type+'.png';
  		  		  	
  		var row = popup.insertRow(popup.rows.length)
  		var imgPopupCell = row.insertCell(0);
  		imgPopupCell.innerHTML="<div style=\"float: left; width: 18px !important;height: 18px !important;background-image:url(" + imgSrc + ") !important; background-image:url(''); filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(src='" + imgSrc + "');\"></div>&nbsp;"+name
  		imgPopupCell.valign="middle"
  		imgPopupCell.destination=url
  		imgPopupCell.className="PopupMenuRowDeselected";
  		imgPopupCell.onmouseover= function onmouseover(event) { this.className="PopupMenuRowSelected"; };
  		imgPopupCell.onmouseout= function onmouseover(event) { this.className="PopupMenuRowDeselected"; };
  		imgPopupCell.onclick= function onclick(event) { window.open(this.destination,'_content_pane') };
  	}

    // shape reference
  	for (j = 0 ; j < shapeLinks.length ; j++) {
	  	var shapeUrlNameType = shapeLinks[j].split("/");
  		var url = shapeUrlNameType[0];
  		var name = shapeUrlNameType[1];
  		var type = shapeUrlNameType[2];
  		var imgSrc = '../images/icons/'+type+'.png';
  		  		  	
		var row = popup.insertRow(popup.rows.length)
		var row = popup.insertRow(popup.rows.length)
		var imgPopupCell = row.insertCell(0);
		imgPopupCell.innerHTML="<div style=\"float: left; width: 18px !important;height: 18px !important;background-image:url(" + imgSrc + ") !important; background-image:url(''); filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(src='" + imgSrc + "');\"></div>&nbsp;"+name
		imgPopupCell.valign="middle"
		imgPopupCell.destination=url
		imgPopupCell.className="PopupMenuRowDeselected";
		imgPopupCell.onmouseover= function onmouseover(event) { this.className="PopupMenuRowSelected"; };
		imgPopupCell.onmouseout= function onmouseover(event) { this.className="PopupMenuRowDeselected"; };
		if (type.length > 0){
			imgPopupCell.onclick= function onclick(event) { window.open(this.destination,'_content_pane') };
		}
  	}
}


function resetPopupForSubdiagram() {
	clearLinkPopupContent();

  	var popup = document.getElementById("linkPopupMenuTable");
  	
    // subdiagram
  	for (j = 0 ; j < subdiagramLinks.length ; j++) {
	  	var diagramUrlNameType = subdiagramLinks[j].split("/");
  		var url = diagramUrlNameType[0];
  		var name = diagramUrlNameType[1];
  		var type = diagramUrlNameType[2];
  		var imgSrc = '../images/icons/'+type+'.png';
  		  		  	
  		var row = popup.insertRow(popup.rows.length)
  		var imgPopupCell = row.insertCell(0);
  		imgPopupCell.innerHTML="<div style=\"float: left; width: 18px !important;height: 18px !important;background-image:url(" + imgSrc + ") !important; background-image:url(''); filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(src='" + imgSrc + "');\"></div>&nbsp;"+name
  		imgPopupCell.valign="middle"
  		imgPopupCell.destination=url
  		imgPopupCell.className="PopupMenuRowDeselected";
  		imgPopupCell.onmouseover= function onmouseover(event) { this.className="PopupMenuRowSelected"; };
  		imgPopupCell.onmouseout= function onmouseover(event) { this.className="PopupMenuRowDeselected"; };
  		imgPopupCell.onclick= function onclick(event) { window.open(this.destination,'_content_pane') };
  	}
}

function movePopupPositionToReferenceIconPosition() {
	movePopupPositionToSpecificPosition(xForRefIcon, yForRefIcon);
}

function movePopupPositionToSubdiagramIconPosition() {
	movePopupPositionToSpecificPosition(xForSubDiagramIcon, yForSubDiagramIcon);
}

function movePopupPositionToCursorPosition(event) {
  	var diagram = document.getElementById("diagram");
  	var xOffset = 0;
  	var yOffset = 0;

  	var e = (window.event) ? window.event : event;
  	xOffset = e.clientX;
  	yOffset = e.clientY;
  	
	if (document.all){
		if (!document.documentElement.scrollLeft)
			xOffset += document.body.scrollLeft;
		else
			xOffset += document.documentElement.scrollLeft;
               
		if (!document.documentElement.scrollTop)
			yOffset += document.body.scrollTop;
		else
			yOffset += document.documentElement.scrollTop;
			
	}else{
		xOffset += window.pageXOffset;
		yOffset += window.pageYOffset;
	}
  	
  	var nX = xOffset*1;
  	var nY = yOffset*1;

  	movePopupPositionToSpecificPosition(nX, nY);
}

function movePopupPositionToSpecificPosition(x, y) {
  	var popupLayer = document.getElementById("linkPopupMenuLayer");
  	if (N) {
  		popupLayer.style.left = x;
  		popupLayer.style.top = y;
  	} else {
  		popupLayer.style.posLeft = x;
  		popupLayer.style.posTop = y;
  	}
}

function switchPopupShowHideStatus(){
	var popup = document.getElementById("linkPopupMenuTable");
  	if (popup.style.visibility=="visible") {
		hideLinkPopup();
	}else{
  		showLinkPopup();
	}
}

function adjustPopupPositionForSpotLightTable() {
	movePopupPositionToSpecificPosition(cursorX,cursorY);
}

function showLinkPopup(){
	var popup = document.getElementById("linkPopupMenuTable");
	popup.style.visibility="visible"
}

function hideLinkPopup(){
	var popup = document.getElementById("linkPopupMenuTable");
	popup.style.visibility="hidden"
}

function clearLinkPopupContent(){
	var popup = document.getElementById("linkPopupMenuTable");
	for (i = popup.rows.length ; i >0 ; i--) {
		popup.deleteRow(0);
	}
}