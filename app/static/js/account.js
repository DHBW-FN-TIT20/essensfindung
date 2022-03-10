function delete_account() {
    $.post({
        url: "/delete/",
        success: () => {
            $(location).prop('href', '/')
        }
    });
}