//odoo.define('task_work.custom_task_work_renderer', function (require) {
//    console.log("helllo color")
//    var ListView = require('web.ListView');
//    var ListRenderer = require('web.ListRenderer');
//
//    ListView.include({
//        render_buttons: function () {
//            var self = this;
//            this._super.apply(this, arguments);
//
//            // Récupérer tous les enregistrements dans la liste
//            var records = this.state.data;
//
//            // Générer des couleurs aléatoires pour chaque work_group_id
//            var colorMap = {};
//            for (var id in records) {
//                var workGroupId = records[id].data.work_group_id;
//                if (!(workGroupId in colorMap)) {
//                    colorMap[workGroupId] = self.generateRandomColor();
//                }
//            }
//
//            // Appliquer les couleurs aux enregistrements
//            this.$el.find('.oe_kanban_color').each(function () {
//                var workGroupId = $(this).data('work_group_id');
//                if (workGroupId in colorMap) {
//                    $(this).css('background-color', colorMap[workGroupId]);
//                }
//            });
//        },
//
//        // Fonction pour générer une couleur aléatoire
//        generateRandomColor: function () {
//            var letters = '0123456789ABCDEF';
//            var color = '#';
//            for (var i = 0; i < 6; i++) {
//                color += letters[Math.floor(Math.random() * 16)];
//            }
//            return color;
//        },
//    });
//});