/**

 @Name: 忘记密码模块

 */
 
layui.define(['laypage', 'fly', 'element', 'flow'], function(exports){

  var $ = layui.jquery;
  var layer = layui.layer;
  var util = layui.util;
  var laytpl = layui.laytpl;
  var form = layui.form;
  var laypage = layui.laypage;
  var fly = layui.fly;
  var countdown = 60;


  var set_time = function (val){
    if (countdown === 0) {
        val.removeClass("layui-btn-disabled");
        val.attr("disabled", false);
        val.text("获取验证码");
        countdown = 60;
        return false;
    } else {
        val.addClass("layui-btn-disabled");
        val.attr("disabled", true);
        val.text("(" + countdown + ")秒后重新发送");
        countdown--;
    }
    setTimeout(function() {
        set_time(val);
    },1000);
  };


  $('#vercodesend').on('click', function(){
      var phone = $("#L_phone").val();
      var loginname = $("#L_loginname").val();
        if (phone === "") {
            layer.msg("手机号未填写");
            return false;
        }
        if (loginname === "") {
            layer.msg("用户名未填写");
            return false;
        }
        fly.json('/user/sms?sms_type=2&phone=' + phone + '&loginname=' + loginname,
            {}, function(res){
          if(res.status === 0){
              set_time($('#vercodesend'));
              layer.msg(res.msg);
          }
        }, {
          "type": "get"
        });
      });

  exports('register', {});
  
});