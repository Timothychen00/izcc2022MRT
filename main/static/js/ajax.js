function load_data(){
    fetch('http://127.0.0.1:8080/games/捷大/api/teams',{ method: "GET",mode: 'cors' })
    .then((response)=>response.json())
    .then((res)=>{console.log(res);window.teams=res;draw_teams()});
}

function draw_teams(data){
    var box=document.getElementById('box');
    console.log(window.teams)
    for(i in window.teams)
    {
        let element = document.querySelector('area[title="'+window.teams[i]['now']+'"]');
        let x1=element.coords.split(',')[0];
        let y1=element.coords.split(',')[1];
        let x2=element.coords.split(',')[2];
        let y2=element.coords.split(',')[3];
        let element2 = document.querySelector('area[title="雙連"]');
        let e_x1=element2.coords.split(',')[0];
        let e_x2=element2.coords.split(',')[2];
        let r=parseFloat(e_x2)-parseFloat(e_x1);
        r*=1.4;
        console.log((parseFloat(y1)+parseFloat(y2))/2);

        let k="<div style='border-radius:50%;border:3px black solid;height:"+r+'px;width:'+r+'px;background-color:'+window.teams[i]['color']+';position:absolute;left:'+((parseFloat(x1)+parseFloat(x2))/2.00-r/2.00)+"px;top:"+((parseFloat(y1)+parseFloat(y2))/2-r/2)+'px;text-align:center;color:black;font-weight:900\'>'+i+'</div>';
        console.log(k);
        element.innerHTML=k;
    }
}
load_data();
draw_teams();