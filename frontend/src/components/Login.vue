<template>
<div class="container">
    <div class="main">
        <div class="title">VulNotes</div>
        <div class="description">这是个漏洞记录平台</div>
        <div class="group">
            <input class="ipt" type="text" placeholder="用户名">
            <input class="ipt" type="password" placeholder="密码">
        </div>
        <button class="btn" v-on:click="login">登录</button>
        <div class="error_description"> {{ error_msg }} </div>
    </div>
</div>
</template>

<script>
import { getLogin } from '../vuex/actions'

export default {
  vuex: {
    actions: {
      getLogin
    }
  },
  data () {
    return {
      error_msg: ''
    }
  },
  methods: {
    login () {
      var that = this
      that.error_msg = ''
      this.getLogin().then((resp) => {
        that.$route.router.go('/')
      }, (resp) => {
        that.error_msg = 'Login Error'
      })
    }
  }
}
</script>

<style scoped>
body,
h1,
h2,
h3,
h4,
h5,
h6,
p,
dl,
dt,
dd,
ul,
ol,
li,
form,
button,
input,
textarea,
th,
td,
button {
    margin: 0;
    padding: 0;
    outline: none;
}
body {
    background-color: #f7fafc;
    font-family: "Microsoft Yahei", Helvetica, Arial, sans-serif;
    font-size: 14px;
    color: #555;
    font-weight: 500;
}
li {
    list-style-type: none;
}
input,
select,
textarea,
label,
button {
    vertical-align: middle;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    font-size: 13px;
    font-family: "Microsoft Yahei", Helvetica, Arial, sans-serif;
}
.container {
    margin: 0 auto;
    min-width: 800px;
}
.main {
    position: absolute;
    top: 50%;
    left: 50%;
    margin-top: -200px;
    margin-left: -150px;
    width: 300px;
    text-align: center;
}
.title {
    padding: 10px 0;
    font-size: 60px;
    color: #0f88eb;
    letter-spacing: 5px;
}
.description {
    padding: 10px 0 30px 0;
    font-size: 18px;
}
.error_description{
    padding: 10px 0 30px 0;
    font-size: 20px;
    font-family: "Microsoft Yahei", Helvetica, Arial, sans-serif;
}
.group {
    border: 1px solid #d5d5d5;
    border-radius: 3px;
    background: #fff;
}
.ipt {
    width: 298px;
    height: 46px;
    line-height: 46px;
    padding: 10px;
    border: 0;
    border-radius: 3px;
    background: #fff;
}
.group .ipt:last-child {
    border-radius: 0 0 3px 3px;
    border-top: 1px solid #e8e8e8;
}
.btn {
    margin-top: 20px;
    width: 300px;
    height: 40px;
    line-height: 40px;
    color: #fff;
    background-color: #0f88eb;
    border: 0;
    border-radius: 3px;
    cursor: pointer;
}
.btn:hover {
    background-color: #55abed;
}
</style>
