import{d as p,u as m,r as f,_ as g,c as i,a as o,t as c,b,w as l,v as u,e as k,o as d}from"./index-DW8eHUYe.js";function w(){const e=document.cookie.split(";");for(const s of e){const[t,r]=s.split("=");if(t.trim()==="csrftoken")return r}return null}const v=p({data(){return{username:"",password:"",token:"",loginError:!1,loginErrorMessage:""}},methods:{async login(){this.loginError=!1,this.loginErrorMessage="";const s={method:"POST",headers:{"Content-type":"application/json","X-CSRFToken":w()||""},body:JSON.stringify({username:this.username,password:this.password})},t=await fetch("/api/login/",s);if(!t.ok){this.loginError=!0,this.loginErrorMessage="Login failed. Please try again.";return}var r=await t.json();const a=m();a.login(r.result.user,r.result.access_token),console.log(a.username),this.token=r.result.access_token,f.push("/dashboard"),alert("Login successful!")}}}),y={class:"container mt-5"},E={key:0,class:"alert alert-danger"},h={class:"form-group mb-3"},S={class:"form-group mb-4"};function C(e,s,t,r,a,M){return d(),i("div",y,[o("form",{onSubmit:s[2]||(s[2]=k(n=>e.login(),["prevent"])),class:"border p-4 bg-light"},[s[5]||(s[5]=o("h2",{class:"mb-4 text-center"},"Log In!",-1)),e.loginError?(d(),i("div",E,c(e.loginErrorMessage),1)):b("",!0),o("div",h,[s[3]||(s[3]=o("label",{for:"usernameInput",class:"form-label"},"Email",-1)),l(o("input",{type:"text","onUpdate:modelValue":s[0]||(s[0]=n=>e.username=n),class:"form-control",id:"usernameInput",placeholder:"Enter email",required:""},null,512),[[u,e.username]])]),o("div",S,[s[4]||(s[4]=o("label",{for:"passwordInput",class:"form-label"},"Password",-1)),l(o("input",{type:"password","onUpdate:modelValue":s[1]||(s[1]=n=>e.password=n),class:"form-control",id:"passwordInput",placeholder:"Password",required:""},null,512),[[u,e.password]])]),s[6]||(s[6]=o("button",{type:"submit",class:"btn btn-primary w-100"},"Submit",-1))],32)])}const I=g(v,[["render",C]]);export{I as default};
