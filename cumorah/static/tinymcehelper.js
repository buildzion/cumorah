

document.body.addEventListener("initialize_tinymce", function(evt){
        tinymce.remove();
        tinymce.init({
        selector: evt.detail.selector,
        license_key: 'gpl',
        menubar: '',
        toolbar: 'undo redo | bold italic | bullist numlist | link emoticons',
        plugins: [
            'link', 'emoticons', 'lists'
        ]
    })
});
