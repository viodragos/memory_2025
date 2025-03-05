/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onMounted, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class TicheteDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            total_ore: 0, cost_manopera: 0, venit_manopera: 0,
            total_materiale_fisa: 0, total_materiale_pick: 0, discrepanta_materiale: 0,
            total_km: 0, cost_transport: 0,
            venit_total_facturi: 0, profit_total: 0,
        });

        onWillStart(async () => {
            const data = await this.orm.call("ticket.helpdesk", "get_dashboard_data", []);
            Object.assign(this.state, data);
        });

        onMounted(() => this.renderChart());
    }

    renderChart() {
        setTimeout(() => {
            const ctx = document.getElementById('cost_pie_chart');
            if (ctx) {
                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Manoperă', 'Materiale', 'Transport'],
                        datasets: [{
                            data: [
                                this.state.cost_manopera,
                                this.state.total_materiale_pick,
                                this.state.cost_transport
                            ],
                            backgroundColor: ['#003366', '#005599', '#0077cc'],
                        }],
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'bottom' },
                        },
                    },
                });
            }
        }, 100); // Dăm timp DOM-ului să-l creeze
    }
}

TicheteDashboard.template = "memory_tickets_dashboard.TicheteDashboard";

registry.category("actions").add("tichete_dashboard_action", TicheteDashboard);