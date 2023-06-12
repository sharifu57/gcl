$(document).on("click",".new-borrower-link",function(e){
    e.preventDefault();
    let $link = $(this);
    $.confirm({
        type: "green",
        closeIcon: true,
        columnClass: "large",
        title: "ADD NEW BORROWER",
        titleClass: "text-center",
        content: "url:" + $link.data("href"),
        onContentReady: function(){
            var self = this;
            $(document).on("submit", ".borrower_form_class", function (e) {
                e.preventDefault();
                let $form = $(this);
                self.showLoading();
                $.ajax({
                    url: $form.attr("action"),
                    type: $form.attr("method"),
                    data: $form.serializeArray(),
                }).done(function (response) {
                    self.hideLoading();
                    try {
                        let data = JSON.parse(response)[0];
                        if (data.status) {
                            self.setType("green");
                            self.setContent(data.message);
                            self.$$save.hide();
                            setTimeout(function () {
                                self.close();
                            }, 1000);
                        }
                    } catch (error) {
                        self.setType("red");
                        self.setContent(response);
                    }
                })
            });
        },
        buttons:{
            save: {
                text: "save",
                btnClass: "btn btn-success",
                action: function(){
                    $(".borrower_form_class").trigger("submit");
                    return false;
                }
            }
        },
        onOpenBefore: function(){
            $("body").css("overflow","d-none ");
        },
        onClose: function(){
            window.location.reload();
        }  
    });
});


