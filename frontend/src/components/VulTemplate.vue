<template>
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog" style="width:80%">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                <h4 class="modal-title" id="myModalLabel">漏洞内容</h4>
            </div>
            <div class="modal-body"><div id="editor"></div></div>
        </div>
    </div>
</div>
</template>

<script>
import { getVulRecord } from '../vuex/actions'

export default {
  props: ['vul_ids'],
  vuex: {
    getters: {
      VulTypeList: ({ VulType }) => VulType.VulTypeList
    },
    actions: {
      getVulRecord,
    }
  },
  ready () {
    var vm = this

    if ( !(vm.vul_ids instanceof Array) ){
      vm.vul_ids = [vm.vul_ids]
    }

    // prompt panel
    $('#myModal').on('hidden.bs.modal', function (){
        vm.$dispatch('dialog_done')
    }).modal('show')

    // init summernote /* {{{ */
    $('#editor').summernote({
      height: 600,
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
      popover: {}
    })
    /* }}} */

    var content = ''
    var loopGet = function(idx){
      if(idx == vm.vul_ids.length){
        $('#editor').summernote('code', vm.makeNoteAfter(content))
      } else {
        var id = vm.vul_ids[idx]
        vm.getVulRecord(id).then(function(resp){
          content += vm.makeNote(resp.json().data)
        }).then(function(){
          loopGet(++idx)
        })
      }
    }
    loopGet(0)
  },
  methods: {
    makeNote (record) {
      var vl2cn = {
        'low': '低',
        'medium': '中',
        'high': '<font color="red">高</font>'
      }

      // 获取漏洞类型
      var v_type = ''
      for(var idx in this.VulTypeList){
        if(this.VulTypeList[idx].id == record.vul_type_id){
          v_type = this.VulTypeList[idx].vul_type
          break
        }
      }

      var note = '<div class="container">'
      + '<div class="row clearfix">'
      + '<div class="col-md-12 column">'
      + '<div style="width:160px"></div><div class="page-header"><h3>' +record.vul_name +'</h3></div>'
      + '<dl class="dl-horizontal">'
      + '<dt>漏洞类型: </dt><dd>' +v_type +'</dd>'
      + '<dt>漏洞等级: </dt><dd>' +vl2cn[record.vul_level] +'</dd>'
      + '<dt>漏洞内容: </dt><dd>' +record.vul_detail +'</dd>'
      + '</dl>'
      + '</div></div></div>'
      return note
    },
    makeNoteAfter (content){
      var note = content
      note += '<style>'
      + '.dl-horizontal dt { width: 80px; text-align: left; }'
      + '.dl-horizontal dd { margin-left: 85px }'
      + '</style>'
      return note
    }
  }
}
</script>
