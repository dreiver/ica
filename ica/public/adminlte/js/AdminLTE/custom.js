$(function() {
    $( document ).ready(function() {
        $(document).pjax('a[data-pjax]', '#main-content')
        //$('a[data-pjax]').pjax()
    });

    window.onload = function(){
        //alert('caca0')
    }
});