// from https://github.com/psolom/RichFilemanager/wiki/How-to-use-the-filemanager-from-a-simple-textfield
// File Picker modification for FCK Editor v2.0 - www.fckeditor.net
// by: Pete Forde <pete@unspace.ca> @ Unspace Interactive
var urlobj;
var oWindow = null;

function ensure_closed_window()
{
  if (oWindow) {
    oWindow.close();
    oWindow = null;
  }
}

function BrowseServer(fm_url, obj)
{
  urlobj = obj;
  OpenServerBrowser(
  fm_url + "?langCode=zh-cn",
  screen.width * 0.7,
  screen.height * 0.7 ) ;
}

function OpenServerBrowser( url, width, height )
{
  var iLeft = (screen.width - width) / 2 ;
  var iTop = (screen.height - height) / 2 ;
  var sOptions = "toolbar=no,status=no,resizable=yes,dependent=yes" ;
  sOptions += ",width=" + width ;
  sOptions += ",height=" + height ;
  sOptions += ",left=" + iLeft ;
  sOptions += ",top=" + iTop ;
  ensure_closed_window();
  oWindow = window.open( url, "BrowseWindow", sOptions ) ;
}

function SetUrl( url, width, height, alt )
{
  document.getElementById(urlobj).value = url ;
  document.getElementById("img_" + urlobj).src = url ;
  document.getElementById("img_" + urlobj).hidden = false ;
  document.getElementById("a_" + urlobj).hidden = false ;
  ensure_closed_window();
}

function ClearField(obj)
{
    console.log("ClearField" + obj);
    document.getElementById(obj).value = "" ;
    document.getElementById("img_" + obj).src = "" ;
    document.getElementById("img_" + obj).hidden = true ;
    document.getElementById("a_" + obj).hidden = true ;
}