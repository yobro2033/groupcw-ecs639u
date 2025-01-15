import{o as p,c as y,r as m,a as d,T as A,w as F,b as u,d as w,e as c,f as b,v as P,F as G,g as K,t as S,h as T,i as Q,u as W,j as V,k as Z,_ as x,l as L,m as o,n as O,p as _}from"./index-D8TLiKlr.js";function H(e){return e===0?!1:Array.isArray(e)&&e.length===0?!0:!e}function ee(e){return(...t)=>!e(...t)}function te(e,t){return e===void 0&&(e="undefined"),e===null&&(e="null"),e===!1&&(e="false"),e.toString().toLowerCase().indexOf(t.trim())!==-1}function j(e,t,s,r){return t?e.filter(a=>te(r(a,s),t)).sort((a,n)=>r(a,s).length-r(n,s).length):e}function se(e){return e.filter(t=>!t.$isLabel)}function M(e,t){return s=>s.reduce((r,a)=>a[e]&&a[e].length?(r.push({$groupLabel:a[t],$isLabel:!0}),r.concat(a[e])):r,[])}function ie(e,t,s,r,a){return n=>n.map(i=>{if(!i[s])return console.warn("Options passed to vue-multiselect do not contain groups, despite the config."),[];const l=j(i[s],e,t,a);return l.length?{[r]:i[r],[s]:l}:[]})}const U=(...e)=>t=>e.reduce((s,r)=>r(s),t);var le={data(){return{search:"",isOpen:!1,preferredOpenDirection:"below",optimizedHeight:this.maxHeight}},props:{internalSearch:{type:Boolean,default:!0},options:{type:Array,required:!0},multiple:{type:Boolean,default:!1},trackBy:{type:String},label:{type:String},searchable:{type:Boolean,default:!0},clearOnSelect:{type:Boolean,default:!0},hideSelected:{type:Boolean,default:!1},placeholder:{type:String,default:"Select option"},allowEmpty:{type:Boolean,default:!0},resetAfter:{type:Boolean,default:!1},closeOnSelect:{type:Boolean,default:!0},customLabel:{type:Function,default(e,t){return H(e)?"":t?e[t]:e}},taggable:{type:Boolean,default:!1},tagPlaceholder:{type:String,default:"Press enter to create a tag"},tagPosition:{type:String,default:"top"},max:{type:[Number,Boolean],default:!1},id:{default:null},optionsLimit:{type:Number,default:1e3},groupValues:{type:String},groupLabel:{type:String},groupSelect:{type:Boolean,default:!1},blockKeys:{type:Array,default(){return[]}},preserveSearch:{type:Boolean,default:!1},preselectFirst:{type:Boolean,default:!1},preventAutofocus:{type:Boolean,default:!1}},mounted(){!this.multiple&&this.max&&console.warn("[Vue-Multiselect warn]: Max prop should not be used when prop Multiple equals false."),this.preselectFirst&&!this.internalValue.length&&this.options.length&&this.select(this.filteredOptions[0])},computed:{internalValue(){return this.modelValue||this.modelValue===0?Array.isArray(this.modelValue)?this.modelValue:[this.modelValue]:[]},filteredOptions(){const e=this.search||"",t=e.toLowerCase().trim();let s=this.options.concat();return this.internalSearch?s=this.groupValues?this.filterAndFlat(s,t,this.label):j(s,t,this.label,this.customLabel):s=this.groupValues?M(this.groupValues,this.groupLabel)(s):s,s=this.hideSelected?s.filter(ee(this.isSelected)):s,this.taggable&&t.length&&!this.isExistingOption(t)&&(this.tagPosition==="bottom"?s.push({isTag:!0,label:e}):s.unshift({isTag:!0,label:e})),s.slice(0,this.optionsLimit)},valueKeys(){return this.trackBy?this.internalValue.map(e=>e[this.trackBy]):this.internalValue},optionKeys(){return(this.groupValues?this.flatAndStrip(this.options):this.options).map(t=>this.customLabel(t,this.label).toString().toLowerCase())},currentOptionLabel(){return this.multiple?this.searchable?"":this.placeholder:this.internalValue.length?this.getOptionLabel(this.internalValue[0]):this.searchable?"":this.placeholder}},watch:{internalValue:{handler(){this.resetAfter&&this.internalValue.length&&(this.search="",this.$emit("update:modelValue",this.multiple?[]:null))},deep:!0},search(){this.$emit("search-change",this.search)}},emits:["open","search-change","close","select","update:modelValue","remove","tag"],methods:{getValue(){return this.multiple?this.internalValue:this.internalValue.length===0?null:this.internalValue[0]},filterAndFlat(e,t,s){return U(ie(t,s,this.groupValues,this.groupLabel,this.customLabel),M(this.groupValues,this.groupLabel))(e)},flatAndStrip(e){return U(M(this.groupValues,this.groupLabel),se)(e)},updateSearch(e){this.search=e},isExistingOption(e){return this.options?this.optionKeys.indexOf(e)>-1:!1},isSelected(e){const t=this.trackBy?e[this.trackBy]:e;return this.valueKeys.indexOf(t)>-1},isOptionDisabled(e){return!!e.$isDisabled},getOptionLabel(e){if(H(e))return"";if(e.isTag)return e.label;if(e.$isLabel)return e.$groupLabel;const t=this.customLabel(e,this.label);return H(t)?"":t},select(e,t){if(e.$isLabel&&this.groupSelect){this.selectGroup(e);return}if(!(this.blockKeys.indexOf(t)!==-1||this.disabled||e.$isDisabled||e.$isLabel)&&!(this.max&&this.multiple&&this.internalValue.length===this.max)&&!(t==="Tab"&&!this.pointerDirty)){if(e.isTag)this.$emit("tag",e.label,this.id),this.search="",this.closeOnSelect&&!this.multiple&&this.deactivate();else{if(this.isSelected(e)){t!=="Tab"&&this.removeElement(e);return}this.multiple?this.$emit("update:modelValue",this.internalValue.concat([e])):this.$emit("update:modelValue",e),this.$emit("select",e,this.id),this.clearOnSelect&&(this.search="")}this.closeOnSelect&&this.deactivate()}},selectGroup(e){const t=this.options.find(s=>s[this.groupLabel]===e.$groupLabel);if(t){if(this.wholeGroupSelected(t)){this.$emit("remove",t[this.groupValues],this.id);const s=this.trackBy?t[this.groupValues].map(a=>a[this.trackBy]):t[this.groupValues],r=this.internalValue.filter(a=>s.indexOf(this.trackBy?a[this.trackBy]:a)===-1);this.$emit("update:modelValue",r)}else{let s=t[this.groupValues].filter(r=>!(this.isOptionDisabled(r)||this.isSelected(r)));this.max&&s.splice(this.max-this.internalValue.length),this.$emit("select",s,this.id),this.$emit("update:modelValue",this.internalValue.concat(s))}this.closeOnSelect&&this.deactivate()}},wholeGroupSelected(e){return e[this.groupValues].every(t=>this.isSelected(t)||this.isOptionDisabled(t))},wholeGroupDisabled(e){return e[this.groupValues].every(this.isOptionDisabled)},removeElement(e,t=!0){if(this.disabled||e.$isDisabled)return;if(!this.allowEmpty&&this.internalValue.length<=1){this.deactivate();return}const s=typeof e=="object"?this.valueKeys.indexOf(e[this.trackBy]):this.valueKeys.indexOf(e);if(this.multiple){const r=this.internalValue.slice(0,s).concat(this.internalValue.slice(s+1));this.$emit("update:modelValue",r)}else this.$emit("update:modelValue",null);this.$emit("remove",e,this.id),this.closeOnSelect&&t&&this.deactivate()},removeLastElement(){this.blockKeys.indexOf("Delete")===-1&&this.search.length===0&&Array.isArray(this.internalValue)&&this.internalValue.length&&this.removeElement(this.internalValue[this.internalValue.length-1],!1)},activate(){this.isOpen||this.disabled||(this.adjustPosition(),this.groupValues&&this.pointer===0&&this.filteredOptions.length&&(this.pointer=1),this.isOpen=!0,this.searchable?(this.preserveSearch||(this.search=""),this.preventAutofocus||this.$nextTick(()=>this.$refs.search&&this.$refs.search.focus())):this.preventAutofocus||typeof this.$el<"u"&&this.$el.focus(),this.$emit("open",this.id))},deactivate(){this.isOpen&&(this.isOpen=!1,this.searchable?this.$refs.search!==null&&typeof this.$refs.search<"u"&&this.$refs.search.blur():typeof this.$el<"u"&&this.$el.blur(),this.preserveSearch||(this.search=""),this.$emit("close",this.getValue(),this.id))},toggle(){this.isOpen?this.deactivate():this.activate()},adjustPosition(){if(typeof window>"u")return;const e=this.$el.getBoundingClientRect().top,t=window.innerHeight-this.$el.getBoundingClientRect().bottom;t>this.maxHeight||t>e||this.openDirection==="below"||this.openDirection==="bottom"?(this.preferredOpenDirection="below",this.optimizedHeight=Math.min(t-40,this.maxHeight)):(this.preferredOpenDirection="above",this.optimizedHeight=Math.min(e-40,this.maxHeight))}}},oe={data(){return{pointer:0,pointerDirty:!1}},props:{showPointer:{type:Boolean,default:!0},optionHeight:{type:Number,default:40}},computed:{pointerPosition(){return this.pointer*this.optionHeight},visibleElements(){return this.optimizedHeight/this.optionHeight}},watch:{filteredOptions(){this.pointerAdjust()},isOpen(){this.pointerDirty=!1},pointer(){this.$refs.search&&this.$refs.search.setAttribute("aria-activedescendant",this.id+"-"+this.pointer.toString())}},methods:{optionHighlight(e,t){return{"multiselect__option--highlight":e===this.pointer&&this.showPointer,"multiselect__option--selected":this.isSelected(t)}},groupHighlight(e,t){if(!this.groupSelect)return["multiselect__option--disabled",{"multiselect__option--group":t.$isLabel}];const s=this.options.find(r=>r[this.groupLabel]===t.$groupLabel);return s&&!this.wholeGroupDisabled(s)?["multiselect__option--group",{"multiselect__option--highlight":e===this.pointer&&this.showPointer},{"multiselect__option--group-selected":this.wholeGroupSelected(s)}]:"multiselect__option--disabled"},addPointerElement({key:e}="Enter"){this.filteredOptions.length>0&&this.select(this.filteredOptions[this.pointer],e),this.pointerReset()},pointerForward(){this.pointer<this.filteredOptions.length-1&&(this.pointer++,this.$refs.list.scrollTop<=this.pointerPosition-(this.visibleElements-1)*this.optionHeight&&(this.$refs.list.scrollTop=this.pointerPosition-(this.visibleElements-1)*this.optionHeight),this.filteredOptions[this.pointer]&&this.filteredOptions[this.pointer].$isLabel&&!this.groupSelect&&this.pointerForward()),this.pointerDirty=!0},pointerBackward(){this.pointer>0?(this.pointer--,this.$refs.list.scrollTop>=this.pointerPosition&&(this.$refs.list.scrollTop=this.pointerPosition),this.filteredOptions[this.pointer]&&this.filteredOptions[this.pointer].$isLabel&&!this.groupSelect&&this.pointerBackward()):this.filteredOptions[this.pointer]&&this.filteredOptions[0].$isLabel&&!this.groupSelect&&this.pointerForward(),this.pointerDirty=!0},pointerReset(){this.closeOnSelect&&(this.pointer=0,this.$refs.list&&(this.$refs.list.scrollTop=0))},pointerAdjust(){this.pointer>=this.filteredOptions.length-1&&(this.pointer=this.filteredOptions.length?this.filteredOptions.length-1:0),this.filteredOptions.length>0&&this.filteredOptions[this.pointer].$isLabel&&!this.groupSelect&&this.pointerForward()},pointerSet(e){this.pointer=e,this.pointerDirty=!0}}},R={name:"vue-multiselect",mixins:[le,oe],compatConfig:{MODE:3,ATTR_ENUMERATED_COERCION:!1},props:{name:{type:String,default:""},modelValue:{type:null,default(){return[]}},selectLabel:{type:String,default:"Press enter to select"},selectGroupLabel:{type:String,default:"Press enter to select group"},selectedLabel:{type:String,default:"Selected"},deselectLabel:{type:String,default:"Press enter to remove"},deselectGroupLabel:{type:String,default:"Press enter to deselect group"},showLabels:{type:Boolean,default:!0},limit:{type:Number,default:99999},maxHeight:{type:Number,default:300},limitText:{type:Function,default:e=>`and ${e} more`},loading:{type:Boolean,default:!1},disabled:{type:Boolean,default:!1},spellcheck:{type:Boolean,default:!1},openDirection:{type:String,default:""},showNoOptions:{type:Boolean,default:!0},showNoResults:{type:Boolean,default:!0},tabindex:{type:Number,default:0},required:{type:Boolean,default:!1}},computed:{hasOptionGroup(){return this.groupValues&&this.groupLabel&&this.groupSelect},isSingleLabelVisible(){return(this.singleValue||this.singleValue===0)&&(!this.isOpen||!this.searchable)&&!this.visibleValues.length},isPlaceholderVisible(){return!this.internalValue.length&&(!this.searchable||!this.isOpen)},visibleValues(){return this.multiple?this.internalValue.slice(0,this.limit):[]},singleValue(){return this.internalValue[0]},deselectLabelText(){return this.showLabels?this.deselectLabel:""},deselectGroupLabelText(){return this.showLabels?this.deselectGroupLabel:""},selectLabelText(){return this.showLabels?this.selectLabel:""},selectGroupLabelText(){return this.showLabels?this.selectGroupLabel:""},selectedLabelText(){return this.showLabels?this.selectedLabel:""},inputStyle(){return this.searchable||this.multiple&&this.modelValue&&this.modelValue.length?this.isOpen?{width:"100%"}:{width:"0",position:"absolute",padding:"0"}:""},contentStyle(){return this.options.length?{display:"inline-block"}:{display:"block"}},isAbove(){return this.openDirection==="above"||this.openDirection==="top"?!0:this.openDirection==="below"||this.openDirection==="bottom"?!1:this.preferredOpenDirection==="above"},showSearchInput(){return this.searchable&&(this.hasSingleSelectedSlot&&(this.visibleSingleValue||this.visibleSingleValue===0)?this.isOpen:!0)}}};const re={ref:"tags",class:"multiselect__tags"},ne={class:"multiselect__tags-wrap"},ae={class:"multiselect__spinner"},ue={key:0},de={class:"multiselect__option"},he={class:"multiselect__option"},pe=T("No elements found. Consider changing the search query."),fe={class:"multiselect__option"},me=T("List is empty.");function be(e,t,s,r,a,n){return p(),y("div",{tabindex:e.searchable?-1:s.tabindex,class:[{"multiselect--active":e.isOpen,"multiselect--disabled":s.disabled,"multiselect--above":n.isAbove,"multiselect--has-options-group":n.hasOptionGroup},"multiselect"],onFocus:t[14]||(t[14]=i=>e.activate()),onBlur:t[15]||(t[15]=i=>e.searchable?!1:e.deactivate()),onKeydown:[t[16]||(t[16]=w(u(i=>e.pointerForward(),["self","prevent"]),["down"])),t[17]||(t[17]=w(u(i=>e.pointerBackward(),["self","prevent"]),["up"]))],onKeypress:t[18]||(t[18]=w(u(i=>e.addPointerElement(i),["stop","self"]),["enter","tab"])),onKeyup:t[19]||(t[19]=w(i=>e.deactivate(),["esc"])),role:"combobox","aria-owns":"listbox-"+e.id},[m(e.$slots,"caret",{toggle:e.toggle},()=>[d("div",{onMousedown:t[1]||(t[1]=u(i=>e.toggle(),["prevent","stop"])),class:"multiselect__select"},null,32)]),m(e.$slots,"clear",{search:e.search}),d("div",re,[m(e.$slots,"selection",{search:e.search,remove:e.removeElement,values:n.visibleValues,isOpen:e.isOpen},()=>[b(d("div",ne,[(p(!0),y(G,null,K(n.visibleValues,(i,l)=>m(e.$slots,"tag",{option:i,search:e.search,remove:e.removeElement},()=>[(p(),y("span",{class:"multiselect__tag",key:l},[d("span",{textContent:S(e.getOptionLabel(i))},null,8,["textContent"]),d("i",{tabindex:"1",onKeypress:w(u(f=>e.removeElement(i),["prevent"]),["enter"]),onMousedown:u(f=>e.removeElement(i),["prevent"]),class:"multiselect__tag-icon"},null,40,["onKeypress","onMousedown"])]))])),256))],512),[[P,n.visibleValues.length>0]]),e.internalValue&&e.internalValue.length>s.limit?m(e.$slots,"limit",{key:0},()=>[d("strong",{class:"multiselect__strong",textContent:S(s.limitText(e.internalValue.length-s.limit))},null,8,["textContent"])]):c("v-if",!0)]),d(A,{name:"multiselect__loading"},{default:F(()=>[m(e.$slots,"loading",{},()=>[b(d("div",ae,null,512),[[P,s.loading]])])]),_:3}),e.searchable?(p(),y("input",{key:0,ref:"search",name:s.name,id:e.id,type:"text",autocomplete:"off",spellcheck:s.spellcheck,placeholder:e.placeholder,required:s.required,style:n.inputStyle,value:e.search,disabled:s.disabled,tabindex:s.tabindex,onInput:t[2]||(t[2]=i=>e.updateSearch(i.target.value)),onFocus:t[3]||(t[3]=u(i=>e.activate(),["prevent"])),onBlur:t[4]||(t[4]=u(i=>e.deactivate(),["prevent"])),onKeyup:t[5]||(t[5]=w(i=>e.deactivate(),["esc"])),onKeydown:[t[6]||(t[6]=w(u(i=>e.pointerForward(),["prevent"]),["down"])),t[7]||(t[7]=w(u(i=>e.pointerBackward(),["prevent"]),["up"])),t[9]||(t[9]=w(u(i=>e.removeLastElement(),["stop"]),["delete"]))],onKeypress:t[8]||(t[8]=w(u(i=>e.addPointerElement(i),["prevent","stop","self"]),["enter"])),class:"multiselect__input","aria-controls":"listbox-"+e.id},null,44,["name","id","spellcheck","placeholder","required","value","disabled","tabindex","aria-controls"])):c("v-if",!0),n.isSingleLabelVisible?(p(),y("span",{key:1,class:"multiselect__single",onMousedown:t[10]||(t[10]=u((...i)=>e.toggle&&e.toggle(...i),["prevent"]))},[m(e.$slots,"singleLabel",{option:n.singleValue},()=>[T(S(e.currentOptionLabel),1)])],32)):c("v-if",!0),n.isPlaceholderVisible?(p(),y("span",{key:2,class:"multiselect__placeholder",onMousedown:t[11]||(t[11]=u((...i)=>e.toggle&&e.toggle(...i),["prevent"]))},[m(e.$slots,"placeholder",{},()=>[T(S(e.placeholder),1)])],32)):c("v-if",!0)],512),d(A,{name:"multiselect"},{default:F(()=>[b(d("div",{class:"multiselect__content-wrapper",onFocus:t[12]||(t[12]=(...i)=>e.activate&&e.activate(...i)),tabindex:"-1",onMousedown:t[13]||(t[13]=u(()=>{},["prevent"])),style:{maxHeight:e.optimizedHeight+"px"},ref:"list"},[d("ul",{class:"multiselect__content",style:n.contentStyle,role:"listbox",id:"listbox-"+e.id,"aria-multiselectable":e.multiple},[m(e.$slots,"beforeList"),e.multiple&&e.max===e.internalValue.length?(p(),y("li",ue,[d("span",de,[m(e.$slots,"maxElements",{},()=>[T("Maximum of "+S(e.max)+" options selected. First remove a selected option to select another.",1)])])])):c("v-if",!0),!e.max||e.internalValue.length<e.max?(p(!0),y(G,{key:1},K(e.filteredOptions,(i,l)=>(p(),y("li",{class:"multiselect__element",key:l,"aria-selected":e.isSelected(i),id:e.id+"-"+l,role:i&&(i.$isLabel||i.$isDisabled)?null:"option"},[i&&(i.$isLabel||i.$isDisabled)?c("v-if",!0):(p(),y("span",{key:0,class:[e.optionHighlight(l,i),"multiselect__option"],onClick:u(f=>e.select(i),["stop"]),onMouseenter:u(f=>e.pointerSet(l),["self"]),"data-select":i&&i.isTag?e.tagPlaceholder:n.selectLabelText,"data-selected":n.selectedLabelText,"data-deselect":n.deselectLabelText},[m(e.$slots,"option",{option:i,search:e.search,index:l},()=>[d("span",null,S(e.getOptionLabel(i)),1)])],42,["onClick","onMouseenter","data-select","data-selected","data-deselect"])),i&&(i.$isLabel||i.$isDisabled)?(p(),y("span",{key:1,"data-select":e.groupSelect&&n.selectGroupLabelText,"data-deselect":e.groupSelect&&n.deselectGroupLabelText,class:[e.groupHighlight(l,i),"multiselect__option"],onMouseenter:u(f=>e.groupSelect&&e.pointerSet(l),["self"]),onMousedown:u(f=>e.selectGroup(i),["prevent"])},[m(e.$slots,"option",{option:i,search:e.search,index:l},()=>[d("span",null,S(e.getOptionLabel(i)),1)])],42,["data-select","data-deselect","onMouseenter","onMousedown"])):c("v-if",!0)],8,["aria-selected","id","role"]))),128)):c("v-if",!0),b(d("li",null,[d("span",he,[m(e.$slots,"noResult",{search:e.search},()=>[pe])])],512),[[P,s.showNoResults&&e.filteredOptions.length===0&&e.search&&!s.loading]]),b(d("li",null,[d("span",fe,[m(e.$slots,"noOptions",{},()=>[me])])],512),[[P,s.showNoOptions&&(e.options.length===0||n.hasOptionGroup===!0&&e.filteredOptions.length===0)&&!e.search&&!s.loading]]),m(e.$slots,"afterList")],12,["id","aria-multiselectable"])],36),[[P,e.isOpen]])]),_:3})],42,["tabindex","aria-owns"])}R.render=be;function C(){const e=document.cookie.split(";");for(const t of e){const[s,r]=t.split("=");if(s.trim()==="csrftoken")return r}return null}const ce=Q({components:{Multiselect:R},setup(){const e=W(),t=V(null),s=V([]),r=V({first_name:"",last_name:"",email:"",date_of_birth:"",selectedHobbies:[]}),a=V({name:"",description:""}),n=V(!1),i=V({old_password:"",new_password:"",new_password_confirm:""}),l=V(!1),f=V(null),k=V(null),$=V(null),E=async()=>{try{const g=await(await fetch("/api/my_profile",{method:"GET",headers:{"Content-Type":"application/json",Authorization:"Token "+e.token}})).json();g.success==="true"?(t.value=g.result,t.value&&(r.value={first_name:t.value.first_name,last_name:t.value.last_name,email:t.value.email,date_of_birth:t.value.date_of_birth,selectedHobbies:t.value.hobbies.map(v=>v)})):f.value=g.error}catch(h){console.error("Error loading profile:",h),f.value="An error occurred while loading profile."}},z=async()=>{try{const g=await(await fetch("/api/hobbies/",{method:"GET",headers:{"Content-Type":"application/json"}})).json();g.success==="true"?s.value=g.result:f.value=g.error}catch(h){console.error("Error loading hobbies list:",h),f.value="An error occurred while loading hobbies list."}},q=async()=>{f.value=null,$.value=null;try{const g=r.value.selectedHobbies.filter(B=>B&&B.id!=="add_new").map(B=>B.id),v=C(),N=await(await fetch("/api/profile/update/",{method:"PUT",headers:{"Content-Type":"application/json",Authorization:"Token "+e.token,"X-CSRFToken":v||""},body:JSON.stringify({first_name:r.value.first_name,last_name:r.value.last_name,email:r.value.email,date_of_birth:r.value.date_of_birth,hobbies:g})})).json();N.success==="true"?($.value="Profile updated successfully!",E()):f.value=N.error}catch(h){console.error("Error updating profile:",h),f.value="An error occurred while updating profile."}},I=h=>{a.value.name=h,n.value=!0},J=async()=>{f.value=null,$.value=null;try{const h=C(),v=await(await fetch("/api/hobbies/add/",{method:"PUT",headers:{"Content-Type":"application/json",Authorization:"Token "+e.token,"X-CSRFToken":h||""},body:JSON.stringify(a.value)})).json();v.success==="true"?(s.value.push(v.result),r.value.selectedHobbies.push(v.result),a.value={name:"",description:""},n.value=!1,$.value="New hobby added successfully!"):f.value=v.error}catch(h){console.error("Failed to add new hobby:",h),f.value="An error occurred while adding new hobby."}},X=()=>{l.value=!0},D=()=>{l.value=!1},Y=async()=>{k.value=null,$.value=null;try{if(i.value.new_password!==i.value.new_password_confirm){k.value="New passwords do not match.";return}if(i.value.new_password.length<8){k.value="New password must be at least 8 characters long.";return}const h=C(),v=await(await fetch("/api/profile/change_password/",{method:"POST",headers:{"Content-Type":"application/json",Authorization:"Token "+e.token,"X-CSRFToken":h||""},body:JSON.stringify(i.value)})).json();v.success==="true"?($.value="Password changed successfully!",i.value={old_password:"",new_password:"",new_password_confirm:""},D()):k.value=v.error}catch(h){console.error("Error changing password:",h),k.value="An error occurred while changing password."}};return Z(()=>{E(),z()}),{userProfile:t,hobbiesList:s,editProfile:r,newHobby:a,showNewHobbyForm:n,passwordForm:i,showPasswordModal:l,errorMessage:f,modalErrorMessage:k,successMessage:$,updateProfile:q,addNewHobbyOption:I,addNewHobby:J,showChangePasswordModal:X,closeChangePasswordModal:D,changePassword:Y}}}),ge={class:"container mt-5"},ve={class:"profile-section mb-4"},ye={key:0},we=["src"],Ve={key:0,class:"mt-3"},Se={class:"change-password-section"},Oe={key:0,class:"modal",tabindex:"-1",role:"dialog",style:{display:"block"}},$e={class:"modal-dialog",role:"document"},Le={class:"modal-body"},ke={key:0,class:"alert alert-danger"},Pe={class:"modal-footer"},Te={key:1,class:"alert alert-danger"},Be={key:2,class:"alert alert-success"};function He(e,t,s,r,a,n){const i=_("Multiselect");return p(),L("div",ge,[t[29]||(t[29]=o("h1",null,"User Dashboard",-1)),o("div",ve,[t[23]||(t[23]=o("h3",null,"Your Profile",-1)),e.userProfile?(p(),L("div",ye,[o("img",{src:e.userProfile.profile_image,alt:"Profile Picture",class:"profile-image mb-3"},null,8,we),o("div",null,[t[15]||(t[15]=o("label",null,"First Name:",-1)),b(o("input",{type:"text","onUpdate:modelValue":t[0]||(t[0]=l=>e.editProfile.first_name=l),class:"form-control mb-2"},null,512),[[O,e.editProfile.first_name]])]),o("div",null,[t[16]||(t[16]=o("label",null,"Last Name:",-1)),b(o("input",{type:"text","onUpdate:modelValue":t[1]||(t[1]=l=>e.editProfile.last_name=l),class:"form-control mb-2"},null,512),[[O,e.editProfile.last_name]])]),o("div",null,[t[17]||(t[17]=o("label",null,"Email:",-1)),b(o("input",{type:"email","onUpdate:modelValue":t[2]||(t[2]=l=>e.editProfile.email=l),class:"form-control mb-2"},null,512),[[O,e.editProfile.email]])]),o("div",null,[t[18]||(t[18]=o("label",null,"Date of Birth:",-1)),b(o("input",{type:"date","onUpdate:modelValue":t[3]||(t[3]=l=>e.editProfile.date_of_birth=l),class:"form-control mb-2"},null,512),[[O,e.editProfile.date_of_birth]])]),o("div",null,[t[21]||(t[21]=o("label",null,"Hobbies:",-1)),d(i,{modelValue:e.editProfile.selectedHobbies,"onUpdate:modelValue":t[4]||(t[4]=l=>e.editProfile.selectedHobbies=l),options:e.hobbiesList,multiple:!0,searchable:!0,taggable:!0,label:"name","track-by":"id",placeholder:"Select or add hobbies",onTag:e.addNewHobbyOption},null,8,["modelValue","options","onTag"]),e.showNewHobbyForm?(p(),L("div",Ve,[t[19]||(t[19]=o("label",null,"New Hobby Name:",-1)),b(o("input",{type:"text","onUpdate:modelValue":t[5]||(t[5]=l=>e.newHobby.name=l),placeholder:"Enter hobby name",class:"form-control mb-2"},null,512),[[O,e.newHobby.name]]),t[20]||(t[20]=o("label",null,"New Hobby Description:",-1)),b(o("input",{type:"text","onUpdate:modelValue":t[6]||(t[6]=l=>e.newHobby.description=l),placeholder:"Enter hobby description",class:"form-control mb-2"},null,512),[[O,e.newHobby.description]]),o("button",{onClick:t[7]||(t[7]=(...l)=>e.addNewHobby&&e.addNewHobby(...l)),class:"btn btn-primary"}," Add Hobby ")])):c("",!0)]),t[22]||(t[22]=o("br",null,null,-1)),o("button",{onClick:t[8]||(t[8]=(...l)=>e.updateProfile&&e.updateProfile(...l)),class:"btn btn-primary"}," Save Profile ")])):c("",!0)]),o("div",Se,[t[24]||(t[24]=o("h3",null,"Change Password",-1)),o("button",{class:"btn btn-danger",onClick:t[9]||(t[9]=l=>e.showPasswordModal=!0)}," Change Password ")]),e.showPasswordModal?(p(),L("div",Oe,[o("div",$e,[t[28]||(t[28]=o("div",{class:"modal-header"},[o("h5",{class:"modal-title"},"Update Password")],-1)),o("div",Le,[o("div",null,[t[25]||(t[25]=o("label",null,"Old Password:",-1)),b(o("input",{type:"password","onUpdate:modelValue":t[10]||(t[10]=l=>e.passwordForm.old_password=l),class:"form-control mb-2"},null,512),[[O,e.passwordForm.old_password]])]),o("div",null,[t[26]||(t[26]=o("label",null,"New Password:",-1)),b(o("input",{type:"password","onUpdate:modelValue":t[11]||(t[11]=l=>e.passwordForm.new_password=l),class:"form-control mb-2"},null,512),[[O,e.passwordForm.new_password]])]),o("div",null,[t[27]||(t[27]=o("label",null,"Confirm New Password:",-1)),b(o("input",{type:"password","onUpdate:modelValue":t[12]||(t[12]=l=>e.passwordForm.new_password_confirm=l),class:"form-control mb-2"},null,512),[[O,e.passwordForm.new_password_confirm]])])]),e.modalErrorMessage?(p(),L("div",ke,S(e.modalErrorMessage),1)):c("",!0),o("div",Pe,[o("button",{type:"button",class:"btn btn-warning",onClick:t[13]||(t[13]=(...l)=>e.changePassword&&e.changePassword(...l))}," Update Password "),o("button",{type:"button",class:"btn btn-secondary",onClick:t[14]||(t[14]=(...l)=>e.closeChangePasswordModal&&e.closeChangePasswordModal(...l))}," Close ")])])])):c("",!0),t[30]||(t[30]=o("br",null,null,-1)),e.errorMessage?(p(),L("div",Te,S(e.errorMessage),1)):c("",!0),e.successMessage?(p(),L("div",Be,S(e.successMessage),1)):c("",!0)])}const Ee=x(ce,[["render",He],["__scopeId","data-v-029142c7"]]);export{Ee as default};
