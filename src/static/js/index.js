
MAX=24;
MIN=1;

//load

var num=MIN;

var loop=null;
var runTime=0;
function search(){
    clearInterval(loop);
    num=1;
    document.getElementById("load_dis").style.cssText='display:flex;';
    loop=setInterval(function () {
//        console.log(runTime);
        document.getElementById("load_dis").style.cssText='display:none;';
        document.getElementById("change").src="static/html/t"+num+".html?_t="+Date.now();
//        window.location.reload();
        runTime+=1;
        if(runTime>0){
            clearInterval(loop);
        }
    },20000)
}

//next
function next(){
    num+=1;
    if(num>MAX){
        num=MIN;
    }
    document.getElementById("change").src="static/html/t"+num+".html?_t="+Date.now();
}

//pre
function pre(){
    num-=1;
    if(num<MIN){
        num=MAX;
    }
    document.getElementById("change").src="/static/html/t"+num+".html?_t="+Date.now();
}

//start
function start(){
    clearInterval(loop);
    console.log("start success");
    loop=setInterval(function () {
        console.log(num);
        num+=1;
        if(num>MAX){
            num=MIN;
        }
        document.getElementById("change").src="static/html/t"+num+".html?_t="+Date.now();
    },5000);
}

//pause
function pause(){
    clearInterval(loop);
    console.log("pause");
}



function input(){
    console.log("focus");
    document.getElementById("select").value="";
    document.getElementById("select").style.cssText="color:black;";
}
