/**
 * 目标页面：selfStatus.html
 * 功能：1.获取当前网络时间
 *      2.1s执行一次ajax，获取判题状态
 * @type {Element}
 */

let timeSpan = document.querySelector('#timeSpan');
let dateSpan = document.querySelector('#dateSpan');

//获取当前网络时间，并显示在网页
function changeTime()
{
  let date = new Date();
  let localeDateString = date.toLocaleDateString();
  let localeTimeString = date.toLocaleTimeString('chinese', {hour12: false});
  dateSpan.textContent = '当前日期：' + localeDateString;
  timeSpan.textContent = '当前时间：' + localeTimeString;
}
