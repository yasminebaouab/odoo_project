odoo.define('crnd_web_float_full_time_widget.FullFloatTime', function (require) {
    "use strict";

    var registry = require('web.field_registry');
    var basic_fields = require('web.basic_fields');
    var FieldUtils = require('web.field_utils');
    var core = require('web.core');

    var _t = core._t;

    function formatFloatFullTime(value) {
        var total_sec = Math.floor(value);

        var hours = Math.floor(total_sec / 3600);
        var minutes = Math.floor((total_sec % 3600) / 60);

        var pattern = '%02d:%02d';

        return _.str.sprintf(pattern, hours, minutes);
    }

    FieldUtils.format.float_time_duration = formatFloatFullTime;

    var FloatTimeDuration = basic_fields.FieldFloat.extend({
        formatType: 'float_time_duration',

        init: function () {
            this._super.apply(this, arguments);
            this.time_only = true; // Always set to true
        },

        _formatValue: function (value) {
            return FieldUtils.format[this.formatType](value);
        },

        _parseValue: function (value) {
            return FieldUtils.parse[this.formatType](value);
        },
    });

    registry.add('float_time_duration', FloatTimeDuration);

    return {
        FloatTimeDuration: FloatTimeDuration,
    };
});
