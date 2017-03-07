<template>
  <div class="item form-horizontal">

    <div class="form-group" required>
      <label for="vul_name" class="col-md-2 control-label">漏洞名称:</label>
      <div id="vul_name" class="col-md-6">
        <input type="text" class="form-control" v-model="record.vul_name"></input>
      </div>
    </div>

    <div class="form-group">
      <label for="vul_company" class="col-md-2 control-label">业务线:</label>
      <div id="vul_company" class="col-md-2">
        <input type="text" class="form-control" v-model="record.vul_company"></input>
      </div>
    </div>

    <div class="form-group">
      <label for="vul_type" class="col-md-2 control-label">漏洞类型:</label>
      <div id="vul_type" class="col-md-2">
        <select class="form-control" v-model="record.vul_type_id">
          <option v-for="option in VulTypeList | orderBy 'id'" value="{{ option.id }}">{{ option.vul_type }}</option>
        </select>


      </div>
    </div>

    <div class="form-group">
      <label for="vul_level" class="col-md-2 control-label">等级:</label>
      <div id="vul_level" class="col-md-2">
        <button-group :value.sync="record.vul_level" type="primary">
          <radio value="low">低</radio>
          <radio value="medium">中</radio>
          <radio value="high">高</radio>
        </button-group>
      </div>
    </div>

    <div class="form-group">
      <label for="vul_status" class="col-md-2 control-label">状态:</label>
      <div id="vul_status" class="col-md-2">
        <button v-if="record.vul_status == 'unresolved'" class="btn btn-danger" v-on:click="changeStatus('resolved')">未解决</button>
        <button v-else class="btn btn-success" v-on:click="changeStatus('unresolved')">已解决</button>
      </div>
    </div>

    <div class="form-group">
      <label for="vul_find_date" class="col-md-2 control-label" >发现时间:</label>
      <div id="vul_find_date" class="col-md-3">
        <input type="text" class="form-control" :value="record.vul_find_date | formatDate" id="dtp_find"></input>
      </div>

      <label for="vul_solve_date" class="col-md-2 control-label" >解决时间:</label>
      <div id="vul_solve_date" class="col-md-3">
        <input type="text" class="form-control" :value="record.vul_solve_date | formatDate" id="dtp_solve"></input>
      </div>
    </div>

    <div class="form-group">
      <label for="vul_detail" class="col-md-2 control-label">细节:</label>
      <div id="vul_detail" class="col-md-8">
        <div id="editor"></div>
      </div>
    </div>

    <div class="form-group">
      <div class="col-md-2 col-md-offset-8 control-label">
        <button class="btn btn-primary btn-lg" v-on:click="applyEdit">apply</button>
      </div>
    </div>
  </div>
</template>

<script>
import { select } from 'vue-strap'
import { radio } from 'vue-strap'
import { buttonGroup } from 'vue-strap'

import { getVulRecord, updateRecord, insertRecord } from '../vuex/actions'
import { formatDate } from '../filters'
import * as config from '../config'

export default {
  props: ['edit_id'],
  components: {
    radio,
    'button-group': buttonGroup,
    'v-select': select,
  },
  vuex: {
    getters : {
      VulTypeList: ({ VulType }) => VulType.VulTypeList
    },
    actions : {
      getVulRecord, updateRecord, insertRecord
    }
  },
  data () {
    return {
      record: {
        'id': null,
        'vul_type_id': null,
        'vul_name': null,
        'vul_level': null,
        'vul_status': null,
        'vul_company': null,
        'vul_detail': null,
        'vul_find_date': null,
        'vul_solve_date': null
      }
    }
  },
  ready () {
    var vm = this

    // init datetimepicker /* {{{ */
    var dtp_format = {
      format: 'yyyy-mm-dd',
      autoclose: 'true',
      minView: 2, // month view
      todayBtn: 'linked',
      todayHighlight: 'true',
      language: 'zh-CN',
      pickerReferer: 'input'
    }

    $('#dtp_find')
    .datetimepicker(dtp_format)
    .on('changeDate', function(ev){
      vm.record.vul_find_date = formatDate(ev.date)
    })

    $('#dtp_solve')
    .datetimepicker(dtp_format)
    .on('changeDate', function(ev){
      vm.record.vul_solve_date = formatDate(ev.date)
    })
    /* }}} */

    // init summernote /* {{{ */
    $('#editor').summernote({
      height: 250,
      fontNames: ['Arial', 'Arial Black', 'Comic Sans MS', 'Courier New'],
      toolbar: [
        ['style', ['bold', 'italic', 'underline', 'clear']],

        ['fontsize', ['fontname', 'fontsize']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['insert', ['picture', 'link', 'table', 'hr']],
        ['misc', ['fullscreen', 'undo']]
      ],
      dialogsInBody: true,
      popover: {},
      callbacks: {
        onImageUpload: function(files, editor, welEditable) {
          var file = files[0]
          var formData = new FormData()
          formData.append("file", file)
          $.ajax({
              url: config.UPLOAD_API +'/' +file.name,
              data: formData,
              dataType: 'json',
              cache: false,
              contentType: false,
              processData: false,
              type: 'POST',
              success: function (data) {
                  var img_path = data.data
                  $('#editor').summernote('insertImage', config.HOST +img_path, img_path)
              }
          })
        }
      }
    })

    /* }}} */

    // 生成空record，或填充 /* {{{ */
    if (vm.edit_id != -1){
      vm.getVulRecord(vm.edit_id).then(function(resp){
        var record = resp.json().data
        vm.record = record
        $('#editor').summernote('code', vm.record.vul_detail)
      }).catch(function(error){
        console.log(error)
      })
    } else {
      vm.record.vul_type_id = 1
      vm.record.vul_status  = 'unresolved'
      vm.record.vul_level   = 'low'
      vm.record.vul_find_date = formatDate(new Date())
    }
    /* }}} */
  },
  methods: {
    // 提交逻辑
    applyEdit () {
      var vm = this
      // 富文本回填“细节”
      this.record.vul_detail = $('#editor').summernote('code')
      this.record.vul_find_date = formatDate(this.record.vul_find_date)
      this.record.vul_solve_date = formatDate(this.record.vul_solve_date)

      if (this.checkFormValidate()){
        if (this.record.id == null) {
          // 插入操作
          this.insertRecord(this.record).then(function(resp){
            vm.$dispatch('item_done')
          }).catch(function(err_resp){
            console.log(err_resp)
          })
        } else {
          // 更新操作
          this.updateRecord(this.record.id, this.record).then(function(resp){
            vm.$dispatch('item_done')
          }).catch(function(err_resp){
            console.log(err_resp)
          })
        }
      }
    },

    // 漏洞状态改变
    changeStatus (status) {
      this.record.vul_status = status
    },

    // Form合法性检查
    checkFormValidate () {
      var isValid = true
      if ( !this.record.vul_name ) {
        isValid = false
        $('#vul_name').parent().addClass('has-error')
      } else {
        $('#vul_company').parent().removeClass('has-error')
      }

      if ( !this.record.vul_company ) {
        isValid = false
        $('#vul_company').parent().addClass('has-error')
      } else {
        $('#vul_company').parent().removeClass('has-error')
      }
      return isValid;
    }
  },
  watch: {
    'record.vul_status': function(newVul, oldVal){
      if (newVul == 'unresolved'){
        this.record.vul_solve_date = null
      }
      if (newVul == 'resolved'){
        if (this.record.vul_solve_date == null){
          this.record.vul_solve_date = formatDate(new Date())
        }
      }
    },
    'record.vul_solve_date': function(newVul, oldVal){
      if (newVul != null){
        this.record.vul_status = 'resolved'
      }
    }
  }
}
</script>
