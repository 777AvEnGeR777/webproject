$(document).ready(function() {
    $('#.btn.like-question').click(function(){
        var id, type;
        id = $(this).attr("data-id");
        type = $(this).attr("like-type");
        $.get('/rate_question/', {question_id: id, type: type}, function(data){
            $('#rating-count-' + id).html(data);
        });
    });  
    $('#.btn.like-answer').click(function(){
        var id, type;
        id = $(this).attr("data-id");
        type = $(this).attr("like-type");
        $.get('/rate_answer/', {answer_id: id, type: type}, function(data){
            $('#answer-rating-count-' + id).html(data);
        });
    });    
});
