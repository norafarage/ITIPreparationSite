
$(document).ready(function(){/* jQuery toggle layout */
    $('#btnToggle').click(function(){
      if ($(this).hasClass('on')) {
        $('#main .col-md-6').addClass('col-md-4').removeClass('col-md-6');
        $(this).removeClass('on');
      }
      else {
        $('#main .col-md-4').addClass('col-md-6').removeClass('col-md-4');
        $(this).addClass('on');
      }
    });



});


function Vote(type, id, vote,event){


        $.post('/vote/', {id:id, type:type, vote:vote}, function(response) {
                if (response) {
                    $('#'+type+id).text(response.votes);
                }
            });
        event.preventDefault();
    }