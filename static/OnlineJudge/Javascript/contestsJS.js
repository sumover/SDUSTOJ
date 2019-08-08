/**
 * 目标页面：contests.html
 * 功能：1.获取当前网络时间
 *      2.将beginTime与endTime由时间戳转化为当前日期时间
 *      3.将状态码化为文字状态
 */
let timeSpan = document.querySelector('#timeSpan');
let dateSpan = document.querySelector('#dateSpan');
let beginTimeTds = document.querySelectorAll('.beginTimeTd');
let endTimeTds = document.querySelectorAll('.endTimeTd');
let statusTds = document.querySelectorAll('.statusTd');

//获取当前网络时间，并显示在网页
function changeTime()
{
  let date = new Date();
  let localeDateString = date.toLocaleDateString();
  let localeTimeString = date.toLocaleTimeString('chinese', {hour12: false});
  dateSpan.textContent = '当前日期：' + localeDateString;
  timeSpan.textContent = '当前时间：' + localeTimeString;
}

//将时间戳转化为当前日期时间
function timestampToTimeString(timestamp)
{
  let timestampFloat = parseFloat(timestamp);
  timestampFloat = timestampFloat * 1000;
  let date = new Date(timestampFloat);
  return date.toLocaleString('zh', {hour12:false});
}

//将状态码以字符串形式传进来，并处理
function statusCodeTostatusWords(statusCode)
{
  let statusString = '无状态信息';
  if(statusCode === '-1')
    statusString = '未开始';
  else if(statusCode === '0')
    statusString = '正在进行';
  else if(statusCode === '1')
    statusString = '已结束';
  return statusString;
}

//将组件列表进行对应的函数处理
function itemDeal(itemList, fun)
{
  for(let i = 0; i < itemList.length; ++i)
    itemList[i].textContent = fun(itemList[i].textContent);
}

/*TODO: 1.获取当前网络时间*/
//500ms执行一次changeTime
setInterval(changeTime, 500);

/*TODO 2.将beginTime与endTime由时间戳转化为当前日期时间*/
//将beginTime和endTime转化为时间字符串
itemDeal(beginTimeTds, timestampToTimeString);
itemDeal(endTimeTds, timestampToTimeString);

/*TODO 3.将状态码化为文字状态*/
itemDeal(statusTds, statusCodeTostatusWords);