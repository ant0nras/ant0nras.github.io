const ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king'];
const suits = ['spades', 'hearts', 'clubs', 'diamonds'];
const maxSelections = 6;

function buildTable(results) {
    results.forEach(function(result) {
        var row = "";
        for (let i = 0; i < 2; i++) {
            var cell = "";
            result[i].forEach(function(card) { 
                const source = "static/images/playing_cards_25_compressed/" + ranks[card[0] - 1] + "_of_" + suits[card[1]] + ".png";
                var cardimg = "<div class = \"card\"><img src = " + source + "></img></div>";
                cell += cardimg;
            });
            row += "<td><div class = \"tablesets\">" + cell + "</div></td>";
        }

        row += "<td>" + Math.round(result[2] * 100) / 100 + "</td>";
        $("#table-results").append("<tr class = \"datarow\">" + row + "</tr");      
    });
}

$(document).ready(function() {
    var selected = 0;

    $("input:checkbox").on('click', function() {
        // selected card is unselected
        if ($(this).parent().hasClass("moved")) {
            $(this).parent().removeClass("moved");
            // $(this).parent().addClass("unmoved");
            selected--;
        }
        // unselected card is selected
        else {
            // $(this).parent().removeClass("unmoved");
            $(this).parent().addClass("moved");
            selected++;
        }
        //if six cards have been selected, disable all other checkboxes (other cards can no longer be selected)
        if (selected == maxSelections) {
            $("input:checkbox:not(:checked)").attr('disabled', 'true');
        }
        else {
            $("input:checkbox:not(:checked)").removeAttr('disabled');
        }
        //update selected counter
        $("#selected").html("Selected " + String(selected) + "/6")
    });
    
    $("input:radio").on('click', function() {
        
    });

    $("input").on('click', function() {
        if (selected == 6 && $("input:radio").is(':checked')) {
            //enable submit
            $(":submit").removeAttr('disabled');
        }
        else {
            //disable submit
            $(":submit").attr('disabled', 'true');
        }
    });

    $("form").on("submit", function(e) {
        $("#form-content").addClass("grayout");
        $("#load").addClass("loader");
        var values = {};
        $(this).serializeArray().forEach(function(elem) {
            values[elem["name"]] = elem["value"];
        });
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/',
            data: values,
            success: function(results) {
                buildTable(results);

                //hide first content and get rid of loader
                $("#content-1").addClass("hidden");
                $("#load").removeClass("loader");
                // reveal table of results
                $("#content-2").removeClass("hidden");
            }
        });
    });

    $("#trynew > button").on("click", function() {
        //clear table and hide
        $(".datarow").remove();
        $("#content-2").addClass("hidden");
        //unshade and reveal first content, reset form
        $("#form-content").removeClass("grayout");
        $("form").trigger("reset");
        $(".card").removeClass("moved");
        $("input:checkbox").removeAttr("disabled");
        selected = 0;
        $("#selected").html("Selected " + String(selected) + "/6")
        $(":submit").attr('disabled', 'true');
        $("#content-1").removeClass("hidden");
    });
});

$(window).on("load", function() {
    $("#deck").removeClass("hidden");
    console.log($("#deck").hasClass("hidden"));
});


