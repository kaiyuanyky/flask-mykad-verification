var allLandmarksMatchingPercent = $('#allLandmarksMatchingPercent').attr('value').slice(1,-1).split(' ');
var allSecurityFeaturesPercent = $('#allSecurityFeaturesPercent').attr('value').slice(1,-1).split(' ');
var allFraudsPercent = $('#allFraudsPercent').attr('value').slice(1,-1).split(' ');

var eachThresholdValue = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 10, 10, 10];

var all_detections_label = ["Security Feature Detection", "Fraud Detection", "Landmark Detection"]

var landmarks_type_label = ["Front MyKad (Full)", "Front MyKad (Defect)", "Rear MyKad (Full)", "Rear MyKad (Defect)"];
var landmarks_type_number = [16, 12, 13, 4];

var landmarks_label = ["IC Logo", "MyKad Logo", "Malaysian Flag", "MSC Logo", "Security Chip", "Hibiscus", "Microprint", "Coat of Arms Logo", "Touch \'n Go Logo", "ATM Logo", "Signature", "Chip", "Petronas Twin Towers", "King\'s Crown", "Malaysia Word"];
var landmarks_point_threshold = [200, 80, 80, 30, 70, 40, 80, 30, 60, 40, 50, 20, 45, 65, 10];
var landmarks_average_accuracy = [55.56, 77.78, 88.89, 33.33, 33.33, 44.44, 11.11, 68.89, 72.41, 66.67, 46.67, 50.56, 37.91, 47.78, 44.45];
var landmarks_detection_ratio = [100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00, 100.00];

var landmarks_category_label = ["Pattern-Type (Front)", "OCR-Type (Front)", "Pattern-Type (Rear)", "OCR-Type (Rear)"];
var landmarks_category_number = [7, 4, 8, 1];
var thresholds_label = ["Blurriness", "Individual Matching of Landmark", "Overall Landmark Score", "Overall Security Feature Score", "Overall Fraud Score"];
var thresholds_value = [25.00, 20.00, 50.00, 50.00, 50.00];

var security_features_label = ["Microprint Existence", "Microprint Matching"]
var security_features_value = [true, true]
var frauds_label = ["Face Existence", "MyKads are a Pair", "Front NRIC is Valid", "Rear NRIC is Valid", "Name has Value", "Address has Value", "Front MyKad is not blurred", "Rear MyKad is not blurred"]
var frauds_value = [true, true, true, true, true, true, true, true]

function chartLandmarkTypeNumber() {
    new Chart("chart-landmark-type-number", {
        type: "pie",
        data: {
            labels: this.landmarks_type_label,
            datasets: [{
                data: this.landmarks_type_number,
                backgroundColor: this.getColors(this.landmarks_type_label.length)
            }]
        },
        options: {
            legend: {display: true},
            title: {
                display: true,
                fontSize: 36,
                text: "Types of MyKad"
            }
        }
    });
}

function chartLandmarkCategory() {
    new Chart("chart-landmark-category", {
        type: "polarArea",
        data: {
            labels: this.landmarks_category_label,
            datasets: [{
                data: this.landmarks_category_number,
                backgroundColor: this.getColors(this.landmarks_category_label.length)
            }]
        },
        options: {
            legend: {display: true},
            title: {
                display: true,
                fontSize: 36,
                text: "Categories of Landmarks"
            }
        }
    });
}

function chartAllThreshold() {
    new Chart("chart-all-threshold", {
        type: "polarArea",
        data: {
            labels: this.thresholds_label,
            datasets: [{
                data: this.thresholds_value,
                backgroundColor: this.getColors(this.thresholds_label.length)
            }]
        },
        options: {
            legend: {display: true},
            title: {
                display: true,
                fontSize: 36,
                text: "Threshold Values"
            }
        }
    });
}

function chartThresholdDenominator() {
    new Chart("chart-threshold-denominator", {
        type: "line",
        data: {
            labels: this.landmarks_label,
            datasets: [{
                label: "Denominator Values",
                data: this.landmarks_point_threshold,
                fill: false,
                tension: 0.3,
                borderColor: 'rgb(0,255,0)',
                pointHoverBackgroundColor: '#fff'
            }]
        },
        options: {
            legend: {display: true},
            title: {
                display: true,
                fontSize: 36,
                text: "Threshold Denominator"
            },
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 200
                    }
                }]
            }
        }
    });
}

function chartEachThreshold() {
    new Chart("chart-each-threshold", {
        type: "polarArea",
        data: {
            labels: this.landmarks_label,
            datasets: [{
                label: "Threshold Values",
                data: this.eachThresholdValue,
                fill: false,
                tension: 0.3,
                backgroundColor: this.getColors(this.landmarks_label.length),
                pointHoverBackgroundColor: '#fff'
            }]
        },
        options: {
            legend: {display: true},
            title: {
                display: true,
                fontSize: 36,
                text: "Each Landmark Threshold"
            }
        }
    });
}

function chartLandmarkRatio() {
    new Chart("chart-landmark-ratio", {
        type: "bar",
        data: {
            labels: this.landmarks_label,
            datasets: [{
                data: this.landmarks_detection_ratio,
                backgroundColor: this.getColors(this.landmarks_label.length),
                label: 'Detection Percentage'
            }]
        },
        options: {
            legend: {display: true},
            title: {
                display: true,
                fontSize: 36,
                text: "Detection of Each Landmark"
            },
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }]
            }
        }
    });
}

function chartLandmarkDetection() {
    new Chart("chart-landmark-detection", {
        type: "bar",
        data: {
            labels: this.landmarks_label,
            datasets: [{
                data: this.landmarks_average_accuracy,
                backgroundColor: this.getColors(this.landmarks_label.length),
                label: 'Landmark Accuracy'
            },
            {
                data: this.eachThresholdValue,
                type: 'line',
                label: 'Landmark Threshold'
            }]
        },
        options: {
            legend: {display: true},
            title: {
                display: true,
                fontSize: 36,
                text: "Accuracy of Each Landmark Detection"
            },
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 90
                    }
                }]
            }
        }
    });
}

function chartSecurityFeatureDetection() {
    new Chart("chart-security-feature-detection", {
        type: "doughnut",
        data: {
            labels: this.security_features_label,
            datasets: [{
                data: this.security_features_value,
                backgroundColor: this.getColors(this.security_features_label.length),
            }]
        },
        options: {
            legend: {display: true},
            title: {
                display: true,
                fontSize: 36,
                text: "Security Feature Detection"
            }
        }
    });
}

function chartFraudDetection() {
    new Chart("chart-fraud-detection", {
        type: "doughnut",
        data: {
            labels: this.frauds_label,
            datasets: [{
                data: this.frauds_value,
                backgroundColor: this.getColors(this.frauds_label.length),
            }]
        },
        options: {
            legend: {display: true},
            title: {
                display: true,
                fontSize: 36,
                text: "Fraud Detection"
            }
        }
    });
}

function chartOverallVerification() {
    new Chart("chart-overall-verification", {
        type: "radar",
        data: {
            labels: this.all_detections_label,
            datasets: [{
                data: [
                    calculateAverage(allSecurityFeaturesPercent), 
                    calculateAverage(allFraudsPercent),
                    calculateAverage(allLandmarksMatchingPercent)
                ],
                backgroundColor: "rgb(0, 255, 0, 0.2)",
                pointBackgroundColor: 'rgb(0, 255, 0)',
                pointHoverBackgroundColor: '#fff'
            }]
        },
        options: {
            legend: {display: false},
            title: {
                display: true,
                fontSize: 36,
                text: "Average Verification Score"
            },
            scale: {
                ticks: {
                    beginAtZero: true,
                    max: 80,
                    min: 35,
                    stepSize: 15
                }
            }
        }
    });
}

function getColors(val) {
    colors = new Array(val)

    for(let i=0; i<val; i++)
        colors[i] = this.getRandomRGB();

    return colors
}

function getRandomRGB() {
    let num = Math.round(0xffffff * Math.random());

    let r = num >> 16;
    let g = num >> 8 & 255;
    let b = num & 255;

    return 'rgb(' + r + ', ' + g + ', ' + b + ')';
}

function calculateAverage(arr) {
    let redundant = 0;
    for (let i=0; i<arr.length; i++) {
        if(arr[i] == "") {
            arr[i] = "0";
            redundant += 1;
        }
        else
            arr[i] = arr[i].split('.')[0];
        arr[i] = parseInt(arr[i]);
    }
    let sum = arr.reduce((a, b) => a + b, 0);
    return sum / (arr.length - redundant);
}

// Create all the charts/graphs
window.addEventListener('DOMContentLoaded', (e) => {
    this.chartLandmarkTypeNumber();
    this.chartLandmarkCategory();
    this.chartAllThreshold();
    this.chartThresholdDenominator();
    this.chartEachThreshold();
    this.chartLandmarkRatio();
    this.chartLandmarkDetection();
    this.chartSecurityFeatureDetection();
    this.chartFraudDetection();
    this.chartOverallVerification();
});