<template>
<div class="row clearfix">
    <div class="col-md-1 column">
         <button type="button" class="btn btn-primary" v-on:click="edit(-1)">添加记录</button>
    </div>
    <div class="col-md-1 column">
         <button type="button" class="btn btn-default" v-on:click="makeEmail">制作邮件</button>
    </div>
    <search></search>
</div>
<div class="row clearfix vulList">
    <div class="col-md-12 column">
      <button-group :value.sync="choose_items" buttons="false">
        <table class="table">
            <thead>
                <tr>
                  <th style="width: 3%"><checkbox type="info" v-on:click="checkAllOrNot"></checkbox></th>
                  <th style="width: 5%">id</th>
                  <th>漏洞名称</th>
                  <th style="width: 10%">业务线</th>
                  <th style="width: 10%">发现时间</th>
                  <th style="width: 20%"></th>
                </tr>
            </thead>
            <tbody v-for="item in RecordsList | orderBy 'id' -1 ">
                <tr :class="{ 'warning': item.vul_status == 'unresolved'}">
                  <td><checkbox :value="item.id" type="info"></checkbox></td>
                  <td>{{ item.id }}</td>
                  <td v-on:click="showVulDetail(item.id)">{{ item.vul_name }}</td>
                  <td>{{ item.vul_company }}</td>
                  <td>{{ item.vul_find_date | customTime }}</td>
                  <td>
                    <button v-if="item.vul_status == 'unresolved'" class="btn btn-success" v-on:click="changeStatus(item.id, 'resolved')" style="width:70px">解决它</button>
                    <button v-else class="btn btn-warning" v-on:click="changeStatus(item.id, 'unresolved')" style="width:70px">取消</button>
                    <button class="btn btn-primary" v-on:click="edit(item.id)">编辑</button>
                    <button class="btn btn-danger" v-on:click="removeRecord(item.id)">删除</button>
                  </td>
                </tr>
            </tbody>
        </table>
      </button-group>

        <aside :show.sync="has_edit_item" placement="left" header="漏洞详情" width="1200">
          <item-component v-if="has_edit_item" :edit_id="edit_item_id"></item-component>
        </aside>
    </div>
</div>
<div class="row clearfix pagination"><pagination :cur.sync="current_pageNum" :all="all_pageNum" v-on:btn-click="changePageNum"></pagination></div>
<vul-template v-if="showManyVulDetailHtml" :vul_ids="choose_items"></vul-template>
<vul-template v-if="showVulDetailHtml" :vul_ids="vul_detail_id"></vul-template>
</template>

<script>
import { aside } from 'vue-strap'
import { buttonGroup } from 'vue-strap'
import { checkbox } from 'vue-strap'

import Pagination from './Pagination'
import search from './Search'
import vulTemplate from './VulTemplate'
import itemComponent from './Item'
import { changeRecordStatus, getVulRecordsCnt,
         deleteRecord, loadBriefVulRecords, getVulType } from '../vuex/actions'

export default {
  components: {
    aside,
    checkbox,
    search,
    'pagination': Pagination,
    'button-group': buttonGroup,
    'item-component': itemComponent,
    'vul-template': vulTemplate
  },
  vuex: {
    getters: {
      RecordsList: ({ Records }) => Records.RecordsList
    },
    actions: {
      changeRecordStatus, getVulRecordsCnt,
      deleteRecord, loadBriefVulRecords, getVulType
    }
  },
  data () {
    return {
      choose_items: [],
      vul_detail_id: -1,
      edit_item_id: null,
      full_checked: false,
      showManyVulDetailHtml: false,
      showVulDetailHtml: false,
      current_pageNum: 1,
      all_pageNum: 0,
      pageSize: 20
    }
  },
  ready () {
    this.getVulType()
    this.setPagination()
    this.changePageNum(1)
  },
  computed:{
    has_edit_item: {
      get: function () {
        return this.edit_item_id != null
      },
      set: function (newVal) {
        if (newVal == false){
          // aside 关闭
          this.edit_item_id = null
        }
      }
    }
  },
  methods: {
    // 更改漏洞状态
    changeStatus (vid, status) {
      this.changeRecordStatus(vid, status)
    },

    // 换页查看
    changePageNum (pageNum) {
      this.current_pageNum = pageNum
      console.log('go page: ' +pageNum)
      this.loadBriefVulRecords(this.current_pageNum, this.pageSize)
    },

    // 设置总页数
    setPagination () {
      var vm = this
      this.getVulRecordsCnt().then(function(resp){
        var n = resp.json().data
        var pn = parseInt(n / vm.pageSize)
        if (n % vm.pageSize != 0){
          pn += 1
        }
        vm.all_pageNum = pn
      })
    },

    // 删除一条记录
    removeRecord (vid) {
      if ( confirm("确认删除？") ){
        this.deleteRecord(vid)
        this.setPagination()
      }
    },

    // 检查是否勾选全部
    checkAllOrNot () {
      this.full_checked = this.full_checked ? false:true
    },

    // 编辑漏洞
    edit (vid) {
      this.edit_item_id = vid
    },

    // 制作邮件
    makeEmail () {
      this.showManyVulDetailHtml = true
    },

    // 查看漏洞
    showVulDetail (vid) {
      this.vul_detail_id = vid
      this.showVulDetailHtml = true
    }
  },
  events: {
    'item_done' () {
      // item-component页编辑完成，回送通知事件
      this.edit_item_id = null
    },
    'dialog_done' () {
      this.showManyVulDetailHtml = false
      this.showVulDetailHtml = false
    }
  },
  watch: {
    'full_checked' (newVal, oldVal) {
      this.choose_items = []
      if (newVal){
        for(var idx=0; idx < this.RecordsList.length; idx++){
          this.choose_items.push(this.RecordsList[idx].id)
        }
      }
    }
  }
}
</script>

<style>
.vulList {
  margin-top: 30px;
}

.pagination {
  text-align: center;
  display: block;
}

.checkbox{
  margin-top: 0px;
  margin-bottom: 20px;
}

.table thead tr th,
.table tbody tr td{
  text-align: left;
  vertical-align: middle;
}

.table thead tr th:last-child,
.table tbody tr td:last-child{
  text-align: right;
}
</style>
