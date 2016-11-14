<template>
<div class="col-md-10 column">
  <div class="col-md-5" style="float:right">
    <div class="input-group">
      <div class="input-group-btn">
          <button type="button" style="width:100px" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
            {{ fields[search_field_id].key }} <span class="caret"></span>
          </button>
          <ul class="dropdown-menu" >
              <li v-for="(idx, field) in fields"><a href="#" @click="menuClick(idx)">{{ field.key }}</a></li>
          </ul>
      </div>
      <input type="text" class="form-control"  v-model="search_keyword" @keyup.enter="searchAction" placeholder="搜索关键字..." >
      <span class="glyphicon glyphicon-remove i-clear" v-show="hasSearch" @click='clearAction'></span>
    </div>
  </div>
</div>
</template>

<script>
import { searchBriefRecord, loadBriefVulRecords } from '../vuex/actions'

export default {
  vuex : {
    actions : {
      searchBriefRecord, loadBriefVulRecords
    }
  },
  data () {
    return {
      fields: [
        { 'key': '标题', 'value': 'title'},
        { 'key': '业务线', 'value': 'company'}
      ],
      search_field_id: 0,
      search_keyword: null
    }
  },
  methods : {
    menuClick : function (id) {
      this.search_field_id = id
    },
    searchAction: function () {
      this.searchBriefRecord(this.search_keyword, this.fields[this.search_field_id].value)
    },
    clearAction: function () {
        this.loadBriefVulRecords()
        this.search_keyword = null
    }
  },
  computed: {
    hasSearch: {
      get: function(){
        return this.search_keyword != null
      }
    }
  }

}
</script>

<style>
    .i-clear{
        position: absolute;
        right: 30px;
        top : 10px;
        cursor: pointer;
        z-index: 10;
        font-size : 16px;
        color :#777;
    }
    .i-search:hover,.i-clear:hover{
        color :#00aa9a;
    }

</style>
