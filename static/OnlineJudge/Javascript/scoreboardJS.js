/**
 * 目标页面：scoreboard.html
 * 功能：1.获取当前网络时间
 *      2.5s执行一次ajax，刷新榜单
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
