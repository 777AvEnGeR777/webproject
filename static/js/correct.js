$(document).ready(function() {
    $('input[type="checkbox"]').click(function(){
        var id, state;
        id = $(this).attr("data-id");
        if($(this).is(":checked"))
            state = true;
        else
            state = false;
        $.get('/mark_answer/', {answer_id: id, state: state}, function(data){});
    });    
});
