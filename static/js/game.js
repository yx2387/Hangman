// Global variables
var dict;
var ans;
var word;
var score;
var show;

// Initiate the playfield, the dictionary etc.
function start_game(){
	ans = $('#word').attr('data-value');
	word = ans.toLowerCase().split("");
	dict = {};
	tries = 10;
	//alert(word);
	for (i = 0; i < word.length; i++) {
		if (dict[word[i]] == undefined ){
			dict[word[i]] = [i];
		}
		else{
			dict[word[i]].push(i);
		}
	}
	show = "_".repeat(word.length).split("");
	document.getElementById("test").innerHTML = show.join("");
}

// Generate a new word for a new game
function new_word(){
	$.get('/new_word', function(data) {
		// Enable all buttons
		$(':button').prop('disabled', false);
		// Update Score
		var s = $( "#score" ).text();
		var b = $( "#best" ).text();
		s = s.split(': ');
		b = b.split(': ');
		t = parseInt(tries, 10);
		s[1] = parseInt(s[1],10);
		s[1] += t;
		b[1] = Math.max(s[1],parseInt(b[1])).toString();
		$.post("/score",{
			"score": s[1]
		});
		s = s.join(': ');
		b = b.join(': ');
		$('#score').html(s);
		$('#best').html(b);

		// Update play field
		ans = data;
		word = ans.toLowerCase().split("");
		dict = {};
		tries = 10;

		for (i = 0; i < word.length; i++) {
			if (dict[word[i]] == undefined ){
				dict[word[i]] = [i];
			}
			else{
				dict[word[i]].push(i);
			}
		}
		show = "_".repeat(word.length).split("");
		document.getElementById("test").innerHTML = show.join("");
		switch_img(tries);
	});
}

// Update the image based on number of attempts remain
function switch_img(num){
	i = 10 - parseInt(num, 10);
	$('.container3').css('background-image','url(../static/image/'+ i.toString() +'.png)');
}

// function called when a guess has been made
function guess(elem){
	var x = elem.id;
	document.getElementById(x).disabled = true;
	// Wrong guess
	if (dict[x] == undefined){
		tries--;
		switch_img(tries);
		// Player loses
		if (tries == 0){
			var s = $( "#score" ).text();
			var b = $( "#best" ).text();
			s = s.split(': ');
			b = b.split(': ');
			document.getElementById('modal_head').innerHTML = "Oops...";
			document.getElementById('modal_body').innerHTML = "You Lost!! :( <br>Your score: "+s[1]+"<br>Your best score: "+b[1];
			document.getElementById('test').innerHTML = word.join("")
			$('#score').html('SCORE: 0');
			// Send score to backend
			$.post("/score",{
				"score": s[1]
			});
			// Show modal
			$("#myModal").modal();
		}
	}
	// Right guess
	else{
		for (i = 0; i < dict[x].length; i++){
			show[dict[x][i]] = word[dict[x][i]];
		}
		document.getElementById("test").innerHTML = show.join("");
	}
	// Player Wins
	if(show.join("")===word.join("")){
		document.getElementById('modal_head').innerHTML = "Congratulations!!";
		document.getElementById('modal_body').innerHTML = "You Win!! :) <br>Attempts Left:"+tries;

		// Show modal
		$("#myModal").modal();
		
	}
}

// Logout
function logout(){
	$.post("/logout", function(){
    });
}

// Resize image when window size changes
$(window).resize(function(){
	var cw = $('.container3').width();
	$('.container3').css({
	    'height': cw + 'px'
	});
});

// New round after modal closes
$('#myModal').on('hidden.bs.modal', function () {
	new_word();
});

// Start game when page ready
$(function(){
	start_game();
	var cw = $('.container3').width();
	$('.container3').css({
	    'height': cw + 'px'
	});
});