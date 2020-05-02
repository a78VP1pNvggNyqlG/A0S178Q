window.onload=function() {
    var sGoodlist=getCookie("aGoodList");
    var aGoodList=sGoodlist?JSON.parse(sGoodlist):[];
    for (var i = 0; i < aGoodList.length; i++) {
        var oLi=document.createElement('li');    
        oLi.innerHTML='<a href="javascript:;" class="abtn" data-id="'+aGoodList[i].id+'">delete</a><img src="'+aGoodList[i].src+'" /><div class="title">'+aGoodList[i].title+'</div><div class="price">￥'+aGoodList[i].price+aGoodList[i].amount+'</div>';
        $("list").appendChild(oLi);
        var oAbtn=getTagByClassName("abtn");
        oAbtn[i].index=i;
        oAbtn[i].onclick=function() {
            if (aGoodList[this.index].amount>1) {
                aGoodList[this.index].amount--
            }
            else
            {
                $("list").removeChild(this.parentNode);
                aGoodList.splice(this.index,1)
            }
            setCookie("aGoodList",JSON.stringify(aGoodList),7);
            window.location.reload();
        } 
    }
}