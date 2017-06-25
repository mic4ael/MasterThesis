(function () {
    var fieldDialogTemplate =
        '<div class="modal fade field-dialog" tabindex="-1"                               ' +
        '     :data-field-type="fieldType"                                                ' +
        '     role="dialog">                                                              ' +
        '    <div class="modal-dialog" role="document">                                   ' +
        '        <div class="modal-content">                                              ' +
        '            <div class="modal-header">                                           ' +
        '                <button type="button" class="close"                              ' +
        '                        data-dismiss="modal">                                    ' +
        '                    <span aria-hidden="true">&times;</span>                      ' +
        '                </button>                                                        ' +
        '                <h4 class="modal-title">                                         ' +
        '                    Nowe pole type: {{ fieldType }}                              ' +
        '                </h4>                                                            ' +
        '            </div>                                                               ' +
        '            <div class="modal-body">                                             ' +
        '                <div class="form-group">                                         ' +
        '                   <label for="field-label">Etykieta</label>                     ' +
        '                   <input class="form-control" type="text"                       ' +
        '                          id="field-label">                                      ' +
        '                </div>                                                           ' +
        '                <div v-if="fieldCanHavePlaceholder(fieldType)"                   ' +
        '                     class="form-group">                                         ' +
        '                   <label for="field-placeholder">                               ' +
        '                       Placeholder                                               ' +
        '                   </label>                                                      ' +
        '                   <input v-if="fieldType != \'paragraph\'"                      ' +
        '                          class="form-control" type="text"                       ' +
        '                          id="field-placeholder">                                ' +
        '                   <textarea v-if="fieldType == \'paragraph\'"                   ' +
        '                          class="form-control"                                   ' +
        '                          id="field-placeholder">                                ' +
        '                   </textarea>                                                   ' +
        '                </div>                                                           ' +
        '                <div v-if="fieldType != \'paragraph\' && fieldType != \'submit\'"' +
        '                     class="checkbox">                                           ' +
        '                   <label>                                                       ' +
        '                       <input id="field-required"                                ' +
        '                              type="checkbox">Pole obowiązkowe                   ' +
        '                   </label>                                                      ' +
        '                </div>                                                           ' +
        '            </div>                                                               ' +
        '            <div class="modal-footer">                                           ' +
        '                <button type="button" class="btn btn-default"                    ' +
        '                        data-dismiss="modal">Zamknij</button>                    ' +
        '                <button type="button"                                            ' +
        '                        class="btn btn-primary btn-approve">                     ' +
        '                    Dodaj                                                        ' +
        '                </button>                                                        ' +
        '            </div>                                                               ' +
        '        </div>                                                                   ' +
        '    </div>                                                                       ' +
        '</div>                                                                           ';

    var newFieldDialogComponent = Vue.component('new-field-dialog', {
        template: fieldDialogTemplate,
        props: ['fieldType'],
        methods: {
            fieldCanHavePlaceholder: function(fieldType) {
                return ['select', 'checkbox', 'date', 'submit'].indexOf(fieldType) === -1;
            }
        }
    });

    var availableTypes = ['text', 'number', 'mail', 'date', 'checkbox',
                          'paragraph', 'select', 'submit'],
        fieldsButtons = $('.forms-fields .btn-group .new-field'),
        formsPreviewVueInstance = new Vue({
            el: '.forms-template',
            data: {
                fields: JSON.parse($('.forms-preview .fields').val())
            },
            methods: {
                openNewFieldDialog: function (event) {
                    var $field = $(event.target);
                    var fieldSelector = 'div.modal[data-field-type="' + $field.data('field-type') + '"]';

                    $(fieldSelector).modal();
                },
                removeField: function (event) {
                    var $target = $(event.target),
                        $inputField = $target.closest('.field-remove').prev().find('.form-control'),
                        fieldIndexToRemove = $inputField.data('field-tmp-id');

                    this.$data.fields.splice(fieldIndexToRemove, 1);
                }
            },
            components: {
                'new-field-dialog': newFieldDialogComponent
            }
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

    $('div.modal[data-field-type] button.btn-approve').on('click', function (evt) {
        var $modal = $(this).closest('div.modal'),
            formFields = $modal.find('input.form-control, input[type=checkbox], textarea.form-control'),
            newField = {'type': $modal.data('field-type'), 'id': null};

        $.each(formFields, function (item, obj) {
            var $obj = $(obj);
            if ($obj.attr('id') == 'field-label') {
                newField['label'] = $obj.val();
                $obj.val('');
            } else if ($obj.attr('id') == 'field-placeholder') {
                newField['placeholder'] = $obj.val();
                $obj.val('');
            } else if ($obj.attr('id') == 'field-required') {
                newField['required'] = $obj.is(':checked');
                $obj.get(0).checked = false;
            }
        });

        formsPreviewVueInstance.$data.fields.push(newField);
        $modal.modal('hide');
    });

    $('.save-form').on('click', function (evt) {
        evt.preventDefault();

        var $this = $(this),
            csrfToken = $('.forms-template').data('csrf-token');

        if (formsPreviewVueInstance.$data.fields.length == 0) {
            return;
        }

        $.ajax({
            url: $this.data('href'),
            method: $this.data('method'),
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            },
            data: {
                fields: JSON.stringify(formsPreviewVueInstance.$data.fields)
            },
            success: function (data) {
                if (data.success) {
                    formsPreviewVueInstance.$data.fields = JSON.parse(data.fields);
                }
            }
        });
    });
})();
