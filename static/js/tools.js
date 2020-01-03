function clickPart0TableButton() {
    var button = $("#part-0-table-button");
    var eles = $("#part0-body").find("tr");
    if (button.attr("register") === "1") {
        for (var i = 0; i < eles.length; i++) {
            var ele = eles[i];
            $(ele).removeClass("hidden");
        }
        button.attr("register", "0");
        button.text("收起");
    } else {
        for (var i = 0; i < eles.length-1; i++) {
            if (i > 20) {
                var ele = eles[i];
                $(ele).addClass("hidden");
            }
        }
        button.text("查看全部");
        button.attr("register", "1");
    }
}
