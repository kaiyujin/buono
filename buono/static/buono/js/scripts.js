var minLengthMessage = '文字以上のコメントをください！'
$("#addComentButton").click(function() {
    var length = $('#ct').val().length;
    if(length < 30) {
	$('#myModalLabel3').text('30'+minLengthMessage)
	$('#myModalLabel3').css('color','red');
	return;
    }
    $('#myModalLabel3').text('&nbsp;')
    $('#myModalLabel3').css('color','');
    $('#addComentForm').submit();
});
$("#addBuonoButton").click(function() {
    var length = $('#bct').val().length;
    if(length < 100) {
	$('#myModalLabel1').text('100'+minLengthMessage)
	$('#myModalLabel1').css('color','red');
	return;
    }
    $('#myModalLabel1').text('&nbsp;')
    $('#myModalLabel1').css('color','');
    $('#addBuonoForm').submit();
});
$("#addSemiBuonoButton").click(function() {
    var length = $('#sbct').val().length;
    if(length < 100) {
	$('#myModalLabel2').text('100'+minLengthMessage)
	$('#myModalLabel2').css('color','red');
	return;
    }
    $('#myModalLabel2').text('&nbsp;')
    $('#myModalLabel2').css('color','');
    $('#addSemiBuonoForm').submit();
});
$("#createBuonoButton").click(function() {
    $('#createBuonoForm').submit();
});
