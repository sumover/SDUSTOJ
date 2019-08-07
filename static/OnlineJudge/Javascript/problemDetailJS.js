/**
 * author: Shixuan Liu
 * 功能: 1.显示当前网络时间、比赛开始时间、结束时间
 *      2.点击提交按钮时候展示提交模态框
 */
let timeSpan = document.querySelector('#timeSpan');
let dateSpan = document.querySelector('#dateSpan');

//获取当前网络时间，并显示在网页
function changeTime()
{
  let dateDate = new Date();
  let localeDateString = dateDate.toLocaleDateString();
  let localeTimeString = dateDate.toLocaleTimeString('chinese', {hour12: false});
  dateSpanItem.textContent = '当前日期：' + localeDateString;
  timeSpanItem.textContent = '当前时间：' + localeTimeString;
}