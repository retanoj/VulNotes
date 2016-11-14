<template>
  <div id="box">
    <button type="button" class="btn btn-success btn-lg" v-on:click="login">登录</button>
    <div> {{ error_msg }} </div>
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

<style>
#box {
  left: 50%;
  top: 50%;
  margin-left: -50px;
  margin-top: -50px;
  width: 100px;
  height: 50px;
  position: absolute;
}
</style>
