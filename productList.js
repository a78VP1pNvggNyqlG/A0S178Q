window.onload=function() {
    var oAbtn=getTagByClassName("abtn");
    for (var i = 0; i < oAbtn.length; i++) {
        oAbtn[i].onclick=function() {
            var goodId=this.getAttribute('data-id');
            var goodTitle=this.getAttribute('data-title');
            var goodPrice=this.getAttribute('data-price');
            var goodAmount=this.getAttribute('data-amount');
            var oGood={
                id:goodId,
                title:goodTitle,
                price:goodPrice,
                amount:goodAmount
            };
            var sGoodlist=getCookie("aGoodList")
            var aGoodList=sGoodlist?JSON.parse(sGoodlist):[];
            var whetherExsits=aGoodList.every(function(v) {
                if (v.id===oGood.id) {
                    v.amount++;
                    return false;
                }
                return true;
            });
            if (whetherExsits) {
                aGoodList.push(oGood);
            }
            setCookie("aGoodList",JSON.stringify(aGoodList),7);
        }
    }
}  