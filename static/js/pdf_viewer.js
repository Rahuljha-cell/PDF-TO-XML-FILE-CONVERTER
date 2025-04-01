document.addEventListener('DOMContentLoaded', function() {
    const pdfViewer = document.getElementById('pdfViewer');
    const pdfFileInput = document.getElementById('pdf_file');
    
    if (pdfViewer && pdfFileInput) {
        // Initialize PDF.js
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.worker.min.js';
        
        // Initialize the PDF viewer when a file is selected
        pdfFileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file && file.type === 'application/pdf') {
                const fileReader = new FileReader();
                
                fileReader.onload = function() {
                    const typedArray = new Uint8Array(this.result);
                    renderPdf(typedArray);
                };
                
                fileReader.readAsArrayBuffer(file);
            }
        });
        
        // Check if there is already a PDF displayed (from previous conversion)
        if (document.getElementById('currentConversionId')) {
            const conversionId = document.getElementById('currentConversionId').value;
            if (conversionId) {
                showExistingPdf(conversionId);
            }
        }
        
        // Render PDF from array buffer
        function renderPdf(pdfData) {
            // Clear any existing content
            pdfViewer.innerHTML = '';
            
            pdfjsLib.getDocument({ data: pdfData }).promise.then(function(pdf) {
                // Get total pages
                const numPages = pdf.numPages;
                
                // Create container for pages
                const pagesContainer = document.createElement('div');
                pagesContainer.className = 'pdf-pages';
                pdfViewer.appendChild(pagesContainer);
                
                // Render first few pages (for performance)
                const pagesToRender = Math.min(3, numPages);
                
                for (let pageNum = 1; pageNum <= pagesToRender; pageNum++) {
                    renderPage(pdf, pageNum, pagesContainer);
                }
                
                // Add a message if there are more pages
                if (numPages > pagesToRender) {
                    const morePages = document.createElement('div');
                    morePages.className = 'more-pages-message';
                    morePages.textContent = `... and ${numPages - pagesToRender} more pages`;
                    pagesContainer.appendChild(morePages);
                }
            }).catch(function(error) {
                console.error('Error rendering PDF:', error);
                pdfViewer.innerHTML = `<div class="pdf-error">Error loading PDF: ${error.message}</div>`;
            });
        }
        
        // Render a single page
        function renderPage(pdf, pageNum, container) {
            pdf.getPage(pageNum).then(function(page) {
                const viewport = page.getViewport({ scale: 1.0 });
                
                // Prepare canvas for rendering
                const pageContainer = document.createElement('div');
                pageContainer.className = 'pdf-page';
                container.appendChild(pageContainer);
                
                const canvas = document.createElement('canvas');
                pageContainer.appendChild(canvas);
                
                const context = canvas.getContext('2d');
                canvas.height = viewport.height;
                canvas.width = viewport.width;
                
                // Render PDF page into canvas context
                const renderContext = {
                    canvasContext: context,
                    viewport: viewport
                };
                
                page.render(renderContext);
                
                // Add page number
                const pageNumber = document.createElement('div');
                pageNumber.className = 'page-number';
                pageNumber.textContent = `Page ${pageNum}`;
                pageContainer.appendChild(pageNumber);
            });
        }
        
        // Load PDF for existing conversion
        function showExistingPdf(conversionId) {
            // For this demo, we won't actually load the PDF content from the server
            // In a real application, you would fetch the PDF data from an API endpoint
            
            // Instead, show a placeholder message in the PDF viewer
            pdfViewer.innerHTML = `
                <div class="pdf-placeholder">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-file-text">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                        <polyline points="10 9 9 9 8 9"></polyline>
                    </svg>
                    <p>PDF preview for conversion #${conversionId}</p>
                    <p class="text-muted">To view a new PDF, upload a file using the form above.</p>
                </div>
            `;
        }
    }
});
