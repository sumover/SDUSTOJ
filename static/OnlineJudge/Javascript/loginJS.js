//定义username长度为学号长度
function checkUsername(usernameString)
{
  for(let i = 0; i < usernameString.length; ++i)
  {
    if(isNaN(parseInt(usernameString.charAt(i))))
      return '用户名中含有非数字字符，请重新输入';
  }
  return null;
}

// 验证账号是否正确填写
$('form').submit(function(event)
{
  let usernameString = $('#username').val().toString();
  let resultString = checkUsername(usernameString);
  if(resultString)
  {
    event.preventDefault();
    alert(resultString);
    let firstFormGroupDiv = $('.form-group').eq(0);
    firstFormGroupDiv.addClass('has-error');
    $('#username')[0].focus();
  }
});