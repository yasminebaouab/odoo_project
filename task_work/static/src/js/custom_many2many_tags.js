odoo.define('project.task.work.custom_many2many_tags', function (require) {
    "use strict";

    var core = require('web.core');
    var FieldMany2ManyTags = core.form_widget_registry.get('many2many_tags');

    var CustomMany2ManyTags = FieldMany2ManyTags.extend({
        _renderEdit: function () {
            this._super.apply(this, arguments);
            var self = this;
            this.$('a.o_tag_remove').each(function () {
                var $tag = $(this).parent();
                var recordID = $tag.data('id');
                var record = self.dataset.get_cache(self.record, recordID);
                if (record) {
                    var employeeModel = new Model('hr.employee');  // Replace 'hr.employee' with your actual model name
                    employeeModel.query(['image_128']).filter([['id', '=', recordID]])
                        .all()
                        .then(function (employees) {
                            if (employees.length > 0) {
                                var image = employees[0].image_128;
                                var $img = $('<img>').attr('src', 'data:image/png;base64,' + image);
                                $tag.prepend($img);
                            }
                        });
                }
            });
        },
    });

    core.form_widget_registry.add('custom_many2many_tags', CustomMany2ManyTags);
});

    core.form_widget_registry.add('custom_many2many_tags', CustomFieldMany2ManyTags);
});
