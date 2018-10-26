/**

 @Name: 兑换模块

 */
 
layui.define(['laypage', 'fly', 'element', 'flow'], function(exports){

  var $ = layui.jquery;
  var layer = layui.layer;
  var util = layui.util;
  var laytpl = layui.laytpl;
  var form = layui.form;
  var laypage = layui.laypage;
  var fly = layui.fly;

  $('#exchange').on('click', function(){
      var product_code = $("#div_detail").data("code");
    fly.json('/prod/order', {
        "product_code": product_code
    }, function(res){
      if(res.status === 0){
          layer.msg(res.msg);
      }
    }, {});
  });

  exports('exchange', {});
  
});