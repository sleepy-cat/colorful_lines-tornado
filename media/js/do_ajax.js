// AJAX handling of high scores.
// 
// Part of the Colorful Lines game
//    by Eli Bendersky (http://eli.thegreenplace.net)
//
// This code is in the public domain
//

// Initiates the submission of a new high score
//
var submit_highscore = function(name, score, token) {
    if (name != "" && score != "") {
        var data = { 
            name:   name, 
            score:  score,
            token:  token
        };
        var args = { 
            type: "POST", 
            url:"/colorful_lines/submit_score/", 
            data: data, 
            complete: done_score_submit 
        };
        $.ajax(args);
    }
};


// Score submit response callback.
//
var done_score_submit = function(res, status) {
    if (status === "success") {
        update_table();
    } else {
    }
};


// Initiates a table update
// 
var update_table = function() {
    loading_image_on();
    get_highscores(done_update_table);
    return true;
}


// Update table response callback. Updates the scores in the HTML
// table.
//
var done_update_table = function(res, status) {
    var scores = parse_highscores_response(res, status);
    
    if (status !== null) {    
        $("#scorestable tbody").empty();
        for (var i in scores) {
            var new_row = '<tr>';
            new_row += '<td>' + (scores.length - i).toString() + '</td>';
            new_row += '<td>' + scores[i].name + '</td>';
            new_row += '<td>' + scores[i].score.toString() + '</td>';
            new_row += '</tr>';
            $("#scorestable tbody").prepend($(new_row));
        }
    }
    
    loading_image_off();
};


// Parses the JSON response from the server and returns the 
// array of scores.
//
function parse_highscores_response(res, status) {
    if (status === 'success') {
        try {
            var res_data = eval('(' + res.responseText + ')');
            return res_data.scores;
        } 
        catch (e) {
            // retry: resolves rare and strange errors with chrome
            // when it fails for some reason to get back a normal
            // response and gets an empty one.
            //
            get_highscores(done_update_table);
        }
    } else {
        return null;
    }
}


// Executes a request to get updated scores from the server,
// registering the given callback as the completion function.
//
var get_highscores = function(complete_func) {
    var args = {
        type:       "POST",
        url:        "/colorful_lines/get_highscores/",
        complete:   complete_func,
    };
    $.ajax(args);
};


// Executes a request to get a token from the server, registering
// the given callback as the completion function
//
var get_token = function(complete_func) {
    // Taking a different route here, just for kicks: 
    // json datatype and 'success' callback. Therefore the given
    // complete_func is called only on success as is given a 
    // single argument.
    //
    var args = {
        type:       "POST",
        url:        "/colorful_lines/get_token/",
        dataType:   'json',
        success:    complete_func,
    };
    $.ajax(args);
}


// The "loading image" is an image in the 'imagestub' div used to
// show a "loading" animation while the table is being updated.
// These functions switch it on and off...
//
function loading_image_on() {
    $("#scorestable").hide();
    $("#imagestub").html("<img src=\"/colorful_lines/media/img/img-loading.gif\"></img>");
}

function loading_image_off() {
    $("#imagestub").html("");
    $("#scorestable").show();
}


// We want to update the table when the document loads
//
$(document).ready(update_table);
