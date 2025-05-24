/**
 * HarmonySchool Dashboard Charts
 * Clean and simple chart configuration
 */

function initDashboardCharts(categoryData, priorityData) {
    // Category Chart (Pie)
    if (document.getElementById('incidentsByCategoryChart')) {
        const ctx = document.getElementById('incidentsByCategoryChart').getContext('2d');
        
        // Simple color palette that matches your UI
        const colors = [
            '#7fc4f6', // Light blue
            '#ff94a7', // Light pink
            '#ffcc5c', // Yellow
            '#96d6c7', // Light green
            '#a58bcc', // Purple
            '#ff8c79'  // Coral
        ];
        
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: categoryData.labels,
                datasets: [{
                    data: categoryData.values,
                    backgroundColor: colors,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            boxWidth: 15,
                            padding: 15,
                            font: {
                                size: 12
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Priority Chart (Bar)
    if (document.getElementById('incidentsByPriorityChart')) {
        const ctx = document.getElementById('incidentsByPriorityChart').getContext('2d');
        
        // Priority color mapping
        const priorityColors = {
            'faible': '#96d6c7',    // Light green
            'moyenne': '#7fc4f6',   // Light blue
            'elevee': '#ffcc5c',    // Yellow
            'critique': '#ff8c79'   // Coral
        };
        
        // Priority labels translation
        const priorityLabels = {
            'faible': 'Faible',
            'moyenne': 'Moyenne',
            'elevee': 'Élevée',
            'critique': 'Critique'
        };
        
        // Format labels
        const displayLabels = priorityData.labels.map(label => 
            priorityLabels[label] || label
        );
        
        // Create colors array based on priority keys
        const barColors = priorityData.labels.map(label => 
            priorityColors[label] || '#a58bcc'
        );
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: displayLabels,
                datasets: [{
                    data: priorityData.values,
                    backgroundColor: barColors,
                    borderWidth: 0,
                    barPercentage: 0.6,
                    categoryPercentage: 0.7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }
}