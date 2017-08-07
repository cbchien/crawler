var x = document.getElementsByClassName('xofy')[0].innerHTML.split(' ');
var maxNum = parseFloat(x[x.length - 1]);
var startNum = parseFloat(document.getElementsByClassName('xofy')[0].innerHTML.split(' ')[1]);
var parseNum = parseFloat(document.getElementsByClassName('jquery-selectbox-currentItem')[0].innerHTML.split(' ')[0]);
var delta = maxNum - startNum;
var currentParseNum = (delta <= parseNum) ? (maxNum - startNum + 1) : parseNum

console.log('max number of items: ' + maxNum + ', Staring at ' + startNum + ', Parse total of ' + currentParseNum);
var totalPage = document.getElementsByClassName('pages')[0].getElementsByClassName('blockSizedLink').length;
console.log('Total page to parse :' + totalPage);

resultJSON = [];

// for (var j = 1; j < totalPage - 1; j++){
	for (var i = 0; i < currentParseNum; i++) {
		resultJSON.push({
			item: i,
			name: document.getElementsByClassName('info')[i].getElementsByTagName('h2')[0].innerText,
			category: document.getElementsByClassName('product_family')[i].innerText,
			price: document.getElementsByClassName('essential_info')[i].innerText.split('\n')[0],
			hour: document.getElementsByClassName('essential_info')[i].innerText.split('\n')[1],
			year: document.getElementsByClassName('essential_info')[i].innerText.split('\n')[2],
			location: document.getElementsByClassName('essential_info')[i].innerText.split('\n')[3]
		})
	}
	//change pages
	

	// document.getElementsByClassName('pages')[0].getElementsByClassName('blockSizedLink')[j].click()
	// setTimeout(function(){ console.log("Parsing page "+ (j+1));}, 2000);
// }

// console.log(resultJSON);

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

// JSONToCSVConvertor(resultJSON, 'track', true);


var textDoc = document.createElement('a');

textDoc.href = 'data:attachment/text,' + JSON.stringify(resultJSON)
textDoc.target = '_blank';
textDoc.download = 'myFile.txt';
textDoc.click();