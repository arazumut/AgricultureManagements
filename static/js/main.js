/**
 * TarımHayTakip Ana JavaScript Dosyası
 */

// Document Ready Event
document.addEventListener('DOMContentLoaded', function() {
    console.log('TarımHayTakip JS yüklendi.');
    
    // Otomatik olarak kaybolan uyarılar
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            setTimeout(function() {
                bsAlert.close();
            }, 5000);
        });
    }, 100);

    // Form doğrulama
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Tooltip başlatma
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(function(tooltip) {
        new bootstrap.Tooltip(tooltip);
    });

    // Popover başlatma
    const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
    popovers.forEach(function(popover) {
        new bootstrap.Popover(popover);
    });

    // Dosya yükleme alanının özelleştirilmesi
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            const label = e.target.nextElementSibling;
            if (label && label.classList.contains('custom-file-label')) {
                label.textContent = fileName || 'Dosya seçin...';
            }
        });
    });
});

/**
 * Şifre göster/gizle işlevi
 * @param {string} inputId Şifre input alanının ID'si
 * @param {string} toggleId Göster/gizle düğmesinin ID'si
 */
function togglePasswordVisibility(inputId, toggleId) {
    const passwordInput = document.getElementById(inputId);
    const toggleButton = document.getElementById(toggleId);
    
    if (passwordInput && toggleButton) {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            toggleButton.innerHTML = '<i class="fas fa-eye-slash"></i>';
        } else {
            passwordInput.type = 'password';
            toggleButton.innerHTML = '<i class="fas fa-eye"></i>';
        }
    }
}

/**
 * Doğrulama mesajlarını göster
 * @param {string} formId Form ID'si
 * @param {Object} errors Hata nesnesi
 */
function showValidationErrors(formId, errors) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    // Önceki hataları temizle
    form.querySelectorAll('.is-invalid').forEach(function(el) {
        el.classList.remove('is-invalid');
    });
    form.querySelectorAll('.invalid-feedback').forEach(function(el) {
        el.remove();
    });
    
    // Yeni hataları ekle
    Object.keys(errors).forEach(function(key) {
        const input = form.querySelector(`[name="${key}"]`);
        if (input) {
            input.classList.add('is-invalid');
            
            const feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            feedback.textContent = errors[key];
            
            input.parentNode.appendChild(feedback);
        }
    });
}

/**
 * Ajax ile form gönderme
 * @param {string} formId Form ID'si
 * @param {string} url Hedef URL
 * @param {Function} successCallback Başarı callback fonksiyonu
 */
function submitFormAjax(formId, url, successCallback) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (typeof successCallback === 'function') {
                    successCallback(data);
                }
            } else if (data.errors) {
                showValidationErrors(formId, data.errors);
            }
        })
        .catch(error => {
            console.error('Form gönderme hatası:', error);
        });
    });
} 