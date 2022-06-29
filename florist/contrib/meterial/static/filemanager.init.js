// 通过自定义回调实现相对路径。
// REF: https://github.com/psolom/RichFilemanager/issues/222

$('.fm-container').richFilemanager({
    callbacks: {
        beforeSelectItem: function (resourceObject, url) {
            return resourceObject.attributes.path;
        },
    }
});