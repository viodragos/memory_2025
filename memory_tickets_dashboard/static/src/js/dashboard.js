/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class TicheteDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({ total: 0, deschise: 0, in_curs: 0, finalizate: 0 });

        onWillStart(async () => {
            const data = await this.orm.call("helpdesk.ticket", "get_dashboard_data", []);
            Object.assign(this.state, data);
        });
    }
}
TicheteDashboard.template = "memory_tickets_dashboard.TicheteDashboard";

registry.category("actions").add("tichete_dashboard_action", TicheteDashboard);