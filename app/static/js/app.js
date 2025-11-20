// Pet Care Advisor - Frontend JavaScript

class PetCareApp {
    constructor() {
        this.initializeEventListeners();
        this.loadStoredData();
    }

    initializeEventListeners() {
        // Form validation
        document.addEventListener('DOMContentLoaded', () => {
            this.setupFormValidation();
            this.setupTooltips();
        });

        // Auto-save form data
        this.setupAutoSave();
    }

    setupFormValidation() {
        const forms = document.querySelectorAll('.needs-validation');
        
        forms.forEach(form => {
            form.addEventListener('submit', (event) => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    }

    setupTooltips() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(
            document.querySelectorAll('[data-bs-toggle="tooltip"]')
        );
        
        tooltipTriggerList.map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    setupAutoSave() {
        // Auto-save form data as user types
        const inputs = document.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                this.saveFormData();
            });
        });
    }

    saveFormData() {
        const formData = {};
        const inputs = document.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            if (input.type === 'checkbox') {
                if (input.checked) {
                    if (!formData[input.name]) {
                        formData[input.name] = [];
                    }
                    formData[input.name].push(input.value);
                }
            } else if (input.value.trim() !== '') {
                formData[input.name] = input.value;
            }
        });

        localStorage.setItem('petFormData', JSON.stringify(formData));
    }

    loadStoredData() {
        const storedData = localStorage.getItem('petFormData');
        
        if (storedData) {
            const formData = JSON.parse(storedData);
            
            Object.keys(formData).forEach(key => {
                const input = document.querySelector(`[name="${key}"]`);
                
                if (input) {
                    if (input.type === 'checkbox') {
                        if (Array.isArray(formData[key]) && formData[key].includes(input.value)) {
                            input.checked = true;
                        }
                    } else {
                        input.value = formData[key];
                    }
                }
            });
        }
    }

    // Utility functions
    showLoader() {
        const loader = document.createElement('div');
        loader.className = 'loader-overlay';
        loader.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary mb-3" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p>Processing your request...</p>
            </div>
        `;
        document.body.appendChild(loader);
    }

    hideLoader() {
        const loader = document.querySelector('.loader-overlay');
        if (loader) {
            loader.remove();
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show`;
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '9999';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
}

// Diagnostic utilities
class DiagnosticUtils {
    static formatConfidence(confidence) {
        return Math.round(confidence * 100) + '%';
    }

    static getConfidenceClass(confidence) {
        if (confidence >= 0.8) return 'success';
        if (confidence >= 0.6) return 'warning';
        if (confidence >= 0.4) return 'info';
        return 'secondary';
    }

    static formatSeverity(severity) {
        const severityMap = {
            'low': { class: 'success', icon: 'fa-check-circle' },
            'medium': { class: 'warning', icon: 'fa-exclamation-triangle' },
            'high': { class: 'danger', icon: 'fa-exclamation-circle' },
            'critical': { class: 'danger', icon: 'fa-times-circle' }
        };
        
        return severityMap[severity] || { class: 'secondary', icon: 'fa-question-circle' };
    }

    static generateShareableReport(diagnosisData, results) {
        const report = {
            pet: {
                name: diagnosisData.name,
                species: diagnosisData.species,
                age: diagnosisData.age,
                breed: diagnosisData.breed
            },
            assessment_date: new Date().toISOString(),
            symptoms: diagnosisData.symptoms,
            results: {
                emergency: results.emergency,
                conditions: results.conditions?.map(c => ({
                    name: c.condition.name,
                    confidence: c.confidence,
                    severity: c.condition.severity
                })) || [],
                recommendations: results.recommendations
            },
            disclaimer: 'This assessment is for informational purposes only. Consult with a qualified veterinarian for professional medical advice.'
        };

        return JSON.stringify(report, null, 2);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    const app = new PetCareApp();
    window.petCareApp = app;
    window.DiagnosticUtils = DiagnosticUtils;
});

// Loader CSS (inject into head)
const loaderCSS = `
    <style>
    .loader-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
    }
    </style>
`;

document.head.insertAdjacentHTML('beforeend', loaderCSS);
