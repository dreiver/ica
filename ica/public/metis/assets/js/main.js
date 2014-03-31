$(function() {
    //prototype para calcular el tiempo de segundos
    Number.prototype.toHHMMSS = function () {
        var seconds = Math.floor(this),
            hours = Math.floor(seconds / 3600);
            seconds -= hours*3600;
        var minutes = Math.floor(seconds / 60);
            seconds -= minutes*60;

        if (hours   < 10) {hours   = "0"+hours;}
        if (minutes < 10) {minutes = "0"+minutes;}
        if (seconds < 10) {seconds = "0"+seconds;}
        return hours+':'+minutes+':'+seconds;
    }

    $('a[rel=tooltip]').tooltip();

    // make code pretty
    window.prettyPrint && prettyPrint();

    /*----------- BEGIN TABLESORTER CODE -------------------------*/
    /* required jquery.tablesorter.min.js*/
    //$(".sortableTable").tablesorter();
    /*----------- END TABLESORTER CODE -------------------------*/

    
    
    $('.minimize-box').on('click', function(e){
        e.preventDefault();
        var $icon = $(this).children('i');
        if($icon.hasClass('icon-chevron-down')) {
            $icon.removeClass('icon-chevron-down').addClass('icon-chevron-up');
        } else if($icon.hasClass('icon-chevron-up')) {
            $icon.removeClass('icon-chevron-up').addClass('icon-chevron-down');
        }
    });
    $('.minimize-box').on('click', function(e){
        e.preventDefault();
        var $icon = $(this).children('i');
        if($icon.hasClass('icon-minus')) {
            $icon.removeClass('icon-minus').addClass('icon-plus');
        } else if($icon.hasClass('icon-plus')) {
            $icon.removeClass('icon-plus').addClass('icon-minus');
        }
    });

    $('.close-box').click(function() {
        $(this).closest('.box').hide('slow');
    });

    $('#changeSidebarPos').on('click', function(e) {
        $('body').toggleClass('hide-sidebar');
    });
});


var pstn = { trunks: 0, servers: 0 }
var conf = { }
get_conf();

/*----------- BEGIN index-graph CODE -------------------------*/
var options = {
    lines: {
        show: true
    },
    points: {
        show: true
    },
    grid: {
        clickable: true
    },
    xaxis: {
        mode: "time",
        timeformat: "%d/%b"
    },
    yaxis: {
        min: 0
    }
};

var data = [];
var plot;
// Fetch one series, adding to what we already have
var alreadyFetched = {};
/*----------- END index-graph CODE -------------------------*/

/*--------------------------------------------------------
 BEGIN IndexGraph SCRIPTS
 ---------------------------------------------------------*/
function IndexGraph() {

    /*----------- BEGIN SPARKLINE CODE -------------------------*/
    /* required jquery.sparkline.min.js*/

    /** This code runs when everything has been loaded on the page */
    /* Inline sparklines take their values from the contents of the tag */
    $('.inlinesparkline').sparkline();

    /* Sparklines can also take their values from the first argument
     passed to the sparkline() function */
    var myvalues = [10, 8, 5, 7, 4, 4, 1];
    $('.dynamicsparkline').sparkline(myvalues);

    /* The second argument gives options such as chart type */
    $('.dynamicbar').sparkline(myvalues, {type: 'bar', barColor: 'green'});

    /* Use 'html' instead of an array of values to pass options
     to a sparkline with data in the tag */
    $('.inlinebar').sparkline('html', {type: 'bar', barColor: 'red'});


    $(".sparkline.bar_week").sparkline('html', {
        type: 'bar',
        height: '40',
        barWidth: 5,
        barColor: '#4d6189',
        negBarColor: '#a20051'
    });

    /* [5, 6, 7, 2, 0, -4, -2, 4]
    $(".sparkline.line_day").sparkline([5, 6, 7, 9, 9, 5, 4, 6, 6, 4, 6, 7], {
        type: 'line',
        height: '40',
        drawNormalOnTop: false
    });*/
    $(".sparkline.line_day").sparkline('html', {
        type: 'line',
        height: '40',
        drawNormalOnTop: false
    });

    $(".sparkline.pie_week").sparkline([1, 1, 2], {
        type: 'pie',
        width: '40',
        height: '40'
    });

    $('.sparkline.stacked_month').sparkline(['0:2', '2:4', '4:2', '4:1'], {
        type: 'bar',
        height: '40',
        barWidth: 10,
        barColor: '#4d6189',
        negBarColor: '#a20051'
    });
    /*----------- END SPARKLINE CODE -------------------------*/



    /*----------- BEGIN index-graph CODE -------------------------*/

    plot = $.plot("#trigo", data, options);
    function onDataReceived(series) {

        // Extract the first coordinate pair; jQuery has parsed it, so
        // the data is now just an ordinary JavaScript object
        // Push the new data onto our existing data array
        if (!alreadyFetched[series.label]) {
            alreadyFetched[series.label] = true;
            data.push(series);
        }
        $.plot("#trigo", data, options);
    }

    $.ajax({
        url: "/api/v1/calls/week_graph",
        type: "GET",
        dataType: "json",
        success: onDataReceived
    });
}
/*--------------------------------------------------------
 END IndexGraph SCRIPTS
 ---------------------------------------------------------*/

/*--------------------------------------------------------
 BEGIN FORM-GENERAL.HTML SCRIPTS
 ---------------------------------------------------------*/
function formGeneral() {
    $('.with-tooltip').tooltip({
        selector: ".input-tooltip"
    });

    /*----------- BEGIN autosize CODE -------------------------*/
    $('#autosize').autosize();
    /*----------- END autosize CODE -------------------------*/
}
/*--------------------------------------------------------
 END FORM-GENERAL.HTML SCRIPTS
 ---------------------------------------------------------*/





/*--------------------------------------------------------
 BEGIN changepasswd SCRIPTS
 ---------------------------------------------------------*/
 function ChangePasswd() {
    $('#changepasswd').validate({
        rules: {
            required: "required",
            username: {
                required: true,
                minlength: 4,
                maxlength: 20
            },
            password: {
                required: true,
                minlength: 5
            },
            passwordnew: {
                required: true,
                minlength: 5
            },
            passwordconfirm: {
                required: true,
                minlength: 5,
                equalTo: "#passwordnew"
            }
        },

        errorClass: 'help-inline',
        errorElement: 'span',
        highlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error').addClass('success');
        }
    });
 }
 /*--------------------------------------------------------
 END changepasswd SCRIPTS
 ---------------------------------------------------------*/


 /*--------------------------------------------------------
 BEGIN login SCRIPTS
 ---------------------------------------------------------*/
 $(document).ready(function () {

         $( "#username, #password" ).keyup(function( e ){
            if ( (e.which == 13) && !event.shiftKey ) {
                var username = $("#username").val();
                var password = $("#password").val();
                authenticate(username, password);
            }
         });

        $( "#Auth" ).click(function () {
            var username = $("#username").val();
            var password = $("#password").val();
            authenticate(username, password);
        });

        $( "#Change" ).click(function () {
            var username        = $("#username").val();
            var password        = $("#password").val();
            var passwordnew     = $("#passwordnew").val();
            var passwordconfirm = $("#passwordconfirm").val();
            changepasswd(username, password, passwordnew, passwordconfirm);
        });

    });
 /*--------------------------------------------------------
 END login SCRIPTS
 ---------------------------------------------------------*/


 function changepasswd(username, password, passwordnew, passwordconfirm) {
    $.ajax({
        type: "POST",
        url: "/api/v1/acces/changepasswd",
        data: "username="+username+"&password="+password+"&passwordnew="+passwordnew+"&passwordconfirm="+passwordconfirm+"&action=changepasswd",
        success: function(resp)
        {
            setTimeout(function(){
                if( resp['succes']['code'] ) {
                    $("#login_loader, #login_change").css('display', 'none');
                    $("#login_ok").css('display', 'inline-block');
                    setTimeout(function(){ authenticate(username, password); }, 500);
                } else {
                    $("#login_loader, #login_change").css('display', 'none');
                    $("#login_error").css('display', 'inline-block');
                }
            }, 500);
        },
        error: function()
        {
            setTimeout(function(){
                $("#login_loader, #login_change").css('display', 'none');
                $("#login_error").css('display', 'inline-block');
            }, 500);
        },
        beforeSend:function()
        {
            $("#login_ok").css('display', 'none');
            $("#login_error").css('display', 'none');
            $("#login_loader").css('display', 'inline-block');
        }
    });
    return false;
}


 function authenticate(username, password) {
    $.ajax({
        type: "POST",
        url: "/api/v1/acces/login",
        data: "username="+username+"&password="+password+"&action=login",
        success: function(resp)
        {
            setTimeout(function(){
                if( resp['succes']['code'] ) {
                    $("#login_loader").css('display', 'none');
                    $("#login_ok").css('display', 'inline-block');
                    setTimeout(function(){ window.location='/'; }, 500);
                } else {

                    if ( resp['succes']['message'] == "redirect" )
                        window.location=resp['succes']['destination'];
                    else {
                        $("#login_loader").css('display', 'none');
                        $("#login_error").css('display', 'inline-block');
                    }
                }
            }, 500);
        },
        error: function()
        {
            setTimeout(function(){
                $("#login_loader").css('display', 'none');
                $("#login_error").css('display', 'inline-block');
            }, 500);
        },
        beforeSend:function()
        {
            $("#login_ok").css('display', 'none');
            $("#login_error").css('display', 'none');
            $("#login_loader").css('display', 'inline-block');
        }
    });
    return false;
}

/*--------------------------------------------------------
 BEGIN FORM-VALIDATION.HTML SCRIPTS
 ---------------------------------------------------------*/
function formValidation() {
    /*----------- BEGIN validationEngine CODE -------------------------*/
    $('#popup-validation').validationEngine();
    /*----------- END validationEngine CODE -------------------------*/

    /*----------- BEGIN validate CODE -------------------------*/
    /*----------- ezequiel CODE -------------------------*/

    $('#sucursal_0_0').uniform().parent().css( "margin-bottom", "20px" );
    $('#audiopre, #audiopost, #audiodesp').uniform();

    $('#inline-validate-update').validate({
        rules: {
            required: "required",
            piloto: {
                required: true,
                minlength: 4,
                maxlength: 4,
                min: 1000,
                max: 9999
            },
            nombre: {
                required: true,
                maxlength: 25,
                minlength: 4
            },
            fechacarga: {
                required: false,
                minlength: 10,
                maxlength: 10
            },
            /*audiopre: {
                required: true,
                accept: "audio/*"
            },
            audiopost: {
                required: false,
                accept: "audio/*"
            },*/
            voz: {
                required: true
            },
            bin_0: {
                required: true
            },
            producto_0_0: {
                required: true,
                minlength: 2,
                maxlength: 2,
                min: 00,
                max: 99
            }
        },

        errorClass: 'help-inline',
        errorElement: 'span',
        highlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error').addClass('success');
        }
    });

    $('#inline-validate').validate({
        rules: {
            required: "required",
            piloto: {
                required: true,
                minlength: 4,
                maxlength: 4,
                min: 1000,
                max: 9999
            },
            nombre: {
                required: true,
                maxlength: 25,
                minlength: 4
            },
            fechacarga: {
                required: false,
                minlength: 10,
                maxlength: 10
            },
            audiopre: {
                required: true,
                accept: "audio/*"
            },
            audiopost: {
                required: false,
                accept: "audio/*"
            },
            audiodesp: {
                required: false,
                accept: "audio/*"
            },
            voz: {
                required: true
            },
            bin_0: {
                required: true
            },
            producto_0_0: {
                required: true,
                minlength: 2,
                maxlength: 2,
                min: 00,
                max: 99
            }
        },

        errorClass: 'help-inline',
        errorElement: 'span',
        highlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error').addClass('success');
        }
    });

    $('#fechacarga-dp, #fechacarga-dp-update').datepicker();

    //Boton agregar precargada
    $("#agregar-prec").on('click', function() {
        if ( $( this ).text() == "Agregar precargada")
            $( this ).text("Ocultar formulario");
        else
            $( this ).text("Agregar precargada");
    });

    function append_prod(where, id, val){

        var main;
        var divasesor;
        var divconpin;

        if (where == "add") {
            main        = "#main-productos";
            divasesor   = "div-asesor" + id;
            divconpin   = "div-conpin" + id;
            $("#numproductos_0").val( id );
        } else if (where == "update") {
            main        = "#main-productos-update";
            divasesor   = "div-asesor-update" + id;
            divconpin   = "div-conpin-update" + id;
            $("#numproductosupdate").val( id );
        } else if (where == "newbin") {
            main        = $("#main-bin-"+val).find("#main-productos")
            divasesor   = "div-asesor" + id;
            divconpin   = "div-conpin" + id;
            $("#main-bin-"+val).find("#numproductos_"+val).val( id );
        } else if (where == "newbinupdate") {
            //main        = $("#main-bin-"+val).find("#main-productos")
            main        = $("#main-bin-"+val).find("#main-productos")
            divasesor   = "div-asesor" + id;
            divconpin   = "div-conpin" + id;
            $("#main-bin-"+val).find("#numproductosupdate_"+val).val( id );
        }

        $(main).append("<div id='productosupdate"+id+"' class='control-group'>\
            <div class='controls'>\
                <input style='float: left' type='number' id='producto_"+val+"_"+id+"' name='producto_"+val+"_"+id+"' class='span1 new'>\
                    <div style='float: left;padding-left: 20px;'>\
                        <a rel='tooltip' Title='Asesor' data-original-title='Asesor'>\
                            <div id='"+divasesor+"'>\
                                <input type='checkbox' id='asesor_"+val+"_"+id+"' name='asesor_"+val+"_"+id+"' />\
                            </div>\
                        </a>\
                        <a rel='tooltip' Title='Pin' data-original-title='Pin'>\
                            <div id='"+divconpin+"'>\
                                <input type='checkbox' id='conpin_"+val+"_"+id+"' name='conpin_"+val+"_"+id+"'/>\
                            </div>\
                        </a>\
                        <a rel='tooltip' title='Audio sucursal' data-original-title='Audio sucursal'>\
                            <input type='file' id='sucursal_"+val+"_"+id+"' name='sucursal_"+val+"_"+id+"'>\
                        </a>\
                    </div>\
                </div>\
            </div>");
        
        if (where == "newbinupdate" && id != 0)
            $( "#productosupdate"+id ).children().append("<a style='float: right;' rel='tooltip' title='Quitar producto' data-original-title='Quitar producto' class='remove-product' id='"+id+"' href='#' data-toggle='modal'><button class='btn btn-mini btn-danger'><i class='icon-remove'></i></button></a>");

        $(main).find("#"+divasesor).toggleButtons({
            style: { enabled: "primary", disabled: "danger" }
        });

        $(main).find("#"+divconpin).toggleButtons({
            style: { enabled: "primary", disabled: "danger" }
        });

        $("#sucursal_"+val+"_"+id).uniform().parent().css( "margin-bottom", "20px" );

        $('input.new').each(function () {
            $(this).rules("add", {
                required: true,
                minlength: 2,
                maxlength: 2,
                min: 00,
                max: 99
            })
        });

        $("select.chzn-select").each(function () {
            $(this).rules("add", {
                required: true
            })
        });
    }

    //Boton Borrar bin
    $(".remove-bin").live("click", function() {
        var id = $(this).attr("id");
        var num = parseInt($("#numbines_update").val()) - 1;

        $("#numbines_update").val(num);
        $("#main-bin-"+id).remove();
    });

    //Boton Borrar producto
    $(".remove-product").live("click", function() {
        var id = $(this).attr("id");
        var num = parseInt($("#numproductosupdate").val()) - 1;
        //error!!!
        $("#numproductosupdate").val(num);
        $("#productosupdate"+id).remove();
    });

    //Boton Agregar bin update!
    $('#agregar-bin-update').on('click', function() {
        var main        = "#main-bin-update";
        var mainupdate  = "#numbines_update";
        var bines       = $("#bin").clone().html();
        var value       = parseInt($("#numbines_update").val()) + 1;

        agregar_bin(main, mainupdate, bines, value);
    });

    //Boton Agregar bin
    $('#agregar-bin').on('click', function() {
        var main        = "#main-bin";
        var mainupdate  = "#numbines";
        var bines       = $("#bin").clone().html();
        var value       = parseInt($("#numbines").val()) + 1;

        agregar_bin(main, mainupdate, bines, value);
    });

    function agregar_bin(main, mainupdate, bines, value)
    {
        $(mainupdate).val( value );

        $(main).append("<div id='main-bin-"+value+"'>\
                <hr>\
                <div class='control-group'>\
                    <label class='control-label'>Seleccione Bin</label>\
                    <div class='controls'>\
                        <select name='bin_"+value+"' id='bin_"+value+"' data-placeholder='Buscar bin...' class='chzn-select' class='validate[required] span2' tabindex='2'>\
                            "+bines+"</select>\
                    </div>\
                </div>\
                <div id='main-productos'>\
                    <div class='control-group'>\
                        <label class='control-label'>Productos</label>\
                        <div class='controls'>\
                            <input style='float: left' type='number' id='producto_"+value+"_0' name='producto_"+value+"_0' class='span1 new'>\
                            <div style='float: left;padding-left: 20px;'>\
                                <a rel='tooltip' data-original-title='Asesor'>\
                                    <div id='div-asesor'>\
                                        <input type='checkbox' id='asesor_"+value+"_0' name='asesor_"+value+"_0' />\
                                    </div>\
                                </a>\
                                <a rel='tooltip' data-original-title='Pin'>\
                                    <div id='div-conpin'>\
                                        <input type='checkbox' id='conpin_"+value+"_0' name='conpin_"+value+"_0' />\
                                    </div>\
                                </a>\
                                <a rel='tooltip' title='Audio sucursal' data-original-title='Audio sucursal'>\
                                    <input type='file' id='sucursal_"+value+"_0' name='sucursal_"+value+"_0'>\
                                </a>\
                            </div>\
                        </div>\
                    </div>\
                </div>\
                <input type='hidden' name='numproductos_"+value+"' id='numproductos_"+value+"' value='0' />\
                <div class='control-group'>\
                    <div class='controls'>\
                        <button id='agregar-producto-bin' value='"+value+"' class='btn btn-mini btn-metis-5' type='button'>+ Agregar mas productos</button>\
                    </div>\
                </div>\
            </div>");

        $("#main-bin-"+value).find("#div-asesor").toggleButtons({
            style: { enabled: "primary", disabled: "danger" }
        });

        $("#main-bin-"+value).find("#div-conpin").toggleButtons({
            style: { enabled: "primary", disabled: "danger" }
        });

        $("#sucursal_"+value+"_0").uniform().parent().css( "margin-bottom", "20px" );

        $('input.new').each(function () {
            $(this).rules("add", {
                required: true,
                minlength: 2,
                maxlength: 2,
                min: 00,
                max: 99
            })
        });

        $("select.chzn-select").each(function () {
            $(this).rules("add", {
                required: true
            })
        });
    }


    function agregar_bin_update(bines, value)
    {
        var main        = "#main-bin-update";
        var mainupdate  = "#numbines_update";
        var removebin   = "";

        $(mainupdate).val( value );

        if (value > 1)
            removebin   = "<a style='float: right;'' rel='tooltip' title='Quitar bin' data-original-title='Quitar bin' class='remove-bin' id='"+value+"' href='#'' data-toggle='modal'><button class='btn btn-mini btn-danger'><i class='icon-remove'></i></button></a>";

        $(main).append("<div id='main-bin-"+value+"'>\
                <hr>\
                "+removebin+"\
                <div class='control-group'>\
                    <label class='control-label'>Seleccione Bin</label>\
                    <div class='controls'>\
                        <select name='bin_"+value+"' id='bin_"+value+"' data-placeholder='Buscar bin...' class='chzn-select' class='validate[required] span2' tabindex='2'>\
                            "+bines+"</select>\
                    </div>\
                </div>\
                <div id='main-productos'>\
                </div>\
                <input type='hidden' name='numproductosupdate_"+value+"' id='numproductosupdate_"+value+"' value='0' />\
                <div class='control-group'>\
                    <div class='controls'>\
                        <button id='agregar-producto-bin-update' value='"+value+"' class='btn btn-mini btn-metis-5' type='button'>+ Agregar mas productos</button>\
                    </div>\
                </div>\
            </div>");

        $("#main-bin-"+value).find("#div-asesor").toggleButtons({
            style: { enabled: "primary", disabled: "danger" }
        });

        $("#main-bin-"+value).find("#div-conpin").toggleButtons({
            style: { enabled: "primary", disabled: "danger" }
        });
    }

    //Boton Agregar producto 'dinamico' en editar
    $(document).on('click', '#agregar-producto-bin-update', function(){
        var val = $(this).val();
        var id  = parseInt( $("#main-bin-"+val).find("#numproductosupdate_"+val).val()) + 1;
        append_prod("newbinupdate", id, val);
    });

    //Boton Agregar producto 'dinamico'
    $(document).on('click', '#agregar-producto-bin', function(){
        var val = $(this).val();
        var id  = parseInt( $("#main-bin-"+val).find("#numproductos_"+val).val()) + 1;
        append_prod("newbin", id, val);
    });

    //Boton Agregar producto
    $('#agregar-producto').on('click', function() {
        var id = parseInt($("#numproductos_0").val()) + 1;
        append_prod("add", id, 0);
    });

    //Boton Agregar producto en actualizar
    $('#agregar-producto-update').on('click', function() {
        var id = parseInt($("#numproductosupdate_0").val()) + 1;
        append_prod("update", id, 0);
    });

    //Boton confirmar
    $(".confirm").live("click", function() {
        $("#confirmprod").find("#precargada").text( $(this).attr("id") );
        $("#confirmprod").find("#piloto").val( $(this).attr("id") );
    });

    //Boton eliminar pre prod
    $(".delete-preprod").live("click", function() {
        $("#delpreprod").find("#precargada").text( $(this).attr("id") );
        $("#delpreprod").find("#piloto").val( $(this).attr("id") );
    });

    //Boton editar precargada
    $(".edit-precargada").live("click", function() {
        var j           = 0;
        var id          = $(this).attr("id");
        var voz         = $("#voz-" + id).text();
        var bin_prod    = $("#bin_prod-" + id).text(), bin_prod_arr = bin_prod.split(';'), i;
        var cardlock    = $("#cardlock-" + id).text();

        $("#precargada-title-update").text( id );
        $("#inline-validate-update").find("#piloto").val( id );
        $("#inline-validate-update").find("#nombre").val( $("#nombre-" + id).text() );
        $("#inline-validate-update").find("#fechacarga").val( $("#fechacarga-" + id).text() );
        $("#inline-validate-update").find("#"+voz).attr('selected', 'true');

        if (cardlock == 1){
            $("#inline-validate-update").find("#div-cardlock-update").children().css( "left", "0px" );
            $("#inline-validate-update").find("#cardlock").attr('checked', true);
        } else {
            $("#inline-validate-update").find("#div-cardlock-update").children().css( "left", "-50%" );
            $("#inline-validate-update").find("#cardlock").attr('checked', false);
        }

        //Remove all inside
        $("div[id*=productosupdate]").remove();
        $("#numproductosupdate").val( 0 );

        for(i in bin_prod_arr){
            var bin = bin_prod_arr[i].substring(0, 6);
            var arr = bin_prod_arr[i].split(':'), h;

            if (bin.length == 6) {

                var bines       = $("#bin").clone().html();
                var value       = parseInt($("#numbines_update").val()) + 1;
                agregar_bin_update(bines, value);

                $("#main-bin-update").find("#main-bin-"+value).find("#"+bin).attr('selected', 'true');

                for(h in arr){
                    if (bin != arr[h]){
                        var arr2 = arr[h].split('-'), g;
                        for(g in arr2){
                            if(arr2[g].length == 5){

                                var prod    = arr2[g].substring(0, 2);
                                var asesor  = arr2[g].substring(2, 3);
                                var conpin  = arr2[g].substring(3, 4);
                                //var bloqueo = arr2[g].substring(4, 5);

                                append_prod("newbinupdate", j, value);
                                $("#main-bin-"+value).find("#producto_"+value+"_"+j).val(prod);

                                if (asesor == 1){
                                    $("#main-bin-"+value).find("#div-asesor"+j).children().css( "left", "0px" );
                                    $("#main-bin-"+value).find("#asesor_"+value+"_"+j).attr('checked', true);
                                } else {
                                    $("#main-bin-"+value).find("#div-asesor"+j).children().css( "left", "-50%" );
                                    $("#main-bin-"+value).find("#asesor_"+value+"_"+j).attr('checked', false);
                                }

                                if (conpin == 1){
                                    $("#main-bin-"+value).find("#div-conpin"+j).children().css( "left", "0px" );
                                    $("#main-bin-"+value).find("#conpin_"+value+"_"+j).attr('checked', true);
                                } else {
                                    $("#main-bin-"+value).find("#div-conpin"+j).children().css( "left", "-50%" );
                                    $("#main-bin-"+value).find("#conpin_"+value+"_"+j).attr('checked', false);
                                }

                                /*if (bloqueo == 1){
                                    $("#main-bin-"+value).find("#div-bloqueo"+j).children().css( "left", "0px" );
                                    $("#main-bin-"+value).find("#bloqueo_"+value+"_"+j).attr('checked', true);
                                } else {
                                    $("#main-bin-"+value).find("#div-bloqueo"+j).children().css( "left", "-50%" );
                                    $("#main-bin-"+value).find("#bloqueo_"+value+"_"+j).attr('checked', false);
                                }*/
                                
                                j++;
                            }
                        }
                    }
                }
            }
        }
    });


    $('#div-asesor, #div-asesor-update').toggleButtons({
        style: {
            // Accepted values ["primary", "danger", "info", "success", "warning"] or nothing
            enabled: "primary",
            disabled: "danger"
        }
    });

    $('#div-conpin, #div-conpin-update').toggleButtons({
        style: {
            enabled: "primary",
            disabled: "danger"
        }
    });

    $('#div-cardlock, #div-cardlock-update').toggleButtons({
        style: {
            enabled: "primary",
            disabled: "danger"
        }
    });

    /*$(".chzn-select").chosen();
    $(".chzn-select-deselect").chosen({
        allow_single_deselect: true
    });*/


    $('#block-validate').validate({
        rules: {
            required2: "required",
            email2: {
                required: true,
                email: true
            },
            date2: {
                required: true,
                date: true
            },
            url2: {
                required: true,
                url: true
            },
            password2: {
                required: true,
                minlength: 5
            },
            confirm_password2: {
                required: true,
                minlength: 5,
                equalTo: "#password2"
            },
            agree2: "required",
            digits: {
                required: true,
                digits: true
            },
            range: {
                required: true,
                range: [5, 16]
            }
        },
        errorClass: 'help-block',
        errorElement: 'span',
        highlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error').addClass('success');
        }
    });

    /*----------- END chosen CODE -------------------------*/
    /*----------- END validate CODE -------------------------*/
}

/*--------------------------------------------------------
 END FORM-VALIDATION.HTML SCRIPTS
 ---------------------------------------------------------*/

/*--------------------------------------------------------
 END FORM-WIZARD.HTML SCRIPTS
 ---------------------------------------------------------*/
function AddUsuario() {
    $('#add-usuario-form').validate({
        rules: {
            required: "required",
            usuario: {
                required: true,
                minlength: 4,
                maxlength: 20
            },
            nombre: {
                required: true,
                minlength: 6,
                maxlength: 20
            },
            rol: {
                required: true
            },
            clave: {
                required: true,
                minlength: 5
            },
            claveconfirm: {
                required: true,
                minlength: 5,
                equalTo: "#clave"
            }
        },

        errorClass: 'help-inline',
        errorElement: 'span',
        highlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error').addClass('success');
        }
    });

    $('#edit-usuario-form').validate({
        rules: {
            required: "required",
            usuario: {
                required: true,
                minlength: 4,
                maxlength: 20
            },
            nombre: {
                required: true,
                minlength: 6,
                maxlength: 20
            },
            rol: {
                required: true
            },
            clave: {
                required: true,
                minlength: 5
            },
            claveconfirm: {
                required: true,
                minlength: 5
                //equalTo: "#clave"
            }
        },

        errorClass: 'help-inline',
        errorElement: 'span',
        highlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error').addClass('success');
        }
    });

    //Boton eliminar usuario
    $(".delete-usuario").live("click", function() {
        $("#delete-usuario").find("#nameusuario").text( $(this).attr("id") );
        $("#delete-usuario").find("#usuario").val( $(this).attr("id") );
    });

    //Boton expirar clave de usuario
    $(".expire-usuario").live("click", function() {
        $("#expire-usuario").find("#nameusuario").text( $(this).attr("id") );
        $("#expire-usuario").find("#usuario").val( $(this).attr("id") );
    });

    //Boton editar usuario
    $(".edit-usuario").live("click", function() {
        var id  = $(this).attr("id");
        var rol = $("#rol-" + id).text();

        //Remove all inside edit
        $("#edit-usuario-clave").empty();

        $("#edit-usuario").find("#usuario").val( id );
        $("#edit-usuario").find("#nombre").val( $("#nombre-" + id).text() );
        $("#edit-usuario").find("#"+rol).attr('selected', 'true');        
    });

    //Boton editar clave
    $("#edit-usuario-clave-button").live("click", function() {
        //Append all stufs
        if ( $('#edit-usuario-clave').children().length == 0 ) {
            //Clave
            $('#edit-usuario-clave').append("<div class='control-group'><label class='control-label'>Clave</label><div class='controls'><div class='input-prepend'><span class='add-on'><i class='icon-lock'></i></span></div><input style='margin-left: -4px;' type='password' id='clave' name='clave' placeholder='Clave nueva'></div></div>");
            //Confirm clave
            $('#edit-usuario-clave').append("<div class='control-group'><label class='control-label'>Confirmar clave</label><div class='controls'><div class='input-prepend'><span class='add-on'><i class='icon-lock'></i></span></div><input style='margin-left: -4px;' type='password' id='claveconfirm' name='claveconfirm' placeholder='Confirmar clave nueva'></div></div>");
        }
        /*<div class='control-group'>
            <label class='control-label'>Clave</label>
            <div class='controls'>
                <div class='input-prepend'>
                    <span class='add-on'><i class='icon-lock'></i></span>
                </div>
                <input style='margin-left: -4px;' type='password' id='clave' name='clave' placeholder='Clave nueva'>
            </div>
        </div>
        <div class='control-group'>
            <label class='control-label'>Confirmar clave</label>
            <div class='controls'>
                <div class='input-prepend'>
                    <span class='add-on'><i class='icon-lock'></i></span>
                </div>
                <input style='margin-left: -4px;' type='password' id='claveconfirm' name='claveconfirm' placeholder='Confirmar clave nueva'>
            </div>
        </div>*/

        //Remove button?
    });

}

 function UsuariosTable() {

    /*----------- BEGIN datatable CODE -------------------------*/
    $('#dataTable').dataTable({
        "sDom": "<'pull-right'l>t<'row-fluid'<'span6'f><'span6'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "Mostrar: _MENU_",
            "sSearch": "Buscar: ",
            "sZeroRecords": "No se encontraron registros",
            "oPaginate": {
                "sPrevious": "Anterior",
                "sNext": "Siguiente"
            }
        }
    });
    /*----------- END datatable CODE -------------------------*/

    /*----------- BEGIN action table CODE -------------------------*/
    $('#actionTable button.remove').on('click', function() {
        $(this).closest('tr').remove();
    });
    $('#actionTable button.edit').on('click', function() {
        $('#editModal').modal({
            show: true
        });
        var val1 = $(this).closest('tr').children('td').eq(1),
                val2 = $(this).closest('tr').children('td').eq(2),
                val3 = $(this).closest('tr').children('td').eq(3);
        $('#editModal #fName').val(val1.html());
        $('#editModal #lName').val(val2.html());
        $('#editModal #uName').val(val3.html());


        $('#editModal #sbmtBtn').on('click', function() {
            val1.html($('#editModal #fName').val());
            val2.html($('#editModal #lName').val());
            val3.html($('#editModal #uName').val());
        });

    });
    /*----------- END action table CODE -------------------------*/
}
/*--------------------------------------------------------
 END TABLES.HTML SCRIPTS
 ---------------------------------------------------------*/

/*--------------------------------------------------------
 BEGIN TABLES.HTML SCRIPTS
 ---------------------------------------------------------*/
function PrecargadaTable() {

    /*----------- BEGIN datatable CODE -------------------------*/
    $('#dataTable').dataTable({
        "sDom": "<'pull-right'l>t<'row-fluid'<'span6'f><'span6'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "Mostrar: _MENU_",
            "sSearch": "Buscar: ",
            "sZeroRecords": "No se encontraron registros",
            "oPaginate": {
                "sPrevious": "Anterior",
                "sNext": "Siguiente"
            }
        }
    });
    /*----------- END datatable CODE -------------------------*/


    /*----------- BEGIN datatable CODE -------------------------*/
    $('#dataTable2').dataTable({
        "sDom": "<'pull-right'l>t<'row-fluid'<'span6'f><'span6'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "Mostrar: _MENU_",
            "sSearch": "Buscar: ",
            "sZeroRecords": "No se encontraron registros",
            "oPaginate": {
                "sPrevious": "Anterior",
                "sNext": "Siguiente"
            }
        }
    });
    /*----------- END datatable CODE -------------------------*/

    /*----------- BEGIN action table CODE -------------------------*/
    $('#actionTable button.remove').on('click', function() {
        $(this).closest('tr').remove();
    });
    $('#actionTable button.edit').on('click', function() {
        $('#editModal').modal({
            show: true
        });
    });
    /*----------- END action table CODE -------------------------*/

}
/*--------------------------------------------------------
 END TABLES.HTML SCRIPTS
 ---------------------------------------------------------*/

 //bines
 function Bines ()
 {

    //Boton eliminar bines
    $('.delete-bin').on('click', function() {
        $("#delbin").find("#servtext").text( $(this).attr("val") );
        $("#delbin").find("#bintext").text( $(this).attr("id") );
        $("#delbin").find("#serv").val( $(this).attr("val") );
        $("#delbin").find("#bin").val( $(this).attr("id") );
    });

    $('#add-bin-precargada-form').validate({
        rules: {
            required: "required",
            bin: {
                required: true,
                minlength: 6,
                maxlength: 6,
                min: 604200,
                max: 604299
            }
        },

        errorClass: 'help-inline',
        errorElement: 'span',
        highlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error').addClass('success');
        }
    });

    $('#add-bin-creditos-form').validate({
        rules: {
            required: "required",
            bin: {
                required: true,
                minlength: 6,
                maxlength: 6,
                min: 589600,
                max: 589699
            }
        },

        errorClass: 'help-inline',
        errorElement: 'span',
        highlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error').addClass('success');
        }
    });


    $('#add-bin-autorizaciones-form').validate({
        rules: {
            required: "required",
            bin: {
                required: true,
                minlength: 6,
                maxlength: 6,
                min: 000000,
                max: 000001
            }
        },

        errorClass: 'help-inline',
        errorElement: 'span',
        highlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error').addClass('success');
        }
    });
 }

//file
 function File ()
 {

    $('#audiopre').uniform();

    //Boton eliminar audio
    $('.delete-audiofile').on('click', function() {
        $("#delfile").find("#audiofile").text( $(this).attr("val") );
        $("#delfile").find("#file").val( $(this).attr("file") );
        $("#delfile").find("#piloto").val( $(this).attr("id") );
    });

    //Boton editar audio
    $('.edit-audiofile').on('click', function() {
        //$("#uploadfile").find("#audiofile").text( $(this).attr("val") );
        $("#uploadfile").find("#file").val( $(this).attr("file") );
        $("#uploadfile").find("#piloto").val( $(this).attr("id") );
    });


     $('#uploadfile-validate').validate({
        rules: {
            required: "required",
            audio: {
                required: true,
                accept: "audio/*"
            }
        },

        errorClass: 'help-inline',
        errorElement: 'span',
        highlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('success').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parents('.control-group').removeClass('error').addClass('success');
        }
    });
 }


function IndexHandleSock ()
{
    try {
        //Connect
        var socket = io.connect('http://'+conf["socket_server"]+':'+conf["socket_port"]);
        var date   = new Date();

        socket.on("index", function(data) {
            $("#ica-logs-error").text(data["ica:logs:error"]);
            $("#ica-logs-calls").text(data["ica:logs:calls"]);
            $("#ica-logs-warning").text(data["ica:logs:warning"]);
            $("#ica-logs-serv-jpos").text(data["ica:logs:serv:jpos"]);
        });

        socket.on("index-graph", function(recv) {
            function UpdateGraph(series) {
                plot.setData([series]);
                plot.setupGrid();
                plot.draw();
            }

            $.ajax({
                url: "/api/v1/calls/week_graph",
                type: "GET",
                dataType: "json",
                success: UpdateGraph
            });
            var id  = date.getDate()+""+(date.getMonth()+1)+""+date.getFullYear();
            var val = parseInt($("#"+id).text());
            
            $("#"+id).text( val + 1 )
        });

        //Admin control
        socket.on("admin", function(data) {
            admin(data["action"], data['text']);
        });

        //Send channel we want
        socket.emit("channel", "index");
        socket.emit("channel", "index-graph");
    } catch(err) {
        if ( conf["debug"] == true )
            alert(err)
    }
}

function CurrentCallsHandleSock ()
{
    try {
        //Connect
        var socket = io.connect('http://'+conf["socket_server"]+':'+conf["socket_port"]);

        socket.on("currentcalls", function(data) {
            //Remove call on 'hangup' event
            if (data['extension'] == "h")
                del_call(data['channel']);
            else
                add_call(data);
        });

        //Actualiza los porcentajes
        socket.on("currentcalls-percent", function(data) {
            set_percentcalls();
        });

        //Admin control
        socket.on("admin", function(data) {
            admin(data["action"], data['text']);
        });

        //Send channel we want
        socket.emit("channel", "currentcalls");
        socket.emit("channel", "currentcalls-percent");
    } catch(err) {
        if ( conf["debug"] == true )
            alert(err)
    }
}

function add_call(data)
{
    var numcalls    = parseInt($( "#numcalls" ).text());
    var uid         = data['uid'].split(".");
    var serv;

    if (data['serv'] != null)
        serv = data['serv']+" ("+data['dnid']+")";
    else
        serv = "no serv ("+data['dnid']+")";

    $("#calls-body").prepend("<tr id='"+data['channel']+"'><td>"+data['callerid']+"</td><td>"+data['callername']+"</td><td>"+serv+"</td><td id='counter' unix='"+uid[0]+"'>00:00:01</td></tr>");
    set_call(numcalls, "more");
    
    var call = $(document.getElementById(data['channel']));
    set_count(call, uid[0]);
}

function del_call(id)
{
    var numcalls    = parseInt($( "#numcalls" ).text());
    var elem        = $(document.getElementById(id));

    if (elem.length)
        elem.remove(elem.selectedIndex, set_call(numcalls, "less"));
}

function set_call(numcalls, action)
{
    if (action == "less") {
        calls = numcalls - 1;
        if (calls == 0 && $("#nocalls").length == 0)
            $("#calls-body").prepend("<tr id='nocalls'><td colspan='4'>No hay llamadas en este momento</td></tr>");

    } else if (action == "more") {
        calls = numcalls + 1;
        if (calls > 0 && $("#nocalls").length > 0)
            $("#nocalls").remove();
    }

    $("#numcalls").text( calls );
    var percentcalls = get_percentcalls( calls );
    set_percent( percentcalls );
}

function get_percentcalls (calls)
{
    var percent;
    var channels = parseInt( pstn["trunks"] ) * 30;

    percent = ( (calls * 100 / channels).toFixed(1) ) * 1;//1 decimal en caso de ser necesario
    //percent = (calls * 100 / channels).toFixed(0);//ningun decimal

    return percent;
}

function set_percentarray ()
{
    jQuery.ajaxSetup( { async: false } );
    $.ajax({
        type: 'GET',
        url: '/api/v1/conf/trunks',
        dataType:'json',
        success: function (data) {
            pstn["trunks"]  = data["trunks"];
            pstn["servers"] = data["servers"];
        }
    });
    jQuery.ajaxSetup( { async: true } );
}

function set_percentcalls ()
{
    set_percentarray();
    var calls = parseInt($("#numcalls").text());
    var percentcalls = get_percentcalls( calls );
    set_percent( percentcalls );
}

function set_percent(percentcalls)
{
    if (pstn["trunks"] == 0)
        percentcalls = 100;

    if (percentcalls >= 90) {
        $("#percenttype").removeClass("progress-success");
        $("#percenttype").removeClass("progress-warning");
        $("#percenttype").addClass("progress-danger");
    } else if (percentcalls >= 75 && percentcalls < 90) {
        $("#percenttype").removeClass("progress-success");
        $("#percenttype").removeClass("progress-danger");
        $("#percenttype").addClass("progress-warning");
    } else if (percentcalls < 75) {
        $("#percenttype").removeClass("progress-warning");
        $("#percenttype").removeClass("progress-danger");
        $("#percenttype").addClass("progress-success");
    }

    $("#percentcallstxt").text( percentcalls )
    $("#percentcalls").css( "width", percentcalls +"%" );
}

function set_count (call, unix)
{
    setInterval(function(count) {
            var now  = Math.round((new Date()).getTime() / 1000);
            var secs = Math.abs(now-unix);
            call.find("#counter").text(secs.toHHMMSS());
        }, 1000
    );
}

function CounterAllTable ()
{
    $('#calls >tbody >tr').each(function(index, elem) {
        var call = $(document.getElementById(elem.id));
        var unix = parseInt( call.find("#counter").attr( "unix" ) );
        set_count(call, unix);
    });
}

//Opciones de administrador
function admin (action, text)
{
    if (action == "reload")
        location.reload();
    else if (action == "alert")
        alert(text);
    else if (action == "redirect")
        window.location.assign(text);
}

function init_calls ()
{
    jQuery.ajaxSetup( { async: false } );
    $.ajax({
        url: "/api/v1/calls/currentcalls",
        type: "GET",
        dataType: "json",
        success: function (data) {
            $('#calls >tbody >tr').each(function(index, elem) {
                var flag = 0;
                for ( var i = 0; i < data['data'].length; i++ )
                {
                    if (elem.id == data['data'][i]['channel']) {
                        flag = 1;
                        break;
                    }
                }

                //Remove extra call!!
                if (flag == 0 && elem.id != "nocalls") {
                    var element = $(document.getElementById(elem.id));
                    element.remove(element.selectedIndex);
                    //console.log("borrar: "+ elem.id);
                }
            });
        }
    });
    CurrentCallsHandleSock();
    jQuery.ajaxSetup( { async: true } );

    set_percentcalls();
    CounterAllTable();
}

function get_conf ()
{
    jQuery.ajaxSetup( { async: false } );
    $.ajax({
        type: 'GET',
        url: '/api/v1/conf/basic',
        dataType:'json',
        success: function (mainconf) {
            conf["socket_server"]   = mainconf["socket_server"];
            conf["socket_port"]     = mainconf["socket_port"];
            conf["domain"]          = mainconf["domain"];
            conf["debug"]           = mainconf["debug"];
        }
    });
    jQuery.ajaxSetup( { async: true } );
}
