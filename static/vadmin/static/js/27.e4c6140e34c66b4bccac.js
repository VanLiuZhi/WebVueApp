webpackJsonp([27],{Dxe4:function(t,e,n){(t.exports=n("FZ+f")(!1)).push([t.i,"\n.edit-input[data-v-43576fb4] {\n  padding-right: 100px;\n}\n.cancel-btn[data-v-43576fb4] {\n  position: absolute;\n  right: 15px;\n  top: 10px;\n}\n",""])},hG8D:function(t,e,n){var i=n("Dxe4");"string"==typeof i&&(i=[[t.i,i,""]]),i.locals&&(t.exports=i.locals);n("rjj0")("03523adf",i,!0)},q4NX:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=n("viA7"),a={name:"articleList",data:function(){return{list:null,total:0,listLoading:!0,listQuery:{page:1,limit:10}}},filters:{statusFilter:function(t){return{published:"success",draft:"info",deleted:"danger"}[t]}},created:function(){this.getList()},methods:{getList:function(){var t=this;this.listLoading=!0,Object(i.i)(this.listQuery).then(function(e){console.log(e),t.list=e.data.data.item,t.total=e.data.data.total,t.listLoading=!1})},handleSizeChange:function(t){this.listQuery.limit=t,this.getList()},handleCurrentChange:function(t){this.listQuery.page=t,this.getList()}}},l={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"app-container"},[n("el-table",{directives:[{name:"loading",rawName:"v-loading.body",value:t.listLoading,expression:"listLoading",modifiers:{body:!0}}],staticStyle:{width:"100%"},attrs:{data:t.list,border:"",fit:"","highlight-current-row":""}},[n("el-table-column",{attrs:{align:"center",label:"ID",width:"80"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("span",[t._v(t._s(e.row.id))])]}}])}),t._v(" "),n("el-table-column",{attrs:{width:"120px",align:"center",label:"Author"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("span",[t._v(t._s(e.row.author))])]}}])}),t._v(" "),n("el-table-column",{attrs:{width:"120px",align:"center",label:"Classify"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("span",[t._v(t._s(e.row.return_article_classify_name))])]}}])}),t._v(" "),n("el-table-column",{attrs:{"min-width":"300px",label:"Title"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("router-link",{staticClass:"link-type",attrs:{to:"/example/edit/"+e.row.id}},[n("span",[t._v(t._s(e.row.title))])])]}}])}),t._v(" "),n("el-table-column",{attrs:{align:"center",label:"Actions",width:"120"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("router-link",{attrs:{to:"/example/edit/"+e.row.guid}},[n("el-button",{attrs:{type:"primary",size:"small",icon:"el-icon-edit"}},[t._v("Edit")])],1)]}}])})],1),t._v(" "),n("div",{staticClass:"pagination-container"},[n("el-pagination",{attrs:{background:"","current-page":t.listQuery.page,"page-sizes":[10,20,30,50],"page-size":t.listQuery.limit,layout:"total, sizes, prev, pager, next, jumper",total:t.total},on:{"size-change":t.handleSizeChange,"current-change":t.handleCurrentChange}})],1)],1)},staticRenderFns:[]};var s=n("VU/8")(a,l,!1,function(t){n("hG8D")},"data-v-43576fb4",null);e.default=s.exports}});