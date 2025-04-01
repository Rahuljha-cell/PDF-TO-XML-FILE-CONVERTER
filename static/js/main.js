document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // File upload drag and drop functionality
    const uploadZone = document.querySelector('.file-upload-zone');
    if (uploadZone) {
        const fileInput = document.getElementById('pdf_file');
        
        uploadZone.addEventListener('click', function() {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', function() {
            if (fileInput.files.length > 0) {
                const fileName = fileInput.files[0].name;
                // Update the upload zone to show the selected file
                uploadZone.querySelector('.upload-text').textContent = `Selected: ${fileName}`;
                
                // Submit the form automatically when a file is selected
                if (document.querySelector('#autoSubmit').checked) {
                    // Get the PDF upload form specifically by looking for a form that contains pdf_file
                    const uploadForm = document.querySelector('form[enctype="multipart/form-data"]');
                    if (uploadForm) {
                        // Use submit button click instead of form.submit() to trigger validation
                        const submitBtn = document.getElementById('pdfSubmitBtn');
                        if (submitBtn) {
                            submitBtn.click();
                        } else {
                            // Fallback to traditional submit if button not found
                            uploadForm.submit();
                        }
                    }
                }
            }
        });
        
        // Drag and drop events
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadZone.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            uploadZone.classList.add('dragover');
        }
        
        function unhighlight() {
            uploadZone.classList.remove('dragover');
        }
        
        uploadZone.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                // Check if file is PDF
                const file = files[0];
                if (file.type === 'application/pdf') {
                    fileInput.files = files;
                    uploadZone.querySelector('.upload-text').textContent = `Selected: ${file.name}`;
                    
                    // Submit the form automatically when a file is dropped
                    if (document.querySelector('#autoSubmit').checked) {
                        // Get the PDF upload form specifically
                        const uploadForm = document.querySelector('form[enctype="multipart/form-data"]');
                        if (uploadForm) {
                            // Use submit button click instead of form.submit() to trigger validation
                            const submitBtn = document.getElementById('pdfSubmitBtn');
                            if (submitBtn) {
                                submitBtn.click();
                            } else {
                                // Fallback to traditional submit if button not found
                                uploadForm.submit();
                            }
                        }
                    }
                } else {
                    alert('Please upload a PDF file.');
                }
            }
        }
    }
    
    // Copy XML content to clipboard
    const copyXmlBtn = document.getElementById('copyXmlBtn');
    if (copyXmlBtn) {
        copyXmlBtn.addEventListener('click', function() {
            const xmlContent = document.getElementById('xmlContent');
            if (xmlContent) {
                navigator.clipboard.writeText(xmlContent.textContent)
                    .then(() => {
                        // Change button text temporarily
                        const originalText = copyXmlBtn.textContent;
                        copyXmlBtn.textContent = 'Copied!';
                        setTimeout(() => {
                            copyXmlBtn.textContent = originalText;
                        }, 2000);
                    })
                    .catch(err => {
                        console.error('Failed to copy XML: ', err);
                        alert('Failed to copy XML to clipboard.');
                    });
            }
        });
    }
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        setTimeout(function() {
            alerts.forEach(alert => {
                // Create fade-out effect
                alert.style.transition = 'opacity 1s';
                alert.style.opacity = '0';
                
                // Remove alert after fade
                setTimeout(function() {
                    alert.remove();
                }, 1000);
            });
        }, 5000);
    }
});
