import{s as h}from"./vue-multiselect.min-CHG4CS3T.js";import{d as S,f as n,g as E,u as I,r as k,_ as V,c as p,a as r,w as a,v as l,h as N,b as y,e as U,i as C,o as f}from"./index-Ct5SDsbx.js";function q(){const s=document.querySelector('meta[name="csrf-token"]');return s?s.getAttribute("content"):null}const P=S({components:{Multiselect:h},setup(){const s=n({first_name:"",last_name:"",email:"",date_of_birth:"",password:"",confirm_password:""}),e=n([]),m=n([]),i=n(!1),d=n(!1),b=async()=>{try{const t=await(await fetch("/api/hobbies/")).json();m.value=t.result}catch(o){console.error("Failed to fetch hobbies:",o)}};return E(()=>{console.log("Fetching hobbies..."),b()}),{form:s,selectedHobbies:e,hobbyOptions:m,passwordError:i,userExistsError:d,submit:async()=>{if(i.value=!1,d.value=!1,s.value.password!==s.value.confirm_password){i.value=!0;return}const o={first_name:s.value.first_name,last_name:s.value.last_name,email:s.value.email,date_of_birth:s.value.date_of_birth,password:s.value.password,password1:s.value.password,password2:s.value.confirm_password,hobbies:e.value.map(t=>({id:t.id,name:t.name}))};try{const t=q(),u=await(await fetch("/api/register/",{method:"POST",headers:{"Content-Type":"application/json","X-CSRFToken":t||""},body:JSON.stringify(o)})).json();if(u.success){const g={method:"POST",headers:{"Content-type":"application/json","X-CSRFToken":t||""},body:JSON.stringify({username:o.email,password:o.password})},w=await fetch("/api/login/",g);w.ok||alert("Signup successful, but login failed. Please try logging in.");const v=await w.json();I().login(v.result.user,v.result.access_token),k.push("/dashboard"),alert("Signup successful")}else u.error==="User already exists"?d.value=!0:alert("Signup failed: "+u.error)}catch(t){console.error("Error during signup:",t)}}}}}),T={class:"mb-3"},O={class:"mb-3"},j={class:"mb-3"},B={class:"mb-3"},F={class:"mb-3"},H={class:"mb-3"},M={class:"mb-3"},_={key:0,class:"alert alert-danger"},$={key:1,class:"alert alert-danger"};function D(s,e,m,i,d,b){const c=C("multiselect");return f(),p("form",{onSubmit:e[7]||(e[7]=U((...o)=>s.submit&&s.submit(...o),["prevent"])),class:"border p-4 bg-light"},[r("div",T,[e[8]||(e[8]=r("label",{for:"firstNameInput",class:"form-label"},"First Name",-1)),a(r("input",{type:"text","onUpdate:modelValue":e[0]||(e[0]=o=>s.form.first_name=o),class:"form-control",id:"firstNameInput",placeholder:"Enter first name",required:""},null,512),[[l,s.form.first_name]])]),r("div",O,[e[9]||(e[9]=r("label",{for:"lastNameInput",class:"form-label"},"Last Name",-1)),a(r("input",{type:"text","onUpdate:modelValue":e[1]||(e[1]=o=>s.form.last_name=o),class:"form-control",id:"lastNameInput",placeholder:"Enter last name",required:""},null,512),[[l,s.form.last_name]])]),r("div",j,[e[10]||(e[10]=r("label",{for:"emailInput",class:"form-label"},"Email",-1)),a(r("input",{type:"email","onUpdate:modelValue":e[2]||(e[2]=o=>s.form.email=o),class:"form-control",id:"emailInput",placeholder:"Enter email",required:""},null,512),[[l,s.form.email]])]),r("div",B,[e[11]||(e[11]=r("label",{for:"dobInput",class:"form-label"},"Date of Birth",-1)),a(r("input",{type:"date","onUpdate:modelValue":e[3]||(e[3]=o=>s.form.date_of_birth=o),class:"form-control",id:"dobInput",placeholder:"Enter date of birth",required:""},null,512),[[l,s.form.date_of_birth]])]),r("div",F,[e[12]||(e[12]=r("label",{for:"hobbiesInput",class:"form-label"},"Hobbies",-1)),N(c,{modelValue:s.selectedHobbies,"onUpdate:modelValue":e[4]||(e[4]=o=>s.selectedHobbies=o),options:s.hobbyOptions,label:"name","track-by":"id",multiple:""},null,8,["modelValue","options"])]),r("div",H,[e[13]||(e[13]=r("label",{for:"passwordInput",class:"form-label"},"Password",-1)),a(r("input",{type:"password","onUpdate:modelValue":e[5]||(e[5]=o=>s.form.password=o),class:"form-control",id:"passwordInput",placeholder:"Password",required:""},null,512),[[l,s.form.password]])]),r("div",M,[e[14]||(e[14]=r("label",{for:"passwordInput2",class:"form-label"},"Confirm Password",-1)),a(r("input",{type:"password","onUpdate:modelValue":e[6]||(e[6]=o=>s.form.confirm_password=o),class:"form-control",id:"passwordInput2",placeholder:"Confirm Password",required:""},null,512),[[l,s.form.confirm_password]])]),s.passwordError?(f(),p("div",_," Passwords do not match. ")):y("",!0),s.userExistsError?(f(),p("div",$," User already exists. ")):y("",!0),e[15]||(e[15]=r("button",{type:"submit",class:"btn btn-primary"},"Sign Up",-1))],32)}const L=V(P,[["render",D]]);export{L as default};
