var sumarr = [];
for (var i = 1; i < document.getElementsByClassName("search-results-item ").length; i++) {
	var w = document.getElementById("search-results-row-"+[i]);
	var curr = [];
	curr.push(w.getElementsByClassName("display-text")[0].innerText);
	curr.push(w.getElementsByClassName("auction-location-link")[0].innerText);
	curr.push(w.getElementsByClassName("auction-date")[0].innerText);
	if (w.getElementsByClassName("item-extra-info").length > 0) {
		curr.push(w.getElementsByClassName("item-extra-info")[0].innerText);
	}
	if (w.getElementsByClassName("dbl-bottom-margin").length > 1) {
		curr.push(w.getElementsByClassName("dbl-bottom-margin")[2].innerText);
	}
	sumarr.push(curr);
}

var textDoc = document.createElement('a');

textDoc.href = 'data:attachment/text,' + JSON.stringify(sumarr)
textDoc.target = '_blank';
textDoc.download = 'myFile.txt';
textDoc.click();