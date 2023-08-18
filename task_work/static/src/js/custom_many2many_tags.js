odoo.define('task_work.custom_many2many_tags', function (require) {
    "use strict";

    var relational_fields = require('web.relational_fields');
    var field_registry = require('web.field_registry');
    var session = require('web.session');
//    var WebClient = require('web.WebClient');
    var core = require('web.core');
    var qweb = core.qweb;

    var FieldMany2ManyTags = relational_fields.FieldMany2ManyTags;

    var CustomMany2ManyTags = FieldMany2ManyTags.extend({
          init: function () {
            this._super.apply(this, arguments);
            this.tag_template = "CustomMany2ManyTags";
          },

          _renderTags: function () {
                var self = this;
                var $tags = this._super.apply(this, arguments);
                var employeeModel = new WebClient.Model('hr.employee');

                this._rpc({
                    model: 'hr.employee',
                    method: 'search_read',
                    domain: [['id', 'in', this.value.res_ids]],
                    fields: ['image_128'],
                }).then(function (employees) {
                    employees.forEach(function (employee) {
                        var $tag = $tags.find('a[data-id="' + employee.id + '"]').parent();
                        if ($tag.length) {
                            var $img = $('<img>')
                                .addClass('rounded-circle')
                                .attr('src', 'data:image/png;base64,' + employee.image_128);
                            $tag.prepend($img);
                        }
                    });
                });

                return $tags;
            },
    });

    field_registry.add('custom_many2many_tags', CustomMany2ManyTags);
    console.log('jssssssssss')
});

