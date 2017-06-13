(function () {
    var availableTypes = ['text', 'number', 'mail', 'date', 'checkbox', 'paragraph', 'select'],
        fieldsButtons = $('.forms-fields .btn-group .new-field'),
        formsPreviewVueInstance = new Vue({
            el: '.forms-preview'
        });

    fieldsButtons.on('click', function (evt) {
        evt.preventDefault();

        var $this = $(this),
            fieldType = $this.data('field-type');

        if (availableTypes.indexOf(fieldType) === -1) {
            console.debug('Wybrano niewspierany typ pola');
            return;
        }
    });
})();
