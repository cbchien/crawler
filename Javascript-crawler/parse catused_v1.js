var x = document.getElementsByClassName('xofy')[0].innerHTML.split(' ');
var maxNum = parseFloat(x[x.length - 1]);
var startNum = parseFloat(document.getElementsByClassName('xofy')[0].innerHTML.split(' ')[1]);
var parseNum = parseFloat(document.getElementsByClassName('jquery-selectbox-currentItem')[0].innerHTML.split(' ')[0]);
console.log('max number of items: ' + maxNum + ', Staring at ' + startNum + ', Parse total of ' + parseNum);


// document.querySelectorAll('[itemprop="availability"]');


// name of the tracker
document.getElementsByClassName('info')[0].getElementsByTagName('h2')[0].innerText

// category
document.getElementsByClassName('product_family')[0].innerText

// essential information
document.getElementsByClassName('essential_info')[0].innerText.split(' ')[0]



// parse the whole text
// document.getElementsByClassName('info')[0].innerText.split('\n')
resultJSON = [];
for (var i = 0; i < parseNum; i++) {
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

console.log(resultJSON);

var textDoc = document.createElement('a');

textDoc.href = 'data:attachment/text,' + JSON.stringify(sumarr)
textDoc.target = '_blank';
textDoc.download = 'myFile.txt';
textDoc.click();