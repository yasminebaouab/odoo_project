odoo.define('task_work.widget_employee_image', function (require) {
    "use strict";

    var FieldMany2ManyTags = require('web.relational_fields').FieldMany2ManyTags;
    var core = require('web.core');

    var QWeb = core.qweb;

    FieldMany2ManyTags.include({
        _renderEdit: function () {
            var self = this;
            this._super.apply(this, arguments);

            this.$('.o_input').each(function () {
                var id = parseInt($(this).data('id'));
                var employee = self.record._cache.employee_ids.records.find(record => record.res_id === id);
                if (employee) {
                    var image = employee.data.image_small;
                    if (image) {
                        var $img = $('<img>').addClass('o_employee_image').attr('src', 'data:image/png;base64,' + image);
                        $(this).prepend($img);
                    }
                }
            });
        },
    });
});