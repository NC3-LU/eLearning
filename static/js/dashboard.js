$(document).ready(function () {
    const ctx = document.getElementById('dashboard');

    // TODO: Fetch values from the backend
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['RGPD', 'RGPD', 'RGPD', 'RGPD', 'RGPD', 'RGPD', 'RGPD', 'RGPD', 'RGPD'],
            datasets: [{
                label: 'score',
                data: [12, 19, 3, 5, 2, 3, 1, 15, 6],
                borderRadius: 30,
                borderSkipped: false,
                backgroundColor: '#AFDFFF',
                barPercentage: 0.6
            }]
        },
        options: {
            scales: {
                y: {
                    display: false,
                },
                x: {
                    grid: {
                        display: false,
                    },
                    border: {
                        display: false,
                    },
                    ticks: {
                        font: {
                            weight: 'bold',
                        }
                    }
                },
            },
            plugins: {
                legend: {
                    display: false
                }
            },
        }
    });

    // TODO: Fetch values from the backend
    for (const i in [1,2,3,4,5]) {
        var progress = (5 - i) * 25;
        let ctx1 = document.getElementById('progress' + i)
        new Chart(ctx1, {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [{
                    data: [100 - progress, progress],
                    backgroundColor: ['#006ED3', '#FFFFFF'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                cutout: "85%",
                animations: {
                    startAngle: {
                      from: Math.PI * 2
                    },
                    endAngle: {
                      from: Math.PI * 2
                    }
                },
                plugins: {
                    tooltip: {
                        enabled: false
                    }
                },
            }
        });
    }

});
