var x = document.getElementsByClassName('section-result-text-content')

resultJSON = [];

function parseResult(num){
	for (var i = 0; i < num; i++) {
		var name = x[i].getElementsByClassName('section-result-title')[0].innerText
		var category = x[i].getElementsByClassName('section-result-details')[0].innerText
		var location = x[i].getElementsByClassName('section-result-location')[0].innerText
		try {
			var ratingScore = x[i].getElementsByClassName('cards-rating-score')[0].innerText
			var rating = x[i].getElementsByClassName('section-result-num-ratings')[0].innerText
		} catch(err) {
        	var ratingScore = ''
        	var rating = ''
    	} 

    	try {
    		var opening = x[i].getElementsByClassName('section-result-opening-hours')[0].innerText
    	} catch(err) {
        	var opening =  ''
    	} 

		resultJSON.push({
			name: name,
			ratingScore: ratingScore,
			rating: rating,
			category: category,
			location: location,
			opening: opening
		})
	}
}

function JSONToCSVConvertor(JSONData, ReportTitle, ShowLabel) {
    //If JSONData is not an object then JSON.parse will parse the JSON string in an Object
    var arrData = typeof JSONData != 'object' ? JSON.parse(JSONData) : JSONData;
    var CSV = '';    
    if (ShowLabel) {
        var row = "";
        for (var index in arrData[0]) {
            row += index + ',';
        }
        row = row.slice(0, -1);
        CSV += row + '\r\n';
    }
    
    for (var i = 0; i < arrData.length; i++) {
        var row = "";
        for (var index in arrData[i]) {
            row += '"' + arrData[i][index] + '",';
        }
        row.slice(0, row.length - 1);
        CSV += row + '\r\n';
    }

    if (CSV == '') {        
        alert("Invalid data");
        return;
    }   
    var fileName = "MyReport_";
    fileName += ReportTitle.replace(/ /g,"_");   
    var uri = 'data:text/csv;charset=utf-8,' + escape(CSV);
    //this trick will generate a temp <a /> tag
    var link = document.createElement("a");    
    link.href = uri;
    link.style = "visibility:hidden";
    link.download = fileName + ".csv";
    //this part will append the anchor tag and remove it after automatic click
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

JSONToCSVConvertor(resultJSON, 'track', true);


var textDoc = document.createElement('a');

textDoc.href = 'data:attachment/text,' + JSON.stringify(resultJSON)
textDoc.target = '_blank';
textDoc.download = 'myFile.txt';
textDoc.click();