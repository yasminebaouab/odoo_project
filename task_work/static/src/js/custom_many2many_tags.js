odoo.define('task_work.custom_many2many_tags', function (require) {
    "use strict";

    var core = require('web.core');
    var FormWidgetRegistry = require('web.form_widget_registry');

    if (!core) {
        console.error("'web.core' is not loaded.");
        return;
    }

    if (!FormWidgetRegistry) {
        console.error("'web.form_widget_registry' is not loaded.");
        return;
    }

    var FieldMany2ManyTags = FormWidgetRegistry.get('many2many_tags');
    var CustomMany2ManyTags = FieldMany2ManyTags.extend({
        _renderEdit: function () {
            this._super.apply(this, arguments);
            var self = this;
            this.$('a.o_tag_remove').each(function () {
                var $tag = $(this).parent();
                var recordID = $tag.data('id');
                var record = self.dataset.get_cache(self.record, recordID);
                if (record) {
                    var employeeModel = new Model('hr.employee');
                    employeeModel.query(['image_128']).filter([['id', '=', recordID]])
                        .all()
                        .then(function (employees) {
                            if (employees.length > 0) {
                                var image = employees[0].image_128;
                                var $img = $('<img>').attr('src', 'data:image/png;base64,' + image);
                                $img.addClass('circle-image'); // Add a CSS class
                                $tag.prepend($img);
                            }
                        });
                }
            });
        },
    });

    FormWidgetRegistry.add('custom_many2many_tags', CustomMany2ManyTags);

    console.log("JS Loaded");
});
