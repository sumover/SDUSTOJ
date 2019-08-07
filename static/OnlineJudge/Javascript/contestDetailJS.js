/**
 * author:Shixuan Liu
 * 目标页面：contestDetail.html
 * 功能：1.获取当前网络时间
 *      2.从contestDetail.html的隐藏标签获取状态码:如果状态码为-1，那么一直向后台请求状态码;如果结果为0那么刷新页面，显示题目
 */
let timeSpanItem = document.querySelector('#timeSpan');
let dateSpanItem = document.querySelector('#dateSpan');
let statusCodeLabelItem = document.querySelector('#statusCodeLabel');

//获取当前网络时间，并显示在网页
function changeTime()
{
  let dateDate = new Date();
  let localeDateString = dateDate.toLocaleDateString();
  let localeTimeString = dateDate.toLocaleTimeString('chinese', {hour12: false});
  dateSpanItem.textContent = '当前日期：' + localeDateString;
  timeSpanItem.textContent = '当前时间：' + localeTimeString;
}

//从id = statusCodeLabel的标签获取状态码并返回
function getStatusCode()
{
  return statusCodeLabelItem.textContent;
}

//检查状态码
function checkStatusCode()
{
  let statusCodeString = getStatusCode();
  if(statusCodeString === '0')
  {
    //在每次进入这个页面的时候，都会绕过浏览器缓存，重新向服务器获取数据。
    if(location.href.indexOf('#reloaded') === -1)
    {
      location.href = location.href + '#reloaded';
      location.reload();
    }
  }
  else if(statusCodeString === '-1')
  {
    $.ajax({
      //提交的URL
      url: '',
      //POST形式提交
      type: 'POST',
      //返回数据的格式
      dataType: 'text',
      //成功之后
      success: function(responseStatusCodeString)
      {
        //将字符串转化为JSON
        responseStatusCodeJSON = JSON.parse(responseStatusCodeString);
        //TODO 访问JSON参数
        responseStatusCode = responseStatusCodeJSON.constructor;
        //更新隐藏label
        statusCodeLabelItem.textContent = responseStatusCodeString;
      }
    })
  }
}

/*TODO 1.获取当前网络时间*/
//500ms执行一次changeTime
setInterval(changeTime, 500);

/*TODO 2.从contestDetail.html的隐藏标签获取状态码，并且进行相应操作*/
setInterval(checkStatusCode, 1000);
