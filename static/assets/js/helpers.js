"use strict";

function retainActiveTabOnPageReload() {
    $('#staticTab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

    // store the currently selected tab in the hash value
    $("ul.nav > li > a").on("shown.bs.tab", function (e) {
        window.location.hash = $(e.target).attr("href").substr(1);
    });

    // on load of the page: switch to the currently selected tab
    const hash = window.location.hash;
    $('#staticTab a[href="' + hash + '"]').tab('show');
}

//retainActiveTabOnPageReload();

// Reload window
function reloadWindow() {
    setTimeout(function () {
        window.location.reload()
    }, 1000);
}


function ajaxGet(title, url, columnClass, containerFluid) {
    $.confirm({
        closeIcon: true,
        title: title,
        content: "url:" + url,
        columnClass: columnClass,
        containerFluid: containerFluid,
        type: "dark",
        offsetTop: 1,
        //offsetBottom: 1,
        onContentReady: function () {

        },
        onOpenBefore: function () {
            $("body").addClass("no-scroll");
        },
        onClose: function () {
            window.location.reload();
        },
        buttons: {
            close: {
                text: "Close",
                isHidden: true,
                action: function () {
                    return false;
                }
            }
        }
    });
}

function ajaxConfirm(title, url, content) {
    $.confirm({
        type: "dark",
        title: title,
        closeIcon: true,
        content: content,
        buttons: {
            confirm: {
                text: "Confirm",
                btnClass: "btn btn-dark",
                action: function () {
                    let self = this;
                    self.showLoading();
                    $.ajax({
                        url: url,
                        type: "GET",
                    }).done(function (response) {
                        self.hideLoading();
                        try {
                            let data = JSON.parse(response);
                            if (data.status) {
                                self.setType("dark");
                                self.setTitle('Success');
                                self.setContent(data.message);
                                self.$$confirm.hide();
                                setTimeout(function () {
                                    self.close();
                                }, 900);
                            } else {
                                self.setType("red");
                                self.setContent(data.message);
                            }
                        } catch (error) {
                            self.setContent(response);
                            self.setType("red");
                        }
                    });
                    return false;
                }
            }
        },
        onOpenBefore: function () {
            $("body").css('overflow', 'hidden');
        },
        onClose: function () {
            window.location.reload();
        }
    });
}

function datePickerSelector() {
    $('.pickadate').datepicker({
        format: 'yyyy-mm-dd',
        startView: 0,
        todayBtn: false,
        clearBtn: true,
        autoclose: true,
        todayHighlight: true
    });
}

function select2Selector() {
    $('.select2').select2();
}

function ajaxPost(title, url, columnClass, containerFluid, formSelector, buttonsColumnClass) {
    $.confirm({
        title: title,
        type: "dark",
        closeIcon: true,
        columnClass: columnClass,
        containerFluid: containerFluid,
        content: "url: " + url,
        offsetTop: 1,
        offsetBottom: 1,
        useBootstrap: true,
        typeAnimated: true,
        onContentReady: function () {
            let self = this;

            $(".jconfirm-buttons").addClass(buttonsColumnClass);

            $(document).on("submit", formSelector, function (e) {
                e.preventDefault();
                let $form = $(this);
                let formData = new FormData($form[0]);
                self.showLoading();
                $.ajax({
                    url: $form.attr('action'),
                    type: $form.attr('method'),
                    data: formData,
                    contentType: false,
                    processData: false,
                    cache: false
                }).done((response) => {
                    self.hideLoading();
                    try {
                        let data = JSON.parse(response);
                        if (data.status) {
                            self.setType("blue");
                            self.setTitle('Success');
                            self.setContent(data.message);
                            self.$$submit.hide();
                            setTimeout(function () {
                                self.close();
                            }, 900);
                        } else {
                            self.setType("red");
                            self.setTitle('Failed');
                            self.setContent(data.message);
                        }
                    } catch (error) {
                        //datePickerSelector()
                        // select2Selector()
                        self.setContent(response);
                        self.setType("red");
                        self.$$submit.show();
                    }
                })
            });
        },
        onClose: function () {
            window.location.reload();
        },
        onOpenBefore: function () {
            $("body").addClass("no-scroll");
        },
        buttons: {
            submit: {
                text: 'SUBMIT',
                btnClass: '',
                action: function () {
                    $(formSelector).trigger("submit");
                    return false;
                }
            }
        }
    });
}
