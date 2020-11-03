odoo.define('systray_badge', function(require) {
    var Widget = require('web.Widget');
    var SystrayMenu = require('web.SystrayMenu');
    var UserMenu = require('web.UserMenu');
    var session = require('web.session');
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var qweb = core.qweb;
    var _t = core._t;

    var SystrayBadge = Widget.extend({
        template: 'SystrayBadge',
        events: {
        },
        start: function() {
            var res = this._super.apply(this, arguments);
            this.loadMessage().then(this.update.bind(this));
            return res;
        },
        loadMessage: function() {
            return this._rpc({
                model: 'systray.badge',
                method: 'get_message',
            });
        },
        update: function(message) {
            this.$('#systray-badge').text(message);
        },
    });

    SystrayMenu.Items.push(SystrayBadge);

    return {
        Menu: SystrayBadge,
    };
});
