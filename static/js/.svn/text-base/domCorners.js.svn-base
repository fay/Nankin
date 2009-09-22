//domCorners by Alessandro Fulciniti on http://web-graphics.com/mtarchive/001660.php

function DomCheck(){
return(document.createElement && document.getElementById)
}

function DomCorners(id,bk,h,tries){
var el=document.getElementById(id);
if(el==null){
    if(tries==null) tries=200;
    if(tries>0)
        setTimeout("DomCorners('"+id+"','"+bk+"',"+h+","+(--tries)+")",50);
    return;
    }
var c=new Array(4);
for(var i=0;i<4;i++){
    c[i]=document.createElement("b");
    c[i].style.display="block";
    c[i].style.height=h+"px";
    c[i].style.fontSize="1px";
    if(i%2==0)
        c[i].style.background="url("+bk+") no-repeat 0 -"+ i*h + "px";
    else
        c[i].style.background="url("+bk+") no-repeat 100% -"+ i*h + "px";
    }
c[0].appendChild(c[1]);
c[2].appendChild(c[3]);
el.style.padding="0";
el.insertBefore(c[0],el.firstChild);
el.appendChild(c[2]);
}