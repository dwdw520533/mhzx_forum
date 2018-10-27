/**

 @Name: 兑换模块

 */
 
layui.use(['laypage', 'fly', 'element', 'flow', 'form'], function(){

  var $ = layui.jquery;
  var layer = layui.layer;
  var util = layui.util;
  var laytpl = layui.laytpl;
  var form = layui.form;
  var laypage = layui.laypage;
  var fly = layui.fly;

  $('#exchange').on('click', function(){
      layer.confirm('您确认购买该商品？', function(index){
        layer.close(index);
        var product_code = $("#div_detail").data("code");
        fly.json('/prod/order', {
                "product_code": product_code
            }, function(res){
              if(res.status === 0){
                  layer.alert("购买成功，请前往已购商品查看订单信息");
              }
            }, {});
          });
      });


  $('#query_role').on('click', function(){
      var zone_id = $("#L_zone_id").val();
      var login_name = $("#L_login_name").val();
      if (login_name === "") {
            layer.msg("请输入用户名");
            return false;
        }
    fly.json('/api/roles', {
        "zone_id": zone_id,
        "login_name": login_name
    }, function(res){
      if(res.status === 0) {
          var html = "";
          if (res.data.length === 0) {
              html = "<option value=''>暂无数据</option>";
          }
          else {
              $.each(res.data, function (index, item) {
                  html += "<option value='" + item.role_id + "'>"+item.role_name+"</option>";
              })
          }
          $("#L_role_id").html(html);
          form.render("select");
      }
    }, {});
  });
});