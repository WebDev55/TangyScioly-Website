/*
  Programmer: Srujan Tripathi
  Most-Recent Date: 3/31/2016
  File Name: Content_Loader.js
  Description: Loads templates into site pages.
*/


//Finding page name.
var title = document.getElementByTag("TITLE").innerHTML;
var pageName = title.slice(title.indexOf("|") + 2, title.length);


//Query server to see if active page actually exists.
var response = null;
var httpRequest = new XMLHttpRequest();
httpRequest.open("GET", "", true) //Fill in server IP
httpRequest.onreadystatechange = function() {
  if(httpRequest.readyState == 4) {
    if(httpRequest.status == 200) {
      response = JSON.parse(httpRequest.responseText).pageExists;
    }
    else {
      throw "Network Error: Couldn't connect to server.";
    }
  }
};
httpRequest.send();


//If page exists, query server for templates for page.
if(response) {
  var header = jumbotron = footer = null;
  httpRequest.open("GET", "", true); //Fill in server IP
  httpRequest.onreadystatechange = function() {
    if(httpRequest.readyState == 4) {
      if(httpRequest.status == 200) {
        response = JSON.parse(httpRequest.responseText);
        header = response.headerTemplate;
        jumbotron = response.jumbotronTemplate;
        footer = response.footerTemplate;
      }
      else {
        throw "Network Error, couldn't connect to server.";
      }
    }
  };
  httpRequest.send();


  //Inject template code into document.
  
}
else {
  throw "Fatal Error: Page doesn't exist.";
}
