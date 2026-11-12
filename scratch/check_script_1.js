
        let processedData = null;
        let pdfResultData = null;
        let toPdfResultData = null;

        // Tab Switcher
        function switchTab(tabName) {
            const wordTab = document.getElementById('wordToExcelTab');
            const pdfTab = document.getElementById('pdfToJpgTab');
            const toPdfTab = document.getElementById('fileToPdfTab');
            const questionTab = document.getElementById('questionBuilderTab');
            const photoTab = document.getElementById('photoEngineeringTab');

            const wordBtn = document.getElementById('tabWordToExcelBtn');
            const pdfBtn = document.getElementById('tabPdfToJpgBtn');
            const toPdfBtn = document.getElementById('tabFileToPdfBtn');
            const questionBtn = document.getElementById('tabQuestionBuilderBtn');
            const photoBtn = document.getElementById('tabPhotoEngineeringBtn');

            // Reset classes
            const activeClass = "flex-1 py-4 px-4 text-center font-bold text-base transition flex items-center justify-center gap-2 border-b-4 border-indigo-600 text-indigo-700 bg-white shadow-sm whitespace-nowrap";
            const inactiveClass = "flex-1 py-4 px-4 text-center font-bold text-base transition flex items-center justify-center gap-2 border-b-4 border-transparent text-gray-500 hover:text-indigo-600 hover:bg-slate-100 whitespace-nowrap";

            if (wordTab) wordTab.classList.add('hidden');
            if (pdfTab) pdfTab.classList.add('hidden');
            if (toPdfTab) toPdfTab.classList.add('hidden');
            if (questionTab) questionTab.classList.add('hidden');
            if (photoTab) photoTab.classList.add('hidden');

            if (wordBtn) wordBtn.className = inactiveClass;
            if (pdfBtn) pdfBtn.className = inactiveClass;
            if (toPdfBtn) toPdfBtn.className = inactiveClass;
            if (questionBtn) questionBtn.className = inactiveClass;
            if (photoBtn) photoBtn.className = inactiveClass;

            if (tabName === 'wordToExcel') {
                if (wordTab) wordTab.classList.remove('hidden');
                if (wordBtn) wordBtn.className = activeClass;
            } else if (tabName === 'pdfToJpg') {
                if (pdfTab) pdfTab.classList.remove('hidden');
                if (pdfBtn) pdfBtn.className = activeClass;
            } else if (tabName === 'fileToPdf') {
                if (toPdfTab) toPdfTab.classList.remove('hidden');
                if (toPdfBtn) toPdfBtn.className = activeClass;
            } else if (tabName === 'questionBuilder') {
                if (questionTab) questionTab.classList.remove('hidden');
                if (questionBtn) questionBtn.className = activeClass;
            } else if (tabName === 'photoEngineering') {
                if (photoTab) photoTab.classList.remove('hidden');
                if (photoBtn) photoBtn.className = activeClass;
            }
        }

        // --- WORD TO EXCEL LOGIC ---
        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData();
            formData.append('word_file', document.getElementById('wordFile').files[0]);
            formData.append('excel_template', document.getElementById('excelTemplate').files[0]);

            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                if (response.ok) {
                    processedData = result;
                    renderPreview(result);
                } else {
                    alert(result.error || 'কোনো সমস্যা হয়েছে');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('ফাইল প্রসেস করতে ব্যর্থ হয়েছে।');
            }
        });

        function renderPreview(result) {
            const head = document.getElementById('tableHead');
            const body = document.getElementById('tableBody');

            head.innerHTML = `<tr>${result.columns.map(col => `<th class="px-4 py-3 text-left font-bold text-indigo-900 border-b">${col}</th>`).join('')}</tr>`;

            body.innerHTML = result.data.map(row => {
                return `<tr class="hover:bg-slate-50">${result.columns.map(col => `<td class="px-4 py-3 whitespace-nowrap">${row[col] || ''}</td>`).join('')}</tr>`;
            }).join('');

            document.getElementById('previewSection').classList.remove('hidden');
        }

        document.getElementById('downloadBtn').addEventListener('click', async () => {
            if (!processedData) return;

            try {
                const response = await fetch('/download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(processedData)
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = (processedData.subject_title || 'Converted_File') + '.xlsx';
                    document.body.appendChild(a);
                    a.click();
                    a.removeChild(a);
                } else {
                    alert('ডাউনলোড করতে সমস্যা হয়েছে।');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });

        // --- MULTI-FORMAT TO JPG LOGIC ---
        document.getElementById('pdfUploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const fileInput = document.getElementById('pdfFileInput');
            const dpiSelect = document.getElementById('dpiSelect');

            if (!fileInput.files || fileInput.files.length === 0) {
                alert('দয়া করে অন্তত একটি ফাইল আপলোড করুন');
                return;
            }

            const formData = new FormData();
            for (let i = 0; i < fileInput.files.length; i++) {
                formData.append('pdf_file', fileInput.files[i]);
            }
            formData.append('dpi', dpiSelect.value);

            document.getElementById('pdfLoading').classList.remove('hidden');
            document.getElementById('pdfResultSection').classList.add('hidden');

            try {
                const response = await fetch('/convert_file', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                document.getElementById('pdfLoading').classList.add('hidden');

                if (response.ok && result.success) {
                    pdfResultData = result;
                    renderPdfResults(result);
                } else {
                    alert(result.error || 'ফাইল প্রসেস করতে ব্যর্থ হয়েছে');
                }
            } catch (error) {
                document.getElementById('pdfLoading').classList.add('hidden');
                console.error('Conversion Error:', error);
                alert('ফাইল কনভার্ট করতে ত্রুটি হয়েছে।');
            }
        });

        let dragSourceIndex = null;
        let dragType = null;

        function renderPdfResults(result) {
            const summaryText = document.getElementById('pdfSummaryText');
            const fileCount = result.total_files || 1;
            const fileLabel = fileCount > 1 ? `মোট ${fileCount}টি ফাইল` : `ফাইল: ${result.pdf_name} [${result.ext || 'FILE'}]`;
            summaryText.innerText = `${fileLabel} | মোট পেজ/ছবি: ${result.total_pages} টি | কোয়ালিটি: ${result.dpi} DPI HD`;

            const imagesGrid = document.getElementById('imagesGrid');
            imagesGrid.innerHTML = '';

            result.pages.forEach((pageData, index) => {
                const card = document.createElement('div');
                card.draggable = true;
                card.dataset.index = index;
                card.className = "bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition flex flex-col cursor-grab active:cursor-grabbing select-none";

                const pageNum = pageData.pageNumber || pageData.page || (index + 1);
                const displayLabel = pageData.label || `ছবি/পেজ ${pageNum}`;

                card.innerHTML = `
                    <div class="bg-indigo-50 border-b border-indigo-100 px-3 py-2 flex justify-between items-center text-xs font-bold text-indigo-900">
                        <span class="flex items-center gap-1.5 cursor-grab text-indigo-600">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"></path></svg>
                            ক্রম: #${index + 1}
                        </span>
                        <span class="text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded font-mono">পেজ ${pageNum}</span>
                    </div>
                    <div class="relative group cursor-pointer overflow-hidden bg-gray-100 flex items-center justify-center p-2" onclick="openModal('${pageData.data_url}', '${displayLabel} (${pageData.width} x ${pageData.height} px)')">
                        <img src="${pageData.data_url}" alt="${displayLabel}" class="max-h-64 object-contain rounded transition transform group-hover:scale-105 pointer-events-none">
                        <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-white font-bold text-sm pointer-events-none">
                            🔍 বড় করে দেখুন
                        </div>
                    </div>
                    <div class="p-4 flex flex-col justify-between flex-grow border-t border-gray-100">
                        <div class="flex justify-between items-center mb-3">
                            <span class="font-bold text-gray-800 text-sm truncate" title="${displayLabel}">${displayLabel}</span>
                            <span class="text-xs text-gray-500 font-mono">${pageData.width}×${pageData.height} px</span>
                        </div>
                        <button onclick="downloadSingleJpg('${pageData.data_url}', '${pageData.filename || result.pdf_name + '_page_' + pageNum + '.jpg'}')" class="w-full bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold py-2 px-3 rounded-lg text-sm transition flex items-center justify-center gap-1">
                            📥 ডাউনলোড JPG
                        </button>
                    </div>
                `;

                attachDragAndDropEvents(card, index, 'jpg');
                imagesGrid.appendChild(card);
            });

            document.getElementById('pdfResultSection').classList.remove('hidden');
        }

        // Download single JPG image
        function downloadSingleJpg(dataUrl, filename) {
            const a = document.createElement('a');
            a.href = dataUrl;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.removeChild(a);
        }

        // Download all images as ZIP (in current Drag & Drop order)
        document.getElementById('downloadAllZipBtn').addEventListener('click', async () => {
            if (!pdfResultData || !pdfResultData.pages || pdfResultData.pages.length === 0) return;

            try {
                const response = await fetch('/download_pdf_zip', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        pages: pdfResultData.pages,
                        zip_b64: pdfResultData.zip_b64,
                        pdf_name: pdfResultData.pdf_name
                    })
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${pdfResultData.pdf_name}_images.zip`;
                    document.body.appendChild(a);
                    a.click();
                    setTimeout(() => {
                        document.body.removeChild(a);
                        window.URL.revokeObjectURL(url);
                    }, 200);
                } else {
                    alert('জিপ ডাউনলোড করতে সমস্যা হয়েছে।');
                }
            } catch (error) {
                console.error('ZIP Download Error:', error);
            }
        });

        // --- MULTI-FORMAT TO PDF LOGIC ---
        document.getElementById('toPdfForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const fileInput = document.getElementById('toPdfFileInput');
            if (!fileInput.files || fileInput.files.length === 0) {
                alert('দয়া করে অন্তত একটি ফাইল আপলোড করুন');
                return;
            }

            const formData = new FormData();
            for (let i = 0; i < fileInput.files.length; i++) {
                formData.append('file', fileInput.files[i]);
            }

            document.getElementById('toPdfLoading').classList.remove('hidden');
            document.getElementById('toPdfResultSection').classList.add('hidden');

            try {
                const response = await fetch('/convert_to_pdf', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                document.getElementById('toPdfLoading').classList.add('hidden');

                if (response.ok && result.success) {
                    toPdfResultData = result;
                    renderToPdfResults(result);
                } else {
                    alert(result.error || 'পিডিএফ রূপান্তর করতে ব্যর্থ হয়েছে');
                }
            } catch (error) {
                document.getElementById('toPdfLoading').classList.add('hidden');
                console.error('To PDF Error:', error);
                alert('পিডিএফ ফাইল তৈরি করতে ত্রুটি হয়েছে।');
            }
        });

        function renderToPdfResults(result) {
            const summaryText = document.getElementById('toPdfSummaryText');
            const kbSize = Math.round(result.pdf_size / 1024);
            const fileCount = result.total_files || 1;
            const fileLabel = fileCount > 1 ? `মোট ${fileCount}টি ফাইল থেকে তৈরিকৃত Combined_Document.pdf` : `ফাইল: ${result.file_name}.pdf [${result.ext}]`;
            summaryText.innerText = `${fileLabel} | মোট পেজ: ${result.total_pages} টি | সাইজ: ${kbSize} KB`;

            const pdfPagesGrid = document.getElementById('pdfPagesGrid');
            pdfPagesGrid.innerHTML = '';

            result.preview_pages.forEach((pageData, index) => {
                const card = document.createElement('div');
                card.draggable = true;
                card.dataset.index = index;
                card.className = "bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition flex flex-col cursor-grab active:cursor-grabbing select-none";

                const pageNum = pageData.pageNumber || pageData.page || (index + 1);

                card.innerHTML = `
                    <div class="bg-purple-50 border-b border-purple-100 px-3 py-2 flex justify-between items-center text-xs font-bold text-purple-900">
                        <span class="flex items-center gap-1.5 cursor-grab text-purple-600">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"></path></svg>
                            ক্রম: #${index + 1}
                        </span>
                        <span class="text-purple-700 bg-purple-100 px-2 py-0.5 rounded font-mono">পেজ ${pageNum}</span>
                    </div>
                    <div class="relative group cursor-pointer overflow-hidden bg-gray-100 flex items-center justify-center p-2" onclick="openModal('${pageData.data_url}', 'পিডিএফ পেজ ${pageNum} (${pageData.width} x ${pageData.height} px)')">
                        <img src="${pageData.data_url}" alt="Page ${pageNum}" class="max-h-64 object-contain rounded transition transform group-hover:scale-105 pointer-events-none">
                        <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-white font-bold text-sm pointer-events-none">
                            🔍 বড় করে দেখুন
                        </div>
                    </div>
                    <div class="p-3 border-t border-gray-100 text-center bg-slate-50">
                        <span class="font-bold text-gray-700 text-sm">পেজ ${pageNum}</span>
                    </div>
                `;

                attachDragAndDropEvents(card, index, 'pdf');
                pdfPagesGrid.appendChild(card);
            });

            document.getElementById('toPdfResultSection').classList.remove('hidden');
        }

        function attachDragAndDropEvents(card, index, type) {
            card.addEventListener('dragstart', (e) => {
                dragSourceIndex = index;
                dragType = type;
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('text/plain', index);
                card.classList.add('opacity-40', 'scale-95', 'border-indigo-500');
            });

            card.addEventListener('dragend', () => {
                card.classList.remove('opacity-40', 'scale-95', 'border-indigo-500');
                const selector = type === 'jpg' ? '#imagesGrid > div' : '#pdfPagesGrid > div';
                document.querySelectorAll(selector).forEach(c => {
                    c.classList.remove('ring-4', 'ring-indigo-400', 'ring-purple-400', 'bg-indigo-50', 'bg-purple-50');
                });
            });

            card.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
                const ringColor = type === 'jpg' ? 'ring-indigo-400' : 'ring-purple-400';
                const bgColor = type === 'jpg' ? 'bg-indigo-50' : 'bg-purple-50';
                card.classList.add('ring-4', ringColor, bgColor);
            });

            card.addEventListener('dragleave', () => {
                const ringColor = type === 'jpg' ? 'ring-indigo-400' : 'ring-purple-400';
                const bgColor = type === 'jpg' ? 'bg-indigo-50' : 'bg-purple-50';
                card.classList.remove('ring-4', ringColor, bgColor);
            });

            card.addEventListener('drop', (e) => {
                e.preventDefault();
                const targetIndex = index;
                if (dragSourceIndex === null || dragSourceIndex === targetIndex || dragType !== type) {
                    return;
                }
                reorderPages(dragSourceIndex, targetIndex, type);
            });
        }

        function reorderPages(fromIndex, toIndex, type) {
            if (type === 'jpg' && pdfResultData && pdfResultData.pages) {
                const pages = pdfResultData.pages;
                // 1. Array Reordering
                const [movedPage] = pages.splice(fromIndex, 1);
                pages.splice(toIndex, 0, movedPage);

                // 2. Dynamic Serial Numbering starting from min(fromIndex, toIndex) to end
                const startIndex = Math.min(fromIndex, toIndex);
                for (let i = startIndex; i < pages.length; i++) {
                    const newSerial = i + 1;
                    pages[i].pageNumber = newSerial;
                    pages[i].page = newSerial;

                    if (pdfResultData.total_files > 1 && pages[i].source_file) {
                        const fileBase = pages[i].source_file.split('.')[0];
                        pages[i].label = `${fileBase} - পেজ ${newSerial}`;
                    } else {
                        pages[i].label = `পেজ/ছবি ${newSerial}`;
                    }
                }

                // 3. UI Update: Trigger immediate re-render
                renderPdfResults(pdfResultData);

            } else if (type === 'pdf' && toPdfResultData && toPdfResultData.preview_pages) {
                const pages = toPdfResultData.preview_pages;
                // 1. Array Reordering
                const [movedPage] = pages.splice(fromIndex, 1);
                pages.splice(toIndex, 0, movedPage);

                // 2. Dynamic Serial Numbering starting from min(fromIndex, toIndex) to end
                const startIndex = Math.min(fromIndex, toIndex);
                for (let i = startIndex; i < pages.length; i++) {
                    const newSerial = i + 1;
                    pages[i].pageNumber = newSerial;
                    pages[i].page = newSerial;
                }

                // 3. UI Update: Trigger immediate re-render
                renderToPdfResults(toPdfResultData);
            }
        }

        // Download PDF File (in current Drag & Drop order)
        document.getElementById('downloadPdfFileBtn').addEventListener('click', async () => {
            if (!toPdfResultData || !toPdfResultData.preview_pages || toPdfResultData.preview_pages.length === 0) {
                alert('কোনো ডাউনলোডেবল ডাটা পাওয়া যায়নি');
                return;
            }

            try {
                const response = await fetch('/download_pdf_file', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        pages: toPdfResultData.preview_pages,
                        pdf_b64: toPdfResultData.pdf_b64,
                        file_name: toPdfResultData.file_name
                    })
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);

                    const cleanName = (toPdfResultData.file_name || 'converted_document')
                        .replace(/\s+/g, ' ')
                        .replace(/[\\/*?:"<>|]/g, '')
                        .trim() + '.pdf';

                    const a = document.createElement('a');
                    a.href = url;
                    a.download = cleanName;
                    document.body.appendChild(a);
                    a.click();

                    setTimeout(() => {
                        document.body.removeChild(a);
                        window.URL.revokeObjectURL(url);
                    }, 200);
                } else {
                    alert('পিডিএফ ফাইল ডাউনলোড করতে সমস্যা হয়েছে।');
                }
            } catch (error) {
                console.error('PDF Download Error:', error);
                alert('পিডিএফ ফাইল ডাউনলোড করতে ত্রুটি হয়েছে।');
            }
        });

        // Lightbox Modal
        function openModal(imgSrc, caption) {
            document.getElementById('modalImage').src = imgSrc;
            document.getElementById('modalCaption').innerText = caption;
            document.getElementById('imageModal').classList.remove('hidden');
        }

        function closeModal() {
            document.getElementById('imageModal').classList.add('hidden');
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeModal();
        });

        // --- SMART QUESTION PAPER BUILDER LOGIC ---
        function customAlert(title, message) {
            document.getElementById("modal-title").innerText = title;
            document.getElementById("modal-body").innerText = message;
            document.getElementById("modal-input-container").classList.add("hidden");

            const cancelBtn = document.getElementById("modal-cancel-btn");
            const confirmBtn = document.getElementById("modal-confirm-btn");

            cancelBtn.classList.add("hidden");
            confirmBtn.innerText = "ঠিক আছে";
            confirmBtn.onclick = function () {
                document.getElementById("custom-modal").classList.add("hidden");
            };
            document.getElementById("custom-modal").classList.remove("hidden");
        }

        function customConfirm(title, message, onConfirm) {
            document.getElementById("modal-title").innerText = title;
            document.getElementById("modal-body").innerText = message;
            document.getElementById("modal-input-container").classList.add("hidden");

            const cancelBtn = document.getElementById("modal-cancel-btn");
            const confirmBtn = document.getElementById("modal-confirm-btn");

            cancelBtn.classList.remove("hidden");
            cancelBtn.innerText = "বাতিল";
            confirmBtn.innerText = "নিশ্চিত করুন";

            cancelBtn.onclick = function () {
                document.getElementById("custom-modal").classList.add("hidden");
            };
            confirmBtn.onclick = function () {
                document.getElementById("custom-modal").classList.add("hidden");
                if (onConfirm) onConfirm();
            };
            document.getElementById("custom-modal").classList.remove("hidden");
        }

        function customPrompt(title, message, defaultValue, placeholder, onConfirm) {
            document.getElementById("modal-title").innerText = title;
            document.getElementById("modal-body").innerText = message;

            const inputContainer = document.getElementById("modal-input-container");
            const inputField = document.getElementById("modal-input-field");
            inputContainer.classList.remove("hidden");
            inputField.value = defaultValue || "";
            inputField.placeholder = placeholder || "";

            const cancelBtn = document.getElementById("modal-cancel-btn");
            const confirmBtn = document.getElementById("modal-confirm-btn");

            cancelBtn.classList.remove("hidden");
            cancelBtn.innerText = "বাতিল";
            confirmBtn.innerText = "নিশ্চিত করুন";

            cancelBtn.onclick = function () {
                document.getElementById("custom-modal").classList.add("hidden");
                inputContainer.classList.add("hidden");
            };

            confirmBtn.onclick = function () {
                const val = inputField.value;
                document.getElementById("custom-modal").classList.add("hidden");
                inputContainer.classList.add("hidden");
                if (onConfirm) onConfirm(val);
            };

            document.getElementById("custom-modal").classList.remove("hidden");
        }

        let paperState = {
            schoolName: "আপনার প্রতিষ্ঠানের নাম এখানে লিখুন",
            examTitle: "পরীক্ষার নাম (যেমন: অর্ধ-বার্ষিক পরীক্ষা - ২০২৬)",
            class: "দশম",
            subject: "সাধারণ গণিত",
            marks: "১০০",
            time: "৩ ঘণ্টা",
            instruction: "ডান পাশের সংখ্যা প্রশ্নের পূর্ণমান জ্ঞাপন করে। যেকোনো ৫টি প্রশ্নের উত্তর দাও।",
            sections: [
                {
                    title: "বিভাগ-ক: বীজগণিত",
                    instruction: "যেকোনো ২টি প্রশ্নের উত্তর দাও",
                    questions: [
                        {
                            number: "১",
                            stem: "উদ্দীপক বা মূল প্রশ্নের প্রথম অংশ এখানে লিখুন। যেমন: $A = \\{x \\in \\mathbb{N} : x < 10\\}$ এবং $B = \\{2, 3, 5, 7\\}$।",
                            parts: [
                                { label: "ক", text: "প্রথম সংক্ষিপ্ত প্রশ্ন এখানে লিখুন?", mark: "২" },
                                { label: "খ", text: "দ্বিতীয় মাঝারি মানের প্রশ্ন বা প্রমাণ করার নির্দেশনা এখানে লিখুন?", mark: "৪" },
                                { label: "গ", text: "শেষ সৃজনশীল প্রশ্ন বা মান নির্ণয়ের নির্দেশনা এখানে লিখুন?", mark: "৪" }
                            ]
                        },
                        {
                            number: "২",
                            stem: "২য় প্রশ্নের উদ্দীপক এখানে লিখুন। যেমন: $x^2 - 3 = 2\\sqrt{2}$ হলে—",
                            parts: [
                                { label: "ক", text: "উৎপাদকে বিশ্লেষণ কর: $4a^2 - 12ab + 9b^2$।", mark: "২" },
                                { label: "খ", text: "প্রমাণ কর যে, $x^3 + \\frac{1}{x^3} = 5\\sqrt{2}$।", mark: "৪" },
                                { label: "গ", text: "$x^5 - \\frac{1}{x^5}$ এর মান কত তা নির্ণয় কর।", mark: "৪" }
                            ]
                        }
                    ]
                }
            ]
        };

        function renderPaper() {
            const container = document.getElementById("word-export-content");
            if (!container) return;

            let sectionsHtml = "";
            paperState.sections.forEach((sec, sIdx) => {
                let questionsHtml = "";
                sec.questions.forEach((q, qIdx) => {
                    let layoutClass = "flex flex-col gap-y-0.5";
                    let itemWidthClass = "w-full";

                    const currentLayout = q.layout || "1x1";
                    if (currentLayout === '1x4') {
                        layoutClass = "mcq-layout-1x4 flex flex-wrap gap-y-0.5";
                        itemWidthClass = "w-1/4 pr-1.5";
                    } else if (currentLayout === '2x2') {
                        layoutClass = "mcq-layout-2x2 flex flex-wrap gap-y-0.5";
                        itemWidthClass = "w-1/2 pr-1.5";
                    } else if (currentLayout === '4x1') {
                        layoutClass = "mcq-layout-4x1 flex flex-col gap-y-0.5";
                        itemWidthClass = "w-full";
                    } else if (currentLayout === '1x1') {
                        layoutClass = "mcq-layout-1x1 flex flex-col gap-y-0.5";
                        itemWidthClass = "w-full";
                    }

                    let partsHtml = "";
                    q.parts.forEach((p, pIdx) => {
                        partsHtml += `
                            <div class="${itemWidthClass} flex justify-between hover:bg-slate-50 p-0 rounded transition-all box-border my-0">
                                <div class="min-w-0 break-words pr-1">
                                    <span class="mcq-label font-semibold" style="font-family: 'NesarulOMR', 'Nikosh', 'Kalpurush', sans-serif;">${cleanMcqLabel(p.label)}</span> 
                                    <span onblur="updateStateField('parts', '${sIdx}-${qIdx}-${pIdx}', this.innerText)" contenteditable="true">${p.text}</span>
                                </div>
                                <div class="flex items-center gap-1 shrink-0">
                                    <button onclick="removePart(${sIdx}, ${qIdx}, ${pIdx})" class="no-print text-red-500 opacity-0 hover:opacity-100 text-[10px]">&times;</button>
                                </div>
                            </div>
                        `;
                    });

                    questionsHtml += `
                        <div class="mb-2.5 relative group border-l-2 border-transparent hover:border-slate-300 pl-2 question-item">
                            <div class="no-print absolute -left-6 top-0 flex flex-col gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                <button onclick="removeQuestion(${sIdx}, ${qIdx})" class="text-xs text-red-500 font-bold" title="মুছে ফেলুন">🗑️</button>
                                <button onclick="addPart(${sIdx}, ${qIdx})" class="text-[10px] text-blue-500 font-bold" title="প্রশ্ন উপ-অংশ/অপশন যোগ করুন">➕</button>
                            </div>
                            <div class="flex justify-between font-semibold mb-0.5">
                                <div>
                                    <span onblur="updateStateField('qNumber', '${sIdx}-${qIdx}', this.innerText)" contenteditable="true">${q.number}</span>. 
                                    <span onblur="updateStateField('stem', '${sIdx}-${qIdx}', this.innerText)" contenteditable="true">${q.stem}</span>
                                </div>
                            </div>
                            <div class="pl-3 ${layoutClass}">
                                ${partsHtml}
                            </div>
                        </div>
                    `;
                });

                sectionsHtml += `
                    <div class="mb-3">
                        <div class="border-b border-black font-bold text-base mb-1.5 flex justify-between items-center bg-gray-100 px-2 py-0.5 section-title-bar">
                            <span onblur="updateStateField('sectionTitle', '${sIdx}', this.innerText)" contenteditable="true">${sec.title}</span>
                            <div class="flex items-center gap-2">
                                <span onblur="updateStateField('sectionInstruction', '${sIdx}', this.innerText)" contenteditable="true" class="text-sm font-normal">${sec.instruction}</span>
                                <button onclick="removeSection(${sIdx})" class="no-print text-red-600 hover:text-red-700 text-xs font-bold px-1 rounded">&times;</button>
                            </div>
                        </div>
                        ${questionsHtml}
                        <button onclick="addQuestion(${sIdx})" class="no-print w-full border border-dashed border-slate-300 hover:border-slate-400 py-1 rounded text-xs text-slate-500 hover:text-slate-700 transition-all font-semibold my-1">
                            ➕ এই বিভাগে নতুন সৃজনশীল প্রশ্ন যোগ করুন
                        </button>
                    </div>
                `;
            });

            container.innerHTML = `
                <div class="paper-content-columns">
                    <!-- School & Exam Header Information -->
                    <div class="text-center mb-3 paper-header-block">
                        <h2 onblur="updateStateField('schoolName', '', this.innerText)" contenteditable="true" class="text-xl font-bold text-slate-900 tracking-tight leading-tight">${paperState.schoolName}</h2>
                        <h3 onblur="updateStateField('examTitle', '', this.innerText)" contenteditable="true" class="text-base font-semibold text-gray-700 mt-0.5 leading-tight">${paperState.examTitle}</h3>
                        
                        <!-- Meta Table details -->
                        <div class="border-t-2 border-b-2 border-slate-900 py-1 mt-1.5 flex justify-between font-semibold text-xs">
                            <div>শ্রেণি: <span onblur="updateStateField('class', '', this.innerText)" contenteditable="true">${paperState.class}</span></div>
                            <div>বিষয়: <span onblur="updateStateField('subject', '', this.innerText)" contenteditable="true">${paperState.subject}</span></div>
                            <div>পূর্ণমান: <span onblur="updateStateField('marks', '', this.innerText)" contenteditable="true">${paperState.marks}</span></div>
                            <div>সময়: <span onblur="updateStateField('time', '', this.innerText)" contenteditable="true">${paperState.time}</span></div>
                        </div>
                        
                        <p onblur="updateStateField('instruction', '', this.innerText)" contenteditable="true" class="text-xs italic text-center mt-1 text-slate-600">
                            [${paperState.instruction}]
                        </p>
                    </div>
                    
                    ${sectionsHtml}
                </div>
            `;

            refreshMathJax();
        }

        function updateStateField(field, key, value) {
            if (field === 'schoolName') paperState.schoolName = value;
            if (field === 'examTitle') paperState.examTitle = value;
            if (field === 'class') paperState.class = value;
            if (field === 'subject') paperState.subject = value;
            if (field === 'marks') paperState.marks = value;
            if (field === 'time') paperState.time = value;
            if (field === 'instruction') paperState.instruction = value;

            if (field === 'sectionTitle') {
                paperState.sections[parseInt(key)].title = value;
            }
            if (field === 'sectionInstruction') {
                paperState.sections[parseInt(key)].instruction = value;
            }
            if (field === 'qNumber') {
                const [sIdx, qIdx] = key.split('-').map(Number);
                paperState.sections[sIdx].questions[qIdx].number = value;
            }
            if (field === 'stem') {
                const [sIdx, qIdx] = key.split('-').map(Number);
                paperState.sections[sIdx].questions[qIdx].stem = value;
            }
            if (field === 'parts') {
                const [sIdx, qIdx, pIdx] = key.split('-').map(Number);
                paperState.sections[sIdx].questions[qIdx].parts[pIdx].text = value;
            }
            if (field === 'mark') {
                const [sIdx, qIdx, pIdx] = key.split('-').map(Number);
                paperState.sections[sIdx].questions[qIdx].parts[pIdx].mark = value;
            }
        }

        function setQuestionLayout(sIdx, qIdx, layoutStyle) {
            if (paperState.sections[sIdx] && paperState.sections[sIdx].questions[qIdx]) {
                paperState.sections[sIdx].questions[qIdx].layout = layoutStyle;
                renderPaper();
            }
        }

        function setGlobalMcqLayout(layoutStyle) {
            if (!paperState || !paperState.sections) return;
            paperState.sections.forEach(sec => {
                if (sec.questions) {
                    sec.questions.forEach(q => {
                        q.layout = layoutStyle;
                    });
                }
            });
            renderPaper();
        }

        function addSection() {
            paperState.sections.push({
                title: "নতুন বিভাগ",
                instruction: "যেকোনো প্রশ্নের উত্তর দাও",
                questions: []
            });
            renderPaper();
        }

        function removeSection(sIdx) {
            paperState.sections.splice(sIdx, 1);
            renderPaper();
        }

        function addQuestion(sIdx) {
            const nextNum = paperState.sections[sIdx].questions.length + 1;
            paperState.sections[sIdx].questions.push({
                number: nextNum.toString(),
                stem: "নতুন উদ্দীপক বিবরণ...",
                parts: [
                    { label: "ক", text: "১ম অংশ লিখুন?", mark: "২" }
                ]
            });
            renderPaper();
        }

        function removeQuestion(sIdx, qIdx) {
            paperState.sections[sIdx].questions.splice(qIdx, 1);
            renderPaper();
        }

        document.addEventListener('keydown', function (e) {
            if (e.ctrlKey && e.shiftKey && e.key === 'S') {
                e.preventDefault();
                addSection();
            }
        });

        function addPart(sIdx, qIdx) {
            const labels = ["ক", "খ", "গ", "ঘ"];
            const currentParts = paperState.sections[sIdx].questions[qIdx].parts;
            const nextLabel = labels[currentParts.length] || "চ";
            currentParts.push({
                label: nextLabel,
                text: "নতুন উপ-প্রশ্ন...",
                mark: "৪"
            });
            renderPaper();
        }

        function removePart(sIdx, qIdx, pIdx) {
            paperState.sections[sIdx].questions[qIdx].parts.splice(pIdx, 1);
            renderPaper();
        }

        function resetToTemplate() {
            customConfirm("সতর্কতা", "আপনি কি নিশ্চিতভাবে ডিফল্ট ফরম্যাটে রিসেট করতে চান? সব এডিট করা তথ্য মুছে যাবে।", function () {
                location.reload();
            });
        }

        function refreshMathJax() {
            if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
                MathJax.typesetPromise().then(() => {
                    console.log('MathJax update successful.');
                }).catch((err) => console.log('MathJax error:', err));
            }
        }

        const apiKey = "";

        function decodeGoogleJwt(token) {
            try {
                let base64Url = token.split('.')[1];
                let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
                let jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
                    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                }).join(''));
                return JSON.parse(jsonPayload);
            } catch (err) {
                console.error("JWT decoding error:", err);
                return null;
            }
        }

        function handleGoogleCredentialResponse(response) {
            const responsePayload = decodeGoogleJwt(response.credential);
            if (responsePayload) {
                const userObj = {
                    name: responsePayload.name,
                    email: responsePayload.email,
                    picture: responsePayload.picture,
                    googleConnected: true
                };

                localStorage.setItem("linked_gmail_account", JSON.stringify(userObj));
                customAlert("সফল জিমেইল সিঙ্ক", `আপনার ক্রোম লগইন মেইল ${userObj.email} সফলভাবে সংযুক্ত হয়েছে। জেমিনি এআই সক্রিয় করা হচ্ছে!`);

                if (!localStorage.getItem("custom_gemini_api_key")) {
                    customPrompt(
                        "জেমিনি অ্যাক্টিভেশন",
                        "জিমেইল অ্যাক্টিভেট হয়েছে! এআই চালু করার জন্য ১-ক্লিকে পাওয়া ফ্রি জেমিনি এপিআই কীটি এখানে দিন (বাম প্যানেলের 'কী' বক্সেও দিতে পারেন):",
                        "",
                        "AIzaSy...",
                        function (mockSessionKey) {
                            if (mockSessionKey && mockSessionKey.trim() !== "") {
                                localStorage.setItem("custom_gemini_api_key", mockSessionKey.trim());
                            }
                            updateApiStatusUI();
                        }
                    );
                } else {
                    updateApiStatusUI();
                }
            }
        }

        function initiateGmailLogin() {
            if (typeof google === 'undefined') {
                simulateChromeGmailAutoSync();
                return;
            }

            try {
                google.accounts.id.prompt((notification) => {
                    if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
                        google.accounts.id.initialize({
                            client_id: "7538259021-mockclientid.apps.googleusercontent.com",
                            callback: handleGoogleCredentialResponse
                        });
                        simulateChromeGmailAutoSync();
                    }
                });
            } catch (e) {
                simulateChromeGmailAutoSync();
            }
        }

        function simulateChromeGmailAutoSync() {
            customConfirm(
                "ক্রোম জিমেইল অটো-ডিটেক্ট",
                "আপনার ক্রোম ব্রাউজারে লগইন থাকা জিমেইল অ্যাকাউন্টটি স্বয়ংক্রিয়ভাবে ডিটেক্ট ও লিংক করতে চান?",
                function () {
                    customPrompt(
                        "জিমেইল নিশ্চিতকরণ",
                        "ডিটেক্ট করা ক্রোম অ্যাকাউন্ট জিমেইলটি নিশ্চিত করুন:",
                        "user.chrome.login@gmail.com",
                        "example@gmail.com",
                        function (inputEmail) {
                            if (inputEmail && inputEmail.trim() !== "") {
                                const userObj = {
                                    name: "ক্রোম জিমেইল ইউজার",
                                    email: inputEmail.trim(),
                                    picture: "https://www.gstatic.com/images/branding/product/2x/avatar_anonymous_512dp.png",
                                    googleConnected: true
                                };
                                localStorage.setItem("linked_gmail_account", JSON.stringify(userObj));

                                customPrompt(
                                    "জেমিনি অ্যাক্টিভেশন",
                                    "জিমেইল অ্যাকাউন্ট লিংক হয়েছে! জেমিনি এআই চালু করার জন্য আপনার জেমিনি এপিআই কীটি যুক্ত করুন:",
                                    "",
                                    "AIzaSy...",
                                    function (activeKey) {
                                        if (activeKey && activeKey.trim() !== "") {
                                            localStorage.setItem("custom_gemini_api_key", activeKey.trim());
                                        }
                                        updateApiStatusUI();
                                        customAlert("সফল লিংকড", `জিমেইল ${userObj.email} সফলভাবে এডিটর প্ল্যাটফর্মের সাথে লিংকড হয়েছে!`);
                                    }
                                );
                            }
                        }
                    );
                }
            );
        }

        function getActiveApiKey() {
            if (apiKey && apiKey.trim() !== "") {
                return apiKey;
            }
            return localStorage.getItem("custom_gemini_api_key") || "";
        }

        function logoutGmail() {
            localStorage.removeItem("linked_gmail_account");
            localStorage.removeItem("custom_gemini_api_key");
            updateApiStatusUI();
            customAlert("লগআউট", "আপনার জিমেইল অ্যাকাউন্ট ও এআই বক্সের সংযোগ বিচ্ছিন্ন করা হয়েছে।");
        }

        function saveManualToken() {
            const tokenVal = document.getElementById("manual-token")?.value.trim();
            if (tokenVal) {
                localStorage.setItem("custom_gemini_api_key", tokenVal);
                document.getElementById("manual-token").value = "";
                updateApiStatusUI();
                customAlert("সফল", "জেমিনি অ্যাক্টিভেশন কী সফলভাবে সেভ হয়েছে!");
            }
        }

        function updateApiStatusUI() {
            const statusContainer = document.getElementById("gmail-status-container");
            const loginArea = document.getElementById("gmail-login-area");
            const offlineTokenBox = document.getElementById("offline-token-box");

            if (!statusContainer) return;

            if (apiKey && apiKey.trim() !== "") {
                statusContainer.className = "p-3 rounded-lg mb-1 bg-green-50 border border-green-200 text-xs text-green-800";
                statusContainer.innerHTML = `
                    <div class="flex items-center gap-2 mb-1.5">
                        <span class="flex h-2 w-2 relative">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                        </span>
                        <span class="font-bold">🟢 এআই অটো-লিংকড (সক্রিয়)</span>
                    </div>
                    <p class="text-[10px] text-green-600">প্ল্যাটফর্ম সেশনের মাধ্যমে আপনার জিমেইল এআই অটোমেটিক কানেক্ট রয়েছে।</p>
                `;
                if (loginArea) loginArea.classList.add("hidden");
                return;
            }

            const linkedAccountJson = localStorage.getItem("linked_gmail_account");
            if (linkedAccountJson) {
                const user = JSON.parse(linkedAccountJson);
                const hasKey = getActiveApiKey() !== "";

                statusContainer.className = "p-3 rounded-lg mb-1 bg-blue-50 border border-blue-200 text-xs text-slate-800";
                statusContainer.innerHTML = `
                    <div class="flex items-center gap-2.5">
                        <img src="${user.picture}" class="w-8 h-8 rounded-full border border-slate-300" onerror="this.src='https://www.gstatic.com/images/branding/product/2x/avatar_anonymous_512dp.png'">
                        <div>
                            <div class="font-bold text-slate-900 text-xs">${user.name}</div>
                            <div class="text-[10px] text-slate-500">${user.email}</div>
                        </div>
                    </div>
                    <div class="mt-2.5 pt-2 border-t border-blue-100/60 flex items-center justify-between">
                        <span class="text-[10px] font-bold ${hasKey ? 'text-green-600' : 'text-amber-500'}">
                            ${hasKey ? '⚡ জেমিনি বক্স সক্রিয়' : '⚠️ এআই কী প্রয়োজন'}
                        </span>
                        <button onclick="logoutGmail()" class="text-[10px] text-red-500 hover:underline">সংযোগ বিচ্ছিন্ন করুন</button>
                    </div>
                `;

                if (loginArea) loginArea.classList.remove("hidden");
                if (offlineTokenBox) {
                    if (hasKey) {
                        offlineTokenBox.classList.add("hidden");
                    } else {
                        offlineTokenBox.classList.remove("hidden");
                    }
                }
            } else {
                statusContainer.className = "p-3 rounded-lg mb-1 bg-amber-50 border border-amber-200 text-xs text-amber-800";
                statusContainer.innerHTML = `
                    <div class="flex items-center gap-2">
                        <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-amber-500"></span>
                        <span class="font-bold text-xs">অ্যাকাউন্ট সংযুক্ত নেই</span>
                    </div>
                    <p class="mt-1 text-[10px] text-amber-600">জেমিনি এআই চালু করতে আপনার গুগল জিমেইল আইডি লিংক করুন।</p>
                `;
                if (loginArea) loginArea.classList.remove("hidden");
                if (offlineTokenBox) offlineTokenBox.classList.remove("hidden");
            }
        }

        async function fetchWithRetry(url, options, retries = 3, delay = 1000) {
            try {
                const response = await fetch(url, options);
                if (!response.ok) {
                    let errorMsg = `HTTP error! status: ${response.status}`;
                    try {
                        const errData = await response.json();
                        if (errData.error && errData.error.message) {
                            errorMsg = errData.error.message;
                        }
                    } catch (e) { }

                    if ((response.status === 429 || response.status >= 500) && retries > 0) {
                        await new Promise(resolve => setTimeout(resolve, delay));
                        return fetchWithRetry(url, options, retries - 1, delay * 2);
                    }
                    throw new Error(errorMsg);
                }
                return await response.json();
            } catch (error) {
                if (error instanceof TypeError && retries > 1) {
                    await new Promise(resolve => setTimeout(resolve, delay));
                    return fetchWithRetry(url, options, retries - 1, delay * 2);
                }
                throw error;
            }
        }

        function showStatus(message, isWorking = true) {
            const loader = document.getElementById("loader-status");
            const loaderMsg = document.getElementById("loader-message");
            if (!loader || !loaderMsg) return;
            loader.classList.remove("hidden");
            loaderMsg.innerText = message;
            if (!isWorking) {
                setTimeout(() => loader.classList.add("hidden"), 6000);
            }
        }

        const systemPrompt = `You are an expert Math teacher and examiner. Convert raw math exam text, questions, images, or PDF documents into clean structured JSON. 
Ensure LaTeX equations are preserved inside $ and $ for inline or $$and$$ for block formatting.
The generated output must strictly follow the provided JSON schema. Ensure bangla names and mathematical terms are spelled and structured correctly.`;

        const responseSchema = {
            type: "OBJECT",
            properties: {
                schoolName: { type: "STRING" },
                examTitle: { type: "STRING" },
                class: { type: "STRING" },
                subject: { type: "STRING" },
                marks: { type: "STRING" },
                time: { type: "STRING" },
                instruction: { type: "STRING" },
                sections: {
                    type: "ARRAY",
                    items: {
                        type: "OBJECT",
                        properties: {
                            title: { type: "STRING" },
                            instruction: { type: "STRING" },
                            questions: {
                                type: "ARRAY",
                                items: {
                                    type: "OBJECT",
                                    properties: {
                                        number: { type: "STRING" },
                                        stem: { type: "STRING" },
                                        parts: {
                                            type: "ARRAY",
                                            items: {
                                                type: "OBJECT",
                                                properties: {
                                                    label: { type: "STRING" },
                                                    text: { type: "STRING" },
                                                    mark: { type: "STRING" }
                                                },
                                                required: ["label", "text", "mark"]
                                            }
                                        }
                                    },
                                    required: ["number", "stem", "parts"]
                                }
                            }
                        },
                        required: ["title", "instruction", "questions"]
                    }
                }
            },
            required: ["schoolName", "examTitle", "class", "subject", "marks", "time", "instruction", "sections"]
        };

        async function runGeminiParser(promptText, base64File = null, mimeType = null) {
            const activeKey = getActiveApiKey();
            if (!activeKey) {
                customAlert("এপিআই কানেকশন ত্রুটি", "এআই দিয়ে রূপান্তর করতে একটি সচল জিমেইল আইডি লিংক করুন এবং জেমিনি বক্স সক্রিয় করুন।");
                return;
            }

            const modelsToTry = [
                "gemini-2.5-flash",
                "gemini-1.5-flash"
            ];

            let lastError = null;
            let parsedState = null;

            const thinkingBudget = parseInt(document.getElementById("thinking-level-select")?.value || "0");

            for (let i = 0; i < modelsToTry.length; i++) {
                const currentModel = modelsToTry[i];

                let modelLabel = currentModel;
                if (currentModel.includes("2.5")) {
                    if (thinkingBudget === 16384) {
                        modelLabel = "Gemini-Thinking Level-Extended";
                    } else if (thinkingBudget === 2048) {
                        modelLabel = "Gemini-Thinking Level-Standard";
                    } else {
                        modelLabel = "Gemini-2.5-Flash (Thinking Disabled)";
                    }
                } else {
                    modelLabel = "Gemini-1.5-Flash";
                }

                showStatus(`এআই মডেল প্রস্তুত করা হচ্ছে (${modelLabel})...`);
                const url = `https://generativelanguage.googleapis.com/v1beta/models/${currentModel}:generateContent?key=${activeKey}`;

                let contentsParts = [];
                if (base64File) {
                    showStatus(mimeType === "application/pdf" ? `পিডিএফ প্রসেস করা হচ্ছে (${modelLabel})...` : `ছবি প্রসেস করা হচ্ছে (${modelLabel})...`);
                    contentsParts.push({ text: promptText });
                    contentsParts.push({
                        inlineData: {
                            mimeType: mimeType,
                            data: base64File
                        }
                    });
                } else {
                    showStatus(`এলোমেলো প্রশ্ন সাজানো হচ্ছে (${modelLabel})...`);
                    contentsParts.push({ text: promptText });
                }

                const payload = {
                    contents: [{ parts: contentsParts }],
                    systemInstruction: { parts: [{ text: systemPrompt }] },
                    generationConfig: {
                        responseMimeType: "application/json",
                        responseSchema: responseSchema
                    }
                };

                if (thinkingBudget > 0 && currentModel.includes("2.5")) {
                    payload.generationConfig.thinkingConfig = {
                        thinkingBudget: thinkingBudget
                    };
                }

                try {
                    const responseData = await fetchWithRetry(url, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    const rawJsonText = responseData.candidates?.[0]?.content?.parts?.[0]?.text;
                    if (rawJsonText) {
                        parsedState = JSON.parse(rawJsonText);
                        break;
                    }
                } catch (err) {
                    console.warn(`Model ${currentModel} failed:`, err.message);
                    lastError = err;
                    if (err.message && (err.message.includes("API key not valid") || err.message.includes("API_KEY_INVALID"))) {
                        break;
                    }
                }
            }

            if (parsedState) {
                paperState = parsedState;
                renderPaper();
                showStatus("✨ সফলভাবে এআই দিয়ে রূপান্তর করা হয়েছে!", false);
            } else {
                console.error("Gemini Parsing Final Error Details:", lastError);
                let detailedMessage = lastError ? lastError.message : "ইন্টারনেট সংযোগ বা সার্ভার সমস্যা!";

                if (lastError instanceof TypeError || (lastError && lastError.message && lastError.message.includes("Failed to fetch"))) {
                    detailedMessage = "ব্রাউজার সিকিউরিটি (CORS) ব্লকিং অথবা ফাইল লোকাল প্রোটোকল প্রাইভেসির কারণে রিকোয়েস্ট ব্লক হয়েছে। সমাধান পেতে এই ফাইলটি ডাবল ক্লিক করে চালানোর বদলে VS Code Live Server ব্যবহার করুন অথবা Python Server চালু করে চালান।";
                    const banner = document.getElementById("cors-warning-banner");
                    if (banner) banner.classList.remove("hidden");
                }
                showStatus(`❌ ত্রুটি: ${detailedMessage}`, false);
            }
        }

        function processAITextInput() {
            const txt = document.getElementById("ai-text-input")?.value.trim();
            if (!txt) {
                customAlert("বার্তা", "দয়া করে টেক্সট বক্সে কিছু লিখুন বা পেস্ট করুন।");
                return;
            }
            runGeminiParser(`Please extract and format the following exam questions into clean JSON schema structures:\n\n${txt}`);
        }

        function handleAIFileUpload(event) {
            const file = event.target.files[0];
            if (!file) return;

            showStatus("ফাইলটি ব্রাউজারে আপলোড হচ্ছে...");

            if (file.type.startsWith('image/') || file.type === "application/pdf") {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const base64Data = e.target.result.split(',')[1];
                    const msg = file.type === "application/pdf" ?
                        "Read this exam question sheet PDF document. Extract all pages, read all questions, and convert its contents into the specified structured JSON, carefully preserving all mathematical formula notation as $...$ inline LaTeX format." :
                        "Read this exam question sheet image. Convert its contents into the specified structured JSON, carefully preserving all mathematical formula notation as $...$ inline LaTeX format.";
                    runGeminiParser(msg, base64Data, file.type);
                };
                reader.readAsDataURL(file);
            } else if (file.type === "text/plain") {
                const reader = new FileReader();
                reader.onload = function (e) {
                    runGeminiParser(`Convert this raw text file into structured math exam JSON schema format:\n\n${e.target.result}`);
                };
                reader.readAsText(file);
            } else {
                showStatus("❌ শুধুমাত্র ছবি (PNG/JPG), PDF বা টেক্সট ফাইল আপলোড করা সম্ভব!", false);
            }
        }

        function setupDropZoneEvents() {
            const dropZone = document.getElementById('drop-zone');
            if (!dropZone) return;

            dropZone.addEventListener('click', () => {
                const input = document.getElementById('ai-file-input');
                if (input) input.click();
            });

            ['dragenter', 'dragover'].forEach(eventName => {
                dropZone.addEventListener(eventName, (e) => {
                    e.preventDefault();
                    dropZone.classList.add('border-blue-500', 'bg-blue-50/50');
                }, false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, (e) => {
                    e.preventDefault();
                    dropZone.classList.remove('border-blue-500', 'bg-blue-50/50');
                }, false);
            });

            dropZone.addEventListener('drop', (e) => {
                const dt = e.dataTransfer;
                const files = dt.files;
                if (files.length) {
                    const inputElement = document.getElementById('ai-file-input');
                    if (inputElement) inputElement.files = files;
                    handleAIFileUpload({ target: { files: files } });
                }
            });
        }

        function downloadJSONBackup() {
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(paperState, null, 2));
            const dlAnchorElem = document.createElement('a');
            dlAnchorElem.setAttribute("href", dataStr);
            dlAnchorElem.setAttribute("download", `Math_Exam_Backup_${new Date().toISOString().slice(0, 10)}.json`);
            dlAnchorElem.click();
        }

        function triggerJSONUpload() {
            const input = document.getElementById("json-file-input");
            if (input) input.click();
        }

        function handleJSONFileLoad(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function (e) {
                try {
                    const data = JSON.parse(e.target.result);
                    if (data.schoolName && data.sections) {
                        paperState = data;
                        renderPaper();
                        customAlert("সফল", "সফলভাবে ব্যাকআপ ফাইল রিস্টোর করা হয়েছে!");
                    } else {
                        customAlert("ত্রুটি", "ভুল বা ত্রুটিপূর্ণ ফাইল ফরম্যাট!");
                    }
                } catch (err) {
                    customAlert("ত্রুটি", "ফাইলটি রিড করতে ব্যর্থ হয়েছে!");
                }
            };
            reader.readAsText(file);
        }

        function findBalancedBrace(str, startIdx) {
            let depth = 0;
            for (let i = startIdx; i < str.length; i++) {
                if (str[i] === '{') depth++;
                else if (str[i] === '}') {
                    depth--;
                    if (depth === 0) return i;
                }
            }
            return -1;
        }

        function getFractionWidth(num, den) {
            const cleanNum = num.replace(/<[^>]+>/g, '');
            const cleanDen = den.replace(/<[^>]+>/g, '');
            const maxLen = Math.max(cleanNum.length, cleanDen.length);
            return Math.max(24, maxLen * 8 + 14);
        }

        function findBalancedBackwards(str, closeIdx, openChar, closeChar) {
            let depth = 0;
            for (let i = closeIdx; i >= 0; i--) {
                if (str[i] === closeChar) {
                    depth++;
                } else if (str[i] === openChar) {
                    depth--;
                    if (depth === 0) return i;
                }
            }
            return -1;
        }

        function findBalancedBraceBackwards(str, closeIdx) {
            return findBalancedBackwards(str, closeIdx, '{', '}');
        }

        function findBalancedParenthesisBackwards(str, closeIdx) {
            return findBalancedBackwards(str, closeIdx, '(', ')');
        }

        function findBalancedBracketBackwards(str, closeIdx) {
            return findBalancedBackwards(str, closeIdx, '[', ']');
        }

        function findMatchingOpenTag(str, closeTagEndIdx) {
            let p = closeTagEndIdx;
            let tagStart = str.lastIndexOf('<', p);
            if (tagStart === -1) return -1;
            let tagText = str.substring(tagStart, p + 1);
            let match = tagText.match(/^<\/([a-zA-Z0-9:]+)>/);
            if (!match) return -1;
            let tagName = match[1];

            let depth = 1;
            let currentIdx = tagStart;
            while (depth > 0 && currentIdx > 0) {
                let prevTagStart = str.lastIndexOf('<', currentIdx - 1);
                if (prevTagStart === -1) return -1;
                let prevTagEnd = str.indexOf('>', prevTagStart);
                if (prevTagEnd === -1) return -1;
                let prevTagText = str.substring(prevTagStart, prevTagEnd + 1);
                
                if (prevTagText.startsWith('</' + tagName + '>')) {
                    depth++;
                } else if (prevTagText.startsWith('<' + tagName + '>') || prevTagText.startsWith('<' + tagName + ' ')) {
                    depth--;
                }
                currentIdx = prevTagStart;
            }
            return currentIdx;
        }

        function extractScript(str, scriptCharIdx) {
            let rest = str.substring(scriptCharIdx + 1);
            if (rest.startsWith('{')) {
                let braceEnd = findBalancedBrace(str, scriptCharIdx + 1);
                if (braceEnd !== -1) {
                    return {
                        content: str.substring(scriptCharIdx + 2, braceEnd),
                        endIndex: braceEnd + 1
                    };
                }
            }
            let p = 0;
            while (p < rest.length && /\s/.test(rest[p])) {
                p++;
            }
            if (p < rest.length) {
                if (rest[p] === '\\') {
                    let cmdMatch = rest.substring(p).match(/^\\[a-zA-Z]+/);
                    if (cmdMatch) {
                        return {
                            content: cmdMatch[0],
                            endIndex: scriptCharIdx + 1 + p + cmdMatch[0].length
                        };
                    }
                }
                return {
                    content: rest[p],
                    endIndex: scriptCharIdx + 1 + p + 1
                };
            }
            return null;
        }

        function findBaseData(str, scriptCharIdx) {
            let p = scriptCharIdx - 1;
            while (p >= 0 && /\s/.test(str[p])) {
                p--;
            }
            if (p < 0) return null;
            
            let char = str[p];
            if (char === '}') {
                let openBrace = findBalancedBraceBackwards(str, p);
                if (openBrace !== -1) {
                    return {
                        text: str.substring(openBrace + 1, p),
                        startIndex: openBrace
                    };
                }
            } else if (char === ')') {
                let openParen = findBalancedParenthesisBackwards(str, p);
                if (openParen !== -1) {
                    return {
                        text: str.substring(openParen + 1, p),
                        startIndex: openParen
                    };
                }
            } else if (char === ']') {
                let openBracket = findBalancedBracketBackwards(str, p);
                if (openBracket !== -1) {
                    return {
                        text: str.substring(openBracket + 1, p),
                        startIndex: openBracket
                    };
                }
            } else if (char === '>') {
                let openTag = findMatchingOpenTag(str, p);
                if (openTag !== -1) {
                    return {
                        text: str.substring(openTag, p + 1),
                        startIndex: openTag
                    };
                }
            } else {
                let sub = str.substring(0, p + 1);
                let match = sub.match(/(\\[a-zA-Z]+|[a-zA-Z0-9θαβ∞∠△°·×÷±≈≠≤≥∈ℕℤ∖∪∩]+)$/);
                if (match) {
                    let text = match[1];
                    return {
                        text: text,
                        startIndex: p + 1 - text.length
                    };
                }
                return {
                    text: char,
                    startIndex: p
                };
            }
            return null;
        }

        function parseScriptsToWordHtml(str) {
            let f = str;
            let idx = -1;
            for (let i = 0; i < f.length; i++) {
                if (f[i] === '^' || f[i] === '_') {
                    let lastOpen = f.lastIndexOf('<', i);
                    let lastClose = f.lastIndexOf('>', i);
                    if (lastOpen > lastClose) {
                        continue;
                    }
                    idx = i;
                    break;
                }
            }
            if (idx === -1) return f;
            
            let isSup = (f[idx] === '^');
            let script1Data = extractScript(f, idx);
            if (!script1Data) {
                let nextStr = f.substring(0, idx) + f.substring(idx + 1);
                return parseScriptsToWordHtml(nextStr);
            }
            
            let script1Content = script1Data.content;
            let script1End = script1Data.endIndex;
            
            let hasSecondScript = false;
            let script2IsSup = false;
            let script2Data = null;
            
            let nextCharIdx = script1End;
            while (nextCharIdx < f.length && /\s/.test(f[nextCharIdx])) {
                nextCharIdx++;
            }
            
            if (nextCharIdx < f.length) {
                let char = f[nextCharIdx];
                if ((isSup && char === '_') || (!isSup && char === '^')) {
                    hasSecondScript = true;
                    script2IsSup = (char === '^');
                    script2Data = extractScript(f, nextCharIdx);
                }
            }
            
            let baseData = findBaseData(f, idx);
            if (!baseData) {
                let nextStr = f.substring(0, idx) + script1Content + f.substring(script1End);
                return parseScriptsToWordHtml(nextStr);
            }
            
            let baseText = baseData.text;
            let baseStart = baseData.startIndex;
            
            baseText = parseScriptsToWordHtml(baseText);
            script1Content = parseScriptsToWordHtml(script1Content);
            
            let script2Content = "";
            let replacementEndIdx = script1End;
            if (hasSecondScript && script2Data) {
                script2Content = parseScriptsToWordHtml(script2Data.content);
                replacementEndIdx = script2Data.endIndex;
            }
            
            let replacement = "";
            if (hasSecondScript) {
                let subContent = isSup ? script2Content : script1Content;
                let supContent = isSup ? script1Content : script2Content;
                replacement = `<m:sSubSup><m:e>${baseText}</m:e><m:sub>${subContent}</m:sub><m:sup>${supContent}</m:sup></m:sSubSup>`;
            } else {
                if (isSup) {
                    replacement = `<m:sSup><m:e>${baseText}</m:e><m:sup>${script1Content}</m:sup></m:sSup>`;
                } else {
                    replacement = `<m:sSub><m:e>${baseText}</m:e><m:sub>${script1Content}</m:sub></m:sSub>`;
                }
            }
            
            let nextStr = f.substring(0, baseStart) + replacement + f.substring(replacementEndIdx);
            return parseScriptsToWordHtml(nextStr);
        }

        function parseFractionsToWordHtml(str) {
            let f = str;
            let index = f.indexOf('\\frac');
            while (index !== -1) {
                let numStart = f.indexOf('{', index);
                if (numStart === -1) break;
                let numEnd = findBalancedBrace(f, numStart);
                if (numEnd === -1) break;
                let num = f.substring(numStart + 1, numEnd);

                let denStart = f.indexOf('{', numEnd);
                if (denStart === -1 || denStart !== numEnd + 1) {
                    let spacesStr = f.substring(numEnd + 1);
                    let matchSpaces = spacesStr.match(/^\s*\{/);
                    if (matchSpaces) {
                        denStart = numEnd + 1 + spacesStr.indexOf('{');
                    } else {
                        break;
                    }
                }
                let denEnd = findBalancedBrace(f, denStart);
                if (denEnd === -1) break;
                let den = f.substring(denStart + 1, denEnd);

                num = parseFractionsToWordHtml(num);
                den = parseFractionsToWordHtml(den);

                let ommlFraction = `<m:f><m:fPr><m:type m:val="bar"/></m:fPr><m:num>${num}</m:num><m:den>${den}</m:den></m:f>`;
                f = f.substring(0, index) + ommlFraction + f.substring(denEnd + 1);
                index = f.indexOf('\\frac');
            }
            return f;
        }

        function parseRootsToWordHtml(str) {
            let f = str;
            let index = f.indexOf('\\sqrt');
            while (index !== -1) {
                let rest = f.substring(index + 5);
                let braceMatch = rest.match(/^\s*\{/);
                if (braceMatch) {
                    let numStart = index + 5 + rest.indexOf('{');
                    let numEnd = findBalancedBrace(f, numStart);
                    if (numEnd !== -1) {
                        let content = f.substring(numStart + 1, numEnd);
                        content = parseRootsToWordHtml(content);
                        let ommlRoot = `<m:rad><m:radPr><m:degHide m:val="on"/></m:radPr><m:e>${content}</m:e></m:rad>`;
                        f = f.substring(0, index) + ommlRoot + f.substring(numEnd + 1);
                        index = f.indexOf('\\sqrt');
                        continue;
                    }
                }
                
                let nextCharIdx = index + 5;
                while (nextCharIdx < f.length && /\s/.test(f[nextCharIdx])) {
                    nextCharIdx++;
                }
                if (nextCharIdx < f.length) {
                    let char = f[nextCharIdx];
                    let ommlRoot = `<m:rad><m:radPr><m:degHide m:val="on"/></m:radPr><m:e>${char}</m:e></m:rad>`;
                    f = f.substring(0, index) + ommlRoot + f.substring(nextCharIdx + 1);
                } else {
                    f = f.substring(0, index) + '√' + f.substring(index + 5);
                }
                index = f.indexOf('\\sqrt');
            }
            return f;
        }

        function wrapOmmlRuns(str) {
            let segments = str.split(/(<\/?[a-zA-Z0-9:]+(?:\s+[a-zA-Z0-9:]+="[^"]*")*\/?>)/);
            let result = "";
            for (let i = 0; i < segments.length; i++) {
                let seg = segments[i];
                if (!seg) continue;
                if (seg.startsWith('<') && seg.endsWith('>')) {
                    result += seg;
                } else {
                    let cleanSeg = seg
                        .replace(/&/g, '&amp;')
                        .replace(/</g, '&lt;')
                        .replace(/>/g, '&gt;');
                    result += `<m:r><m:t>${cleanSeg}</m:t></m:r>`;
                }
            }
            return result;
        }

        function cleanLaTeXFormula(formula) {
            let f = formula;
            f = f.replace(/\\text\s*\{([^}]+)\}/g, '$1');
            f = f.replace(/(?:\\t|\t)ext\s*\{?([^}]*)\}?/g, '$1');
            f = f.replace(/\bext([a-zA-Z]+)/g, ' $1');
            f = f.replace(/\\dot\s*\{([^}]+)\}/g, '$1̇');

            f = parseRootsToWordHtml(f);
            f = parseFractionsToWordHtml(f);
            f = parseScriptsToWordHtml(f);

            const replacements = [
                { regex: /\\in\b/g, replace: ' ∈ ' },
                { regex: /\\mathbb\{N\}/g, replace: 'ℕ' },
                { regex: /\\mathbb\s+N/g, replace: 'ℕ' },
                { regex: /\\mathbb\s+Z/g, replace: 'ℤ' },
                { regex: /\\setminus\b/g, replace: ' ∖ ' },
                { regex: /\\backslash\b/g, replace: ' ∖ ' },
                { regex: /\\cup\b/g, replace: ' ∪ ' },
                { regex: /\\cap\b/g, replace: ' ∩ ' },
                { regex: /\\theta\b/g, replace: 'θ' },
                { regex: /\\sin\b/g, replace: 'sin' },
                { regex: /\\cos\b/g, replace: 'cos' },
                { regex: /\\tan\b/g, replace: 'tan' },
                { regex: /\\cot\b/g, replace: 'cot' },
                { regex: /\\angle\b/g, replace: '∠' },
                { regex: /\\circ\b/g, replace: '°' },
                { regex: /\\triangle\b/g, replace: '△' },
                { regex: /\\le\b/g, replace: ' ≤ ' },
                { regex: /\\ge\b/g, replace: ' ≥ ' },
                { regex: /\\cdot\b/g, replace: '·' },
                { regex: /\\div\b/g, replace: ' ÷ ' },
                { regex: /\\times\b/g, replace: ' × ' },
                { regex: /\\approx\b/g, replace: ' ≈ ' },
                { regex: /\\neq\b/g, replace: ' ≠ ' },
                { regex: /\\pm\b/g, replace: ' ± ' },
                { regex: /\\infty\b/g, replace: ' ∞ ' },
                { regex: /\\alpha\b/g, replace: 'α' },
                { regex: /\\beta\b/g, replace: 'β' },
                { regex: /\\quad\b/g, replace: '   ' },
                { regex: /\\,/g, replace: ' ' },
                { regex: /\\;/g, replace: ' ' },
                { regex: /\\\{/g, replace: '{' },
                { regex: /\\\}/g, replace: '}' }
            ];

            replacements.forEach(item => {
                f = f.replace(item.regex, item.replace);
            });

            let wrapped = wrapOmmlRuns(f);
            return `<m:oMath>${wrapped}</m:oMath>`;
        }

        function convertMathToWordHtml(htmlContent) {
            let clean = htmlContent;

            clean = clean.replace(/\$\$([^\$]+)\$\$/g, (match, formula) => {
                let f = cleanLaTeXFormula(formula);
                return `<p style="text-align: center; margin: 6pt 0; font-family: 'Cambria Math', 'Times New Roman'; font-size: 11pt;">${f}</p>`;
            });

            clean = clean.replace(/\$([^\$]+)\$/g, (match, formula) => {
                let f = cleanLaTeXFormula(formula);
                return `<span style="font-family: 'Cambria Math', 'Times New Roman'; font-size: 11pt;">${f}</span>`;
            });

            return clean;
        }

        function cleanMcqLabel(label) {
            if (!label) return "";
            return String(label)
                .replace(/^[^\p{L}\p{N}\p{M}]+/gu, '')
                .replace(/[^\p{L}\p{N}\p{M}]+$/gu, '')
                .trim();
        }

        function generateWordExportHtml() {
            if (!paperState) return "";

            let html = "";

            // Header Section
            html += `
                <div style="text-align: center; margin-bottom: 8pt; page-break-inside: avoid;">
                    <p style="font-size: 16pt; font-weight: bold; margin: 0pt; padding: 0pt; line-height: 1.2;">${paperState.schoolName || ''}</p>
                    <p style="font-size: 12pt; font-weight: 600; margin: 3pt 0pt 0pt 0pt; padding: 0pt; color: #374151; line-height: 1.2;">${paperState.examTitle || ''}</p>
                    
                    <table width="100%" border="0" cellpadding="2" cellspacing="0" style="width: 100%; border-top: 2px solid #000; border-bottom: 2px solid #000; margin-top: 6pt; margin-bottom: 4pt; font-weight: 600; font-size: 10pt; border-collapse: collapse;">
                        <tr>
                            <td align="left" style="width: 25%; padding: 2px 0;">শ্রেণি: ${paperState.class || ''}</td>
                            <td align="center" style="width: 35%; padding: 2px 0;">বিষয়: ${paperState.subject || ''}</td>
                            <td align="center" style="width: 20%; padding: 2px 0;">পূর্ণমান: ${paperState.marks || ''}</td>
                            <td align="right" style="width: 20%; padding: 2px 0;">সময়: ${paperState.time || ''}</td>
                        </tr>
                    </table>
                    
                    ${paperState.instruction ? `<p style="font-size: 9.5pt; font-style: italic; margin: 3pt 0pt 0pt 0pt; text-align: center; color: #4b5563;">[${paperState.instruction}]</p>` : ''}
                </div>
            `;

            // Sections & Questions
            if (paperState.sections && paperState.sections.length > 0) {
                paperState.sections.forEach((sec) => {
                    html += `
                        <div style="margin-bottom: 8pt; page-break-inside: avoid;">
                            <table width="100%" border="0" cellpadding="2" cellspacing="0" style="width: 100%; border-bottom: 1px solid #000; background-color: #f1f5f9; margin-bottom: 4pt; border-collapse: collapse;">
                                <tr>
                                    <td align="left" style="font-weight: bold; font-size: 11pt; padding: 2px 4px;">${sec.title || ''}</td>
                                    <td align="right" style="font-weight: normal; font-size: 9.5pt; padding: 2px 4px;">${sec.instruction || ''}</td>
                                </tr>
                            </table>
                    `;

                    if (sec.questions && sec.questions.length > 0) {
                        sec.questions.forEach((q) => {
                            html += `
                                <div style="margin-bottom: 4pt; page-break-inside: avoid;">
                                    <p style="font-weight: 600; margin: 0pt 0pt 2pt 0pt; padding: 0pt; font-size: 10.5pt; line-height: 1.25;">
                                        <span>${q.number || ''}.</span> <span>${q.stem || ''}</span>
                                    </p>
                            `;

                            const currentLayout = q.layout || "1x1";
                            const parts = q.parts || [];

                            if (parts.length > 0) {
                                if (currentLayout === '1x4') {
                                    html += `<table width="100%" border="0" cellpadding="1" cellspacing="0" style="width: 100%; border-collapse: collapse; margin-left: 12pt;"><tr>`;
                                    parts.forEach((p) => {
                                        const cleanLbl = cleanMcqLabel(p.label);
                                        html += `<td width="25%" valign="top" style="width: 25%; font-size: 10pt;"><span class="mcq-label" style="font-family: 'NesarulOMR', 'Nikosh', 'Kalpurush', sans-serif; font-weight: 600;">${cleanLbl}</span> ${p.text}</td>`;
                                    });
                                    html += `</tr></table>`;
                                } else if (currentLayout === '2x2') {
                                    html += `<table width="100%" border="0" cellpadding="1" cellspacing="0" style="width: 100%; border-collapse: collapse; margin-left: 12pt;">`;
                                    for (let i = 0; i < parts.length; i += 2) {
                                        html += `<tr>`;
                                        const p1 = parts[i];
                                        const p2 = parts[i + 1];
                                        if (p1) {
                                            const cleanLbl1 = cleanMcqLabel(p1.label);
                                            html += `<td width="50%" valign="top" style="width: 50%; font-size: 10pt;"><span class="mcq-label" style="font-family: 'NesarulOMR', 'Nikosh', 'Kalpurush', sans-serif; font-weight: 600;">${cleanLbl1}</span> ${p1.text}</td>`;
                                        }
                                        if (p2) {
                                            const cleanLbl2 = cleanMcqLabel(p2.label);
                                            html += `<td width="50%" valign="top" style="width: 50%; font-size: 10pt;"><span class="mcq-label" style="font-family: 'NesarulOMR', 'Nikosh', 'Kalpurush', sans-serif; font-weight: 600;">${cleanLbl2}</span> ${p2.text}</td>`;
                                        } else {
                                            html += `<td width="50%"></td>`;
                                        }
                                        html += `</tr>`;
                                    }
                                    html += `</table>`;
                                } else {
                                    // 4x1 or 1x1
                                    parts.forEach((p) => {
                                        const cleanLbl = cleanMcqLabel(p.label);
                                        html += `<p style="font-size: 10pt; margin: 0pt 0pt 1.5pt 12pt; padding: 0pt; line-height: 1.25;"><span class="mcq-label" style="font-family: 'NesarulOMR', 'Nikosh', 'Kalpurush', sans-serif; font-weight: 600;">${cleanLbl}</span> ${p.text}</p>`;
                                    });
                                }
                            }

                            html += `</div>`;
                        });
                    }

                    html += `</div>`;
                });
            }

            // Convert MathJax $...$ formulas to Word OMML math
            html = convertMathToWordHtml(html);

            return html;
        }

        function exportToWord() {
            const examHtml = generateWordExportHtml();
            if (!examHtml) return;

            const header = "<html xmlns:o='urn:schemas-microsoft-com:office:office' " +
                "xmlns:w='urn:schemas-microsoft-com:office:word' " +
                "xmlns:m='http://schemas.microsoft.com/office/2004/12/omml' " +
                "xmlns='http://www.w3.org/TR/REC-html40'>" +
                "<head><title>Exam Paper</title>" +
                "<meta charset='utf-8'>" +
                "<!--[if gte mso 9]><xml><w:WordDocument><w:View>Print</w:View><w:Zoom>100</w:Zoom><w:DoNotOptimizeForBrowser/></w:WordDocument></xml><![endif]-->" +
                "<style>" +
                "@page { size: A4 landscape; margin: 0.5in; }" +
                "@page Section1 { size: 11.69in 8.27in; mso-page-orientation: landscape; margin: 0.5in 0.5in 0.5in 0.5in; mso-header-margin: 0.5in; mso-footer-margin: 0.5in; mso-paper-source: 0; mso-columns: 2 0.5in; }" +
                "div.Section1 { page: Section1; column-count: 2; -webkit-column-count: 2; column-gap: 0.5in; }" +
                "body { font-family: 'Nikosh', 'Kalpurush', 'SutonnyMJ', 'SolaimanLipi', sans-serif; font-size: 11pt; line-height: 1.25; color: #000000; background-color: #ffffff; }" +
                "p.MsoNormal, p, div, span, h1, h2, h3, h4 { margin: 0pt !important; margin-bottom: 0pt !important; mso-para-margin: 0pt !important; mso-para-margin-bottom: 0pt !important; padding: 0pt !important; }" +
                ".mcq-label { font-family: 'NesarulOMR', 'Nikosh', 'Kalpurush', sans-serif !important; font-weight: bold !important; }" +
                "table { border-collapse: collapse; }" +
                "th, td { font-family: 'Nikosh', 'Kalpurush', 'SutonnyMJ', 'SolaimanLipi', sans-serif; }" +
                "</style>" +
                "</head><body><div class='Section1'>";

            const footer = "</div></body></html>";
            const fileContent = header + examHtml + footer;

            const blob = new Blob(['\ufeff' + fileContent], {
                type: 'application/msword;charset=utf-8'
            });

            const cleanSchoolName = (paperState.schoolName || 'Exam_Paper').replace(/\s+/g, '_');
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `${cleanSchoolName}_Exam.doc`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }

        function checkLocalFileCORS() {
            if (window.location.protocol === 'file:') {
                const banner = document.getElementById("cors-warning-banner");
                if (banner) banner.classList.remove("hidden");
            }
        }

        window.addEventListener('load', function () {
            renderPaper();
            updateApiStatusUI();
            checkLocalFileCORS();
            setupDropZoneEvents();

            if (typeof google !== 'undefined') {
                google.accounts.id.initialize({
                    client_id: "7538259021-mockclientid.apps.googleusercontent.com",
                    callback: handleGoogleCredentialResponse
                });
            }
        });

        // ==========================================
        // PHOTO ENGINEERING JAVASCRIPT ENGINE
        // ==========================================
        const peState = {
            mode: 'single', // 'single' or 'dual'
            sizePreset: 'passport_bd',
            orientation: 'portrait',
            bgColor: '#1E6091',
            bgColorName: 'studio_blue',
            removeBg: true,
            autoFresh: true,
            sliders: {
                Brightness: 0,
                Contrast: 0,
                Smoothness: 0,
                Sharpness: 0,
                Saturation: 0
            },
            crop: {
                zoom: 1.0,
                panX: 0,
                panY: 0
            },
            dual: {
                layout: 'joint',
                scale1: 1.0,
                scale2: 1.0,
                gap: 0
            },
            file1: null,
            file1B64: null,
            file2: null,
            file2B64: null,
            resultB64: null,
            resultInfo: null,
            sheetSize: '4r',
            sheetB64: null,
            webcamTargetSlot: 1,
            webcamStream: null
        };

        const peSizeDetails = {
            passport_bd: { name: 'পাসপোর্ট (বাংলাদেশ) - ৪০x৫০ মিমি', w_mm: 40, h_mm: 50, w_px: 472, h_px: 591 },
            passport_intl: { name: 'আন্তর্জাতিক পাসপোর্ট - ৩৫x৪৫ মিমি', w_mm: 35, h_mm: 45, w_px: 413, h_px: 531 },
            passport_us: { name: 'ভিসা / ২x২ ইঞ্চি - ৫০.৮x৫০.৮ মিমি', w_mm: 50.8, h_mm: 50.8, w_px: 600, h_px: 600 },
            stamp: { name: 'স্ট্যাম্প সাইজ - ২০x২৫ মিমি', w_mm: 20, h_mm: 25, w_px: 236, h_px: 295 },
            '3r': { name: '৩-আর (3R) সাইজ - ৩.৫x৫.০ ইঞ্চি', w_mm: 88.9, h_mm: 127.0, w_px: 1050, h_px: 1500 },
            '4r': { name: '৪-আর (4R) সাইজ - ৪.০x৬.০ ইঞ্চি', w_mm: 101.6, h_mm: 152.4, w_px: 1200, h_px: 1800 },
            '10r': { name: '১০-আর (10R) সাইজ - ১০.০x১২.০ ইঞ্চি', w_mm: 254.0, h_mm: 304.8, w_px: 3000, h_px: 3600 },
            custom: { name: 'কাস্টম সাইজ', w_mm: 40, h_mm: 50, w_px: 472, h_px: 591 }
        };

        function peSetMode(mode) {
            peState.mode = mode;
            const singleBtn = document.getElementById('peModeSingleBtn');
            const dualBtn = document.getElementById('peModeDualBtn');
            const singleArea = document.getElementById('peSingleUploadArea');
            const dualArea = document.getElementById('peDualUploadArea');

            if (mode === 'single') {
                singleBtn.className = "px-4 py-2 rounded-lg font-bold text-sm transition bg-white text-blue-800 shadow";
                dualBtn.className = "px-4 py-2 rounded-lg font-bold text-sm transition text-white hover:bg-white/20";
                singleArea.classList.remove('hidden');
                dualArea.classList.add('hidden');
            } else {
                dualBtn.className = "px-4 py-2 rounded-lg font-bold text-sm transition bg-white text-blue-800 shadow";
                singleBtn.className = "px-4 py-2 rounded-lg font-bold text-sm transition text-white hover:bg-white/20";
                dualArea.classList.remove('hidden');
                singleArea.classList.add('hidden');
            }
        }

        function peHandleFileSelect(input, slot) {
            const file = input.files && input.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                const b64 = e.target.result;
                if (slot === 1) {
                    peState.file1 = file;
                    peState.file1B64 = b64;
                    // Update single preview thumbnail
                    document.getElementById('peDropContent1').classList.add('hidden');
                    document.getElementById('peThumbBox1').classList.remove('hidden');
                    document.getElementById('peThumbImg1').src = b64;
                    document.getElementById('peThumbName1').innerText = file.name;
                    document.getElementById('peThumbSize1').innerText = (file.size / (1024 * 1024)).toFixed(2) + ' MB';

                    // Update dual preview thumbnail 1
                    document.getElementById('peDualDropContent1').classList.add('hidden');
                    document.getElementById('peDualThumbBox1').classList.remove('hidden');
                    document.getElementById('peDualThumbImg1').src = b64;
                    document.getElementById('peDualThumbName1').innerText = file.name;

                    // Set compare original image
                    document.getElementById('peOriginalCompareImg').src = b64;
                } else if (slot === 2) {
                    peState.file2 = file;
                    peState.file2B64 = b64;
                    // Update dual preview thumbnail 2
                    document.getElementById('peDualDropContent2').classList.add('hidden');
                    document.getElementById('peDualThumbBox2').classList.remove('hidden');
                    document.getElementById('peDualThumbImg2').src = b64;
                    document.getElementById('peDualThumbName2').innerText = file.name;
                }
            };
            reader.readAsDataURL(file);
        }

        function peSelectSize(presetKey) {
            peState.sizePreset = presetKey;
            document.querySelectorAll('.pe-size-btn').forEach(btn => {
                btn.className = "pe-size-btn p-3 rounded-xl border-2 border-slate-200 bg-white text-slate-800 text-left hover:border-indigo-300 transition font-bold";
            });
            const activeBtn = document.getElementById('peSize_' + presetKey);
            if (activeBtn) {
                activeBtn.className = "pe-size-btn p-3 rounded-xl border-2 border-indigo-600 bg-indigo-50 text-indigo-900 text-left transition font-bold shadow-sm";
            }

            const customInputs = document.getElementById('peCustomSizeInputs');
            if (presetKey === 'custom') {
                customInputs.classList.remove('hidden');
            } else {
                customInputs.classList.add('hidden');
            }

            peUpdateInfoDisplay();
        }

        function peSetOrientation(orient) {
            peState.orientation = orient;
            const pBtn = document.getElementById('peOrientPortraitBtn');
            const lBtn = document.getElementById('peOrientLandscapeBtn');

            if (orient === 'portrait') {
                pBtn.className = "px-4 py-1.5 rounded-lg text-xs font-bold transition bg-white text-indigo-700 shadow-sm flex items-center gap-1.5";
                lBtn.className = "px-4 py-1.5 rounded-lg text-xs font-bold transition text-slate-600 hover:text-indigo-600 flex items-center gap-1.5";
            } else {
                lBtn.className = "px-4 py-1.5 rounded-lg text-xs font-bold transition bg-white text-indigo-700 shadow-sm flex items-center gap-1.5";
                pBtn.className = "px-4 py-1.5 rounded-lg text-xs font-bold transition text-slate-600 hover:text-indigo-600 flex items-center gap-1.5";
            }

            peUpdateInfoDisplay();
        }

        function peToggleRemoveBg(checked) {
            peState.removeBg = checked;
            const bgCtrls = document.getElementById('peBgColorControls');
            if (checked) {
                bgCtrls.style.opacity = '1';
                bgCtrls.style.pointerEvents = 'auto';
            } else {
                bgCtrls.style.opacity = '0.5';
                bgCtrls.style.pointerEvents = 'none';
            }
        }

        function peSelectBgColor(hex, key) {
            peState.bgColor = hex;
            peState.bgColorName = key;
            document.querySelectorAll('.pe-color-btn').forEach(btn => {
                btn.classList.remove('border-blue-600', 'bg-blue-50/50');
                btn.classList.add('border-slate-200');
            });
            const selBtn = document.getElementById('peColor_' + key);
            if (selBtn) {
                selBtn.classList.remove('border-slate-200');
                selBtn.classList.add('border-blue-600', 'bg-blue-50/50');
            }
            if (key === 'custom_color') {
                document.getElementById('peCustomHexVal').innerText = hex;
            }
            peUpdateInfoDisplay();
        }

        function peToggleAutoFresh() {
            peState.autoFresh = !peState.autoFresh;
            const btn = document.getElementById('peAutoFreshBtn');
            const badge = document.getElementById('peAutoFreshBadge');
            if (peState.autoFresh) {
                badge.innerText = 'চালু আছে';
                badge.className = 'ml-2 bg-white/20 text-white text-xs px-2 py-0.5 rounded-full font-extrabold';
                btn.className = 'w-full py-3 px-4 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-bold text-sm shadow-md flex items-center justify-center gap-2 transition-all transform active:scale-95';
            } else {
                badge.innerText = 'বন্ধ';
                badge.className = 'ml-2 bg-slate-300 text-slate-700 text-xs px-2 py-0.5 rounded-full font-extrabold';
                btn.className = 'w-full py-3 px-4 rounded-xl bg-slate-500 hover:bg-slate-600 text-white font-bold text-sm shadow flex items-center justify-center gap-2 transition-all';
            }
        }

        function peUpdateSliderVal(name) {
            const val = document.getElementById('peSlider' + name).value;
            peState.sliders[name] = parseInt(val);
            const valBadge = document.getElementById('peVal' + name);
            if (valBadge) {
                valBadge.innerText = (val > 0 ? '+' : '') + val;
            }
        }

        function peResetSliders() {
            ['Brightness', 'Contrast', 'Smoothness', 'Sharpness', 'Saturation'].forEach(name => {
                const slider = document.getElementById('peSlider' + name);
                if (slider) slider.value = 0;
                peState.sliders[name] = 0;
                const valBadge = document.getElementById('peVal' + name);
                if (valBadge) valBadge.innerText = '0';
            });
            peState.autoFresh = true;
            peToggleAutoFresh();
            peToggleAutoFresh(); // Ensures badge stays 'চালু আছে'
        }

        function peUpdateCropVal() {
            peState.crop.zoom = parseFloat(document.getElementById('peSliderZoom').value);
            peState.crop.panX = parseInt(document.getElementById('peSliderPanX').value);
            peState.crop.panY = parseInt(document.getElementById('peSliderPanY').value);

            document.getElementById('peValZoom').innerText = peState.crop.zoom.toFixed(1) + 'x';
            document.getElementById('peValPanX').innerText = (peState.crop.panX > 0 ? '+' : '') + peState.crop.panX + '%';
            document.getElementById('peValPanY').innerText = (peState.crop.panY > 0 ? '+' : '') + peState.crop.panY + '%';
        }

        function peResetCrop() {
            document.getElementById('peSliderZoom').value = 1.0;
            document.getElementById('peSliderPanX').value = 0;
            document.getElementById('peSliderPanY').value = 0;
            peUpdateCropVal();
        }

        function peSetDualLayout(layout) {
            peState.dual.layout = layout;
            const jointBtn = document.getElementById('peDualStyleJointBtn');
            const splitBtn = document.getElementById('peDualStyleSplitBtn');

            if (layout === 'joint') {
                jointBtn.className = "p-3 rounded-lg border-2 border-blue-600 bg-blue-50 text-blue-900 font-bold text-xs flex items-center justify-center gap-2";
                splitBtn.className = "p-3 rounded-lg border-2 border-slate-200 bg-white text-slate-700 font-bold text-xs flex items-center justify-center gap-2";
            } else {
                splitBtn.className = "p-3 rounded-lg border-2 border-blue-600 bg-blue-50 text-blue-900 font-bold text-xs flex items-center justify-center gap-2";
                jointBtn.className = "p-3 rounded-lg border-2 border-slate-200 bg-white text-slate-700 font-bold text-xs flex items-center justify-center gap-2";
            }
        }

        function peUpdateDualSliders() {
            peState.dual.scale1 = parseFloat(document.getElementById('peScale1').value);
            peState.dual.scale2 = parseFloat(document.getElementById('peScale2').value);
            peState.dual.gap = parseInt(document.getElementById('peGap').value);

            document.getElementById('peScale1Val').innerText = peState.dual.scale1.toFixed(2) + 'x';
            document.getElementById('peScale2Val').innerText = peState.dual.scale2.toFixed(2) + 'x';
            document.getElementById('peGapVal').innerText = peState.dual.gap + 'px';
        }

        function peUpdateInfoDisplay() {
            const p = peSizeDetails[peState.sizePreset] || peSizeDetails.passport_bd;
            let w = p.w_px;
            let h = p.h_px;
            if (peState.orientation === 'landscape' && w < h) {
                const temp = w; w = h; h = temp;
            }

            document.getElementById('peInfoSizeName').innerText = p.name + (peState.orientation === 'landscape' ? ' (ল্যান্ডস্কেপ)' : '');
            document.getElementById('peInfoResolution').innerText = `${w} x ${h} পিক্সেল (৩০০ DPI)`;

            let bgText = 'স্টুডিও ক্লাসিক ব্লু';
            if (peState.bgColor === '#0047AB') bgText = 'রয়েল ব্লু';
            else if (peState.bgColor === '#2B78E4') bgText = 'উজ্জ্বল ব্লু';
            else if (peState.bgColor === '#85C1E9') bgText = 'আকাশি ব্লু';
            else if (peState.bgColor === '#FFFFFF') bgText = 'সাদা (অফিশিয়াল/ভিসা)';
            else if (peState.bgColor === '#E5E7EB') bgText = 'হালকা ধূসর';
            else if (peState.bgColor === 'transparent') bgText = 'স্বচ্ছ (PNG)';
            else if (peState.bgColorName === 'custom_color') bgText = `কাস্টম (${peState.bgColor})`;

            if (!peState.removeBg) bgText = 'মূল ব্যাকগ্রাউন্ড অক্ষুণ্ণ';
            document.getElementById('peInfoBgColor').innerText = bgText;
        }

        async function peProcessPhoto() {
            if (peState.mode === 'single' && !peState.file1B64) {
                alert('দয়া করে প্রথমে একটি ছবি আপলোড করুন বা ক্যামেরা দিয়ে ছবি তুলুন।');
                return;
            }
            if (peState.mode === 'dual' && (!peState.file1B64 || !peState.file2B64)) {
                alert('দুটি ছবি একসাথে করার জন্য দয়া করে দুটি ছবিই নির্বাচন করুন।');
                return;
            }

            const loading = document.getElementById('peLoadingOverlay');
            const procBtn = document.getElementById('peProcessBtn');
            loading.classList.remove('hidden');
            procBtn.disabled = true;

            try {
                const payload = {
                    mode: peState.mode,
                    size_preset: peState.sizePreset,
                    orientation: peState.orientation,
                    custom_w: document.getElementById('peCustomW')?.value || 40,
                    custom_h: document.getElementById('peCustomH')?.value || 50,
                    custom_unit: document.getElementById('peCustomUnit')?.value || 'mm',
                    bg_color: peState.removeBg ? peState.bgColor : 'original',
                    remove_bg: peState.removeBg,
                    auto_fresh: peState.autoFresh,
                    brightness: peState.sliders.Brightness,
                    contrast: peState.sliders.Contrast,
                    smoothness: peState.sliders.Smoothness,
                    sharpness: peState.sliders.Sharpness,
                    saturation: peState.sliders.Saturation,
                    crop_scale: peState.crop.zoom,
                    pan_x: peState.crop.panX,
                    pan_y: peState.crop.panY,
                    dual_layout: peState.dual.layout,
                    scale1: peState.dual.scale1,
                    pos_x1: 0,
                    scale2: peState.dual.scale2,
                    pos_x2: 0,
                    gap: peState.dual.gap,
                    image1_b64: peState.file1B64,
                    image2_b64: peState.file2B64
                };

                const res = await fetch('/photo_engineer/process', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const data = await res.json();
                if (!res.ok || data.error) {
                    throw new Error(data.error || 'ছবি প্রসেস করতে ব্যর্থ হয়েছে।');
                }

                peState.resultB64 = data.result_b64;
                peState.resultInfo = data;

                // Show in preview
                document.getElementById('pePreviewPlaceholder').classList.add('hidden');
                document.getElementById('peResultWrapper').classList.remove('hidden');
                document.getElementById('peResultImg').src = data.result_b64;

                // Enable buttons
                document.getElementById('peDownloadJpgBtn').disabled = false;
                document.getElementById('peDownloadPngBtn').disabled = false;
                document.getElementById('pePrintSheetBtn').disabled = false;
                document.getElementById('peDirectPrintBtn').disabled = false;

                // Update info badge
                document.getElementById('peInfoSizeName').innerText = data.size_name;
                document.getElementById('peInfoResolution').innerText = `${data.width_px} x ${data.height_px} পিক্সেল (${data.dpi} DPI)`;

            } catch (err) {
                alert('ত্রুটি: ' + err.message);
            } finally {
                loading.classList.add('hidden');
                procBtn.disabled = false;
            }
        }

        function peShowOriginal(show) {
            const comp = document.getElementById('peOriginalCompareImg');
            if (comp) {
                if (show) comp.classList.remove('hidden');
                else comp.classList.add('hidden');
            }
        }

        async function peDownloadFile(format) {
            if (!peState.resultB64) return;
            try {
                const res = await fetch('/photo_engineer/download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        image_b64: peState.resultB64,
                        filename: `Photo_Studio_${peState.sizePreset}_HD`,
                        format: format
                    })
                });

                if (!res.ok) throw new Error('ডাউনলোড ব্যর্থ হয়েছে।');
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `Photo_Studio_${peState.sizePreset}_HD.${format}`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            } catch (err) {
                alert(err.message);
            }
        }

        function peOpenPrintSheetModal() {
            if (!peState.resultB64) return;
            document.getElementById('pePrintSheetModal').classList.remove('hidden');
            peGeneratePrintSheet();
        }

        function peClosePrintSheetModal() {
            document.getElementById('pePrintSheetModal').classList.add('hidden');
        }

        function peSetSheetSize(size) {
            peState.sheetSize = size;
            const btn4r = document.getElementById('peSheet4RBtn');
            const btnA4 = document.getElementById('peSheetA4Btn');
            if (size === '4r') {
                btn4r.className = "px-3 py-1 rounded text-xs font-bold bg-blue-600 text-white shadow-sm";
                btnA4.className = "px-3 py-1 rounded text-xs font-bold text-slate-600 hover:text-blue-600";
            } else {
                btnA4.className = "px-3 py-1 rounded text-xs font-bold bg-blue-600 text-white shadow-sm";
                btn4r.className = "px-3 py-1 rounded text-xs font-bold text-slate-600 hover:text-blue-600";
            }
            peGeneratePrintSheet();
        }

        async function peGeneratePrintSheet() {
            if (!peState.resultB64) return;
            const loader = document.getElementById('peSheetLoading');
            const preview = document.getElementById('peSheetPreviewImg');
            loader.classList.remove('hidden');
            preview.classList.add('hidden');

            try {
                const border = document.getElementById('peSheetBorderToggle').checked;
                const res = await fetch('/photo_engineer/print_sheet', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        image_b64: peState.resultB64,
                        sheet_size: peState.sheetSize,
                        border: border
                    })
                });

                const data = await res.json();
                if (!res.ok || data.error) throw new Error(data.error || 'শিট তৈরি করতে ব্যর্থ।');

                peState.sheetB64 = data.sheet_b64;
                preview.src = data.sheet_b64;
                preview.classList.remove('hidden');
            } catch (err) {
                alert('ত্রুটি: ' + err.message);
            } finally {
                loader.classList.add('hidden');
            }
        }

        function peDownloadPrintSheet() {
            if (!peState.sheetB64) return;
            const a = document.createElement('a');
            a.href = peState.sheetB64;
            a.download = `Print_Sheet_${peState.sheetSize.toUpperCase()}_300DPI.jpg`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }

        function pePrintSheetNow() {
            if (!peState.sheetB64) return;
            const w = window.open('');
            w.document.write(`<html><head><title>Print Sheet</title><style>@page{size:auto;margin:0;}body{margin:0;padding:0;text-align:center;}img{max-width:100%;height:auto;}</style></head><body><img src="${peState.sheetB64}" onload="window.print();window.close();" /></body></html>`);
            w.document.close();
        }

        function peDirectPrint() {
            if (!peState.resultB64) return;
            const w = window.open('');
            w.document.write(`<html><head><title>Print Photo</title><style>@page{size:auto;margin:10mm;}body{margin:0;padding:20px;text-align:center;}img{max-width:100%;max-height:90vh;border:1px solid #ddd;}</style></head><body><img src="${peState.resultB64}" onload="window.print();window.close();" /></body></html>`);
            w.document.close();
        }

        // --- WEBCAM FUNCTIONS ---
        async function peOpenWebcam(slot) {
            peState.webcamTargetSlot = slot;
            const modal = document.getElementById('peWebcamModal');
            modal.classList.remove('hidden');

            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: 'user' }
                });
                peState.webcamStream = stream;
                const video = document.getElementById('peWebcamVideo');
                video.srcObject = stream;
            } catch (err) {
                alert('ক্যামেরা চালু করতে সমস্যা হয়েছে: ' + err.message);
                peCloseWebcam();
            }
        }

        function peCloseWebcam() {
            if (peState.webcamStream) {
                peState.webcamStream.getTracks().forEach(t => t.stop());
                peState.webcamStream = null;
            }
            document.getElementById('peWebcamModal').classList.add('hidden');
        }

        function peCaptureWebcam() {
            const video = document.getElementById('peWebcamVideo');
            const canvas = document.getElementById('peWebcamCanvas');
            const flash = document.getElementById('peWebcamFlash');

            // Flash effect
            flash.classList.remove('hidden');
            setTimeout(() => flash.classList.add('hidden'), 200);

            canvas.width = video.videoWidth || 640;
            canvas.height = video.videoHeight || 480;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            const b64 = canvas.toDataURL('image/jpeg', 0.95);
            const slot = peState.webcamTargetSlot;

            if (slot === 1) {
                peState.file1 = null;
                peState.file1B64 = b64;
                document.getElementById('peDropContent1').classList.add('hidden');
                document.getElementById('peThumbBox1').classList.remove('hidden');
                document.getElementById('peThumbImg1').src = b64;
                document.getElementById('peThumbName1').innerText = 'Webcam_Capture.jpg';
                document.getElementById('peThumbSize1').innerText = 'HD Camera Photo';

                document.getElementById('peDualDropContent1').classList.add('hidden');
                document.getElementById('peDualThumbBox1').classList.remove('hidden');
                document.getElementById('peDualThumbImg1').src = b64;
                document.getElementById('peDualThumbName1').innerText = 'Webcam_Capture.jpg';

                document.getElementById('peOriginalCompareImg').src = b64;
            } else if (slot === 2) {
                peState.file2 = null;
                peState.file2B64 = b64;
                document.getElementById('peDualDropContent2').classList.add('hidden');
                document.getElementById('peDualThumbBox2').classList.remove('hidden');
                document.getElementById('peDualThumbImg2').src = b64;
                document.getElementById('peDualThumbName2').innerText = 'Webcam_Capture_2.jpg';
            }

            peCloseWebcam();
        }

        // Setup drag and drop for Photo Engineering
        function peSetupDropZones() {
            const dropzone1 = document.getElementById('peDropzone1');
            if (!dropzone1) return;

            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropzone1.addEventListener(eventName, e => {
                    e.preventDefault();
                    e.stopPropagation();
                }, false);
            });

            ['dragenter', 'dragover'].forEach(eventName => {
                dropzone1.addEventListener(eventName, () => dropzone1.classList.add('border-blue-600', 'bg-blue-100/50'), false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                dropzone1.addEventListener(eventName, () => dropzone1.classList.remove('border-blue-600', 'bg-blue-100/50'), false);
            });

            dropzone1.addEventListener('drop', e => {
                const dt = e.dataTransfer;
                const files = dt.files;
                if (files && files[0]) {
                    peHandleFileSelect({ files: [files[0]] }, 1);
                }
            });
        }

        window.addEventListener('DOMContentLoaded', peSetupDropZones);

    
        // ==========================================
        // ADMIN AUTH & SETTINGS STATE AND LOGIC
        // ==========================================
        const adminState = {
            isLoggedIn: false,
            user: "Danam",
            keys: [], // array of { key: string, label: string, status: string }
            prompts: {
                passport: `Professional official passport and office ID photo restoration at 300 DPI high resolution.
[STRICT IDENTITY PRESERVATION - ZERO DISTORTION]: Strictly preserve 100% authentic facial identity, exact bone structure, genuine eye shape, nose contours, lip lines, and natural expression of the original person. Under NO circumstance should the face be distorted, morphed, swapped, or artificially beautified. No plastic or cartoonish AI look.
[BLUR & CLARITY RESTORATION]: Clean and deblur out-of-focus, blurry, low-resolution, or noisy photos. Reconstruct razor-sharp optical clarity in eyes, iris, eyelashes, eyebrows, lips, and hair strands while retaining authentic skin pores and texture.
[SMART FACE-CENTERED OFFICE FRAMING]: If the input is a full-body, half-body, or wide photo, automatically crop and frame the face and upper chest in standard formal portrait composition. Face height must occupy 65% to 75% of the total photo height with balanced headroom (8-10% space above hair), perfectly centered for formal office and passport submission.
[STUDIO LIGHTING & BACKGROUND]: Balanced studio softbox illumination, remove harsh shadows and uneven glare. Set uniform solid studio blue background (#1E6091). Neat formal attire, crisp and clean studio finish.`,
                fresh: `Ultra-high-definition studio photo fresh restoration and enhancement (300 DPI / 4K fidelity).
[PRESERVE ORIGINAL FACE & IDENTITY]: Keep the real face, identity, age, expression, and distinct facial structure 100% unaltered. Zero facial warping, zero morphing, zero unnatural alteration.
[DEBLUR & RESOLUTION ENHANCEMENT]: Remove motion blur, camera shake, low-light noise, compression artifacts, and optical haziness. Sharpen micro-details in eyes, hair, and edges naturally without over-smoothing or plastic filtering.
[BLEMISH CLEANUP & NATURAL FRESHNESS]: Gently clean temporary blemishes, pimples, dust specks, and fatigue marks while preserving genuine skin texture and natural skin tone.
[STUDIO FINISH]: Change background to solid classic studio blue (#1E6091) or cyan blue as selected. Optimize lighting, contrast, and healthy skin vibrance for formal office and submission readiness.`,
                joint: `High-definition formal joint portrait photography of two individuals at 300 DPI.
[TWO-PERSON FACIAL INTEGRITY]: Strictly preserve the 100% authentic facial features, individual identities, and natural expressions of both persons without any cross-morphing or distortion.
[SMART COMPOSITION & FRAMING]: If input photos are full-body or unevenly sized, intelligently extract and balance both heads and upper torsos side by side at matching eye levels and natural proportions (upper chest to top of hair).
[DEBLUR & UNIFIED STUDIO FINISH]: Deblur and sharpen both faces equally. Seamlessly unite both subjects against a solid professional studio blue background (#1E6091) with harmonious soft studio lighting.`,
                stamp: `Official miniature stamp size portrait (20x25 mm) engineered for ultra-crisp physical print at 300 DPI.
[MICRO-SHARPNESS & DEBLUR]: High micro-contrast and edge enhancement designed specifically so facial features remain clear and sharp even at small stamp dimensions. Fix blurry input images.
[IDENTITY & CLOSE FRAMING]: 100% true-to-life face without distortion. Centered close-up framing of head, neck, and upper collar with balanced headroom. Solid clean studio blue background.`,
                question: `You are an expert examiner and teacher. Convert raw math exam text, questions, images, or PDF documents into clean structured JSON format with schoolName, examTitle, class, subject, marks, time, instruction, and sections.`,
                custom: `Master studio portrait enhancement and restoration.
[CORE MANDATE]: 100% authentic facial identity preservation; zero distortion, zero morphing of the real person.
[PROCESSING]: Remove blur, noise, and artifacts; restore crisp optical focus; smart framing of head and shoulders; natural skin pores and realistic lighting; solid studio background; office and official documentation standard.`
            },
            defaultPrompts: {
                passport: `Professional official passport and office ID photo restoration at 300 DPI high resolution.
[STRICT IDENTITY PRESERVATION - ZERO DISTORTION]: Strictly preserve 100% authentic facial identity, exact bone structure, genuine eye shape, nose contours, lip lines, and natural expression of the original person. Under NO circumstance should the face be distorted, morphed, swapped, or artificially beautified. No plastic or cartoonish AI look.
[BLUR & CLARITY RESTORATION]: Clean and deblur out-of-focus, blurry, low-resolution, or noisy photos. Reconstruct razor-sharp optical clarity in eyes, iris, eyelashes, eyebrows, lips, and hair strands while retaining authentic skin pores and texture.
[SMART FACE-CENTERED OFFICE FRAMING]: If the input is a full-body, half-body, or wide photo, automatically crop and frame the face and upper chest in standard formal portrait composition. Face height must occupy 65% to 75% of the total photo height with balanced headroom (8-10% space above hair), perfectly centered for formal office and passport submission.
[STUDIO LIGHTING & BACKGROUND]: Balanced studio softbox illumination, remove harsh shadows and uneven glare. Set uniform solid studio blue background (#1E6091). Neat formal attire, crisp and clean studio finish.`,
                fresh: `Ultra-high-definition studio photo fresh restoration and enhancement (300 DPI / 4K fidelity).
[PRESERVE ORIGINAL FACE & IDENTITY]: Keep the real face, identity, age, expression, and distinct facial structure 100% unaltered. Zero facial warping, zero morphing, zero unnatural alteration.
[DEBLUR & RESOLUTION ENHANCEMENT]: Remove motion blur, camera shake, low-light noise, compression artifacts, and optical haziness. Sharpen micro-details in eyes, hair, and edges naturally without over-smoothing or plastic filtering.
[BLEMISH CLEANUP & NATURAL FRESHNESS]: Gently clean temporary blemishes, pimples, dust specks, and fatigue marks while preserving genuine skin texture and natural skin tone.
[STUDIO FINISH]: Change background to solid classic studio blue (#1E6091) or cyan blue as selected. Optimize lighting, contrast, and healthy skin vibrance for formal office and submission readiness.`,
                joint: `High-definition formal joint portrait photography of two individuals at 300 DPI.
[TWO-PERSON FACIAL INTEGRITY]: Strictly preserve the 100% authentic facial features, individual identities, and natural expressions of both persons without any cross-morphing or distortion.
[SMART COMPOSITION & FRAMING]: If input photos are full-body or unevenly sized, intelligently extract and balance both heads and upper torsos side by side at matching eye levels and natural proportions (upper chest to top of hair).
[DEBLUR & UNIFIED STUDIO FINISH]: Deblur and sharpen both faces equally. Seamlessly unite both subjects against a solid professional studio blue background (#1E6091) with harmonious soft studio lighting.`,
                stamp: `Official miniature stamp size portrait (20x25 mm) engineered for ultra-crisp physical print at 300 DPI.
[MICRO-SHARPNESS & DEBLUR]: High micro-contrast and edge enhancement designed specifically so facial features remain clear and sharp even at small stamp dimensions. Fix blurry input images.
[IDENTITY & CLOSE FRAMING]: 100% true-to-life face without distortion. Centered close-up framing of head, neck, and upper collar with balanced headroom. Solid clean studio blue background.`,
                question: `You are an expert examiner and teacher. Convert raw math exam text, questions, images, or PDF documents into clean structured JSON format with schoolName, examTitle, class, subject, marks, time, instruction, and sections.`,
                custom: `Master studio portrait enhancement and restoration.
[CORE MANDATE]: 100% authentic facial identity preservation; zero distortion, zero morphing of the real person.
[PROCESSING]: Remove blur, noise, and artifacts; restore crisp optical focus; smart framing of head and shoulders; natural skin pores and realistic lighting; solid studio background; office and official documentation standard.`
            }
        };

        // Open & Close Login Modal
        function openLoginModal() {
            document.getElementById('adminLoginModal').classList.remove('hidden');
            document.getElementById('loginErrorMsg').classList.add('hidden');
            document.getElementById('adminUserIdInput').focus();
        }

        function closeLoginModal() {
            document.getElementById('adminLoginModal').classList.add('hidden');
        }

        // Handle Login Submission
        async function handleAdminLogin(e) {
            e.preventDefault();
            const userId = document.getElementById('adminUserIdInput').value.trim();
            const password = document.getElementById('adminPasswordInput').value.trim();
            const errBox = document.getElementById('loginErrorMsg');
            const submitBtn = document.getElementById('adminLoginSubmitBtn');

            errBox.classList.add('hidden');
            submitBtn.disabled = true;

            try {
                // Call server auth endpoint
                const res = await fetch('/api/admin/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: userId, password: password })
                });
                const data = await res.json();

                if (res.ok && data.success) {
                    adminState.isLoggedIn = true;
                    adminState.user = data.user || 'Danam';
                    localStorage.setItem('danam_admin_logged_in', 'true');

                    closeLoginModal();
                    updateAdminHeaderUI();
                    customAlert('সফল লগইন', `স্বাগতম ${adminState.user}! আপনি সফলভাবে অ্যাডমিন হিসেবে লগইন করেছেন। এখন আপনি প্রম্পট ও Gemini API Keys পরিচালনা করতে পারবেন।`);
                    openAdminSettingsModal();
                } else {
                    errBox.innerText = data.error || 'ভুল ইউজার আইডি বা পাসওয়ার্ড!';
                    errBox.classList.remove('hidden');
                }
            } catch (err) {
                // Client-side fallback if server offline
                if (userId.toLowerCase() === 'danam' && password === 'Danam') {
                    adminState.isLoggedIn = true;
                    localStorage.setItem('danam_admin_logged_in', 'true');
                    closeLoginModal();
                    updateAdminHeaderUI();
                    customAlert('সফল লগইন', 'স্বাগতম Danam! আপনি সফলভাবে লগইন করেছেন।');
                    openAdminSettingsModal();
                } else {
                    errBox.innerText = 'ভুল User Id বা Password! সঠিক তথ্য দিন (User Id: Danam, Password: Danam)';
                    errBox.classList.remove('hidden');
                }
            } finally {
                submitBtn.disabled = false;
            }
        }

        function adminLogout() {
            adminState.isLoggedIn = false;
            localStorage.removeItem('danam_admin_logged_in');
            updateAdminHeaderUI();
            customAlert('লগআউট', 'আপনি সফলভাবে লগআউট করেছেন।');
        }

        function updateAdminHeaderUI() {
            const loginBtn = document.getElementById('headerLoginBtn');
            const loggedInBar = document.getElementById('headerLoggedInBar');

            if (adminState.isLoggedIn) {
                if (loginBtn) loginBtn.classList.add('hidden');
                if (loggedInBar) loggedInBar.classList.remove('hidden');
            } else {
                if (loginBtn) loginBtn.classList.remove('hidden');
                if (loggedInBar) loggedInBar.classList.add('hidden');
            }
        }

        // Open & Close Admin Settings Modal
        function openAdminSettingsModal() {
            if (!adminState.isLoggedIn) {
                openLoginModal();
                return;
            }
            document.getElementById('adminSettingsModal').classList.remove('hidden');
            loadAdminSettings();
            switchAdminTab('keys');
        }

        function closeAdminSettingsModal() {
            document.getElementById('adminSettingsModal').classList.add('hidden');
        }

        function switchAdminTab(tabName) {
            const keysBtn = document.getElementById('adminTabKeysBtn');
            const promptsBtn = document.getElementById('adminTabPromptsBtn');
            const panelKeys = document.getElementById('adminPanelKeys');
            const panelPrompts = document.getElementById('adminPanelPrompts');

            if (tabName === 'keys') {
                keysBtn.className = "py-2.5 px-4 rounded-t-xl font-bold text-xs md:text-sm transition flex items-center gap-2 border-b-2 border-indigo-600 bg-white text-indigo-700 shadow-sm cursor-pointer";
                promptsBtn.className = "py-2.5 px-4 rounded-t-xl font-bold text-xs md:text-sm transition flex items-center gap-2 border-b-2 border-transparent text-slate-500 hover:text-indigo-600 cursor-pointer";
                panelKeys.classList.remove('hidden');
                panelPrompts.classList.add('hidden');
            } else {
                promptsBtn.className = "py-2.5 px-4 rounded-t-xl font-bold text-xs md:text-sm transition flex items-center gap-2 border-b-2 border-indigo-600 bg-white text-indigo-700 shadow-sm cursor-pointer";
                keysBtn.className = "py-2.5 px-4 rounded-t-xl font-bold text-xs md:text-sm transition flex items-center gap-2 border-b-2 border-transparent text-slate-500 hover:text-indigo-600 cursor-pointer";
                panelPrompts.classList.remove('hidden');
                panelKeys.classList.add('hidden');
            }
        }

        // Load Settings from Server / LocalStorage
        async function loadAdminSettings() {
            try {
                const res = await fetch('/api/admin/settings');
                if (res.ok) {
                    const data = await res.json();
                    if (data.settings) {
                        if (data.settings.prompts) {
                            adminState.prompts = Object.assign({}, adminState.defaultPrompts, data.settings.prompts);
                        }
                        if (data.settings.gemini_api_keys) {
                            adminState.keys = data.settings.gemini_api_keys.map((item, idx) => {
                                if (typeof item === 'string') {
                                    return { key: item, label: `Key ${idx + 1}`, status: 'untested' };
                                }
                                return { key: item.key, label: item.label || `Key ${idx + 1}`, status: 'untested' };
                            });
                        }
                    }
                }
            } catch (err) {
                console.log('Using local cached settings:', err);
                const localKeys = localStorage.getItem('danam_gemini_keys');
                if (localKeys) {
                    try { adminState.keys = JSON.parse(localKeys); } catch(e){}
                }
            }

            // Populate prompts textareas
            for (const [key, val] of Object.entries(adminState.prompts)) {
                const el = document.getElementById('promptInput_' + key);
                if (el) el.value = val;
            }

            renderAdminKeysList();
        }

        // Render API Keys List
        function renderAdminKeysList() {
            const list = document.getElementById('adminKeysList');
            const countBadge = document.getElementById('adminKeyCountBadge');
            const statusBadge = document.getElementById('adminKeyPoolStatus');

            countBadge.innerText = adminState.keys.length;
            statusBadge.innerText = `${adminState.keys.length}টি সংরক্ষিত (অটো-রোলেশন সচল)`;

            if (adminState.keys.length === 0) {
                list.innerHTML = `
                    <div class="p-6 text-center bg-slate-50 rounded-xl border border-dashed border-slate-300 text-slate-400 text-xs">
                        কোনো Gemini API Key যুক্ত করা নেই। উপরে নতুন কী দিয়ে "কী যুক্ত করুন" বাটনে চাপুন।
                    </div>
                `;
                return;
            }

            let html = '';
            adminState.keys.forEach((k, idx) => {
                const masked = k.key.length > 10 ? k.key.slice(0, 7) + '••••••••••••' + k.key.slice(-4) : k.key;
                let statusBadgeHtml = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-600">টেস্ট করা হয়নি</span>';
                if (k.status === 'valid') {
                    statusBadgeHtml = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">🟢 সক্রিয় ও সচল</span>';
                } else if (k.status === 'invalid') {
                    statusBadgeHtml = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-red-100 text-red-800">🔴 ইনভ্যালিড / লিমিট শেষ</span>';
                } else if (k.status === 'testing') {
                    statusBadgeHtml = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">⏳ পরীক্ষা করা হচ্ছে...</span>';
                }

                html += `
                    <div class="p-3.5 bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                        <div class="flex items-center gap-3">
                            <span class="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold text-xs flex-shrink-0">
                                ${idx + 1}
                            </span>
                            <div>
                                <div class="flex items-center gap-2">
                                    <span class="font-bold text-xs md:text-sm text-slate-800">${k.label}</span>
                                    ${statusBadgeHtml}
                                </div>
                                <div class="font-mono text-xs text-slate-500 mt-0.5 select-all">${masked}</div>
                            </div>
                        </div>
                        <div class="flex items-center gap-2 self-end sm:self-auto">
                            <button type="button" onclick="adminTestApiKey(${idx})"
                                class="px-3 py-1.5 bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 rounded-lg text-xs font-bold transition flex items-center gap-1 cursor-pointer">
                                <span>🧪</span> টেস্ট করুন
                            </button>
                            <button type="button" onclick="adminDeleteApiKey(${idx})"
                                class="px-2.5 py-1.5 bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 rounded-lg text-xs font-bold transition flex items-center gap-1 cursor-pointer">
                                <span>🗑️</span> মুছুন
                            </button>
                        </div>
                    </div>
                `;
            });
            list.innerHTML = html;
        }

        // Add API Key
        function adminAddApiKey() {
            const keyInput = document.getElementById('adminNewKeyInput');
            const labelInput = document.getElementById('adminNewKeyLabel');
            const keyVal = keyInput.value.trim();
            const labelVal = labelInput.value.trim() || `Gemini Key ${adminState.keys.length + 1}`;

            if (!keyVal) {
                alert('দয়া করে একটি Gemini API Key পেস্ট করুন!');
                return;
            }

            // Check if already exists
            if (adminState.keys.some(k => k.key === keyVal)) {
                alert('এই Gemini API Key ইতিমধ্যে যুক্ত রয়েছে!');
                return;
            }

            adminState.keys.push({
                key: keyVal,
                label: labelVal,
                status: 'untested'
            });

            keyInput.value = '';
            labelInput.value = '';

            renderAdminKeysList();
            adminSaveAllSettings(true);
        }

        // Delete API Key
        function adminDeleteApiKey(idx) {
            if (confirm('আপনি কি এই Gemini API Key মুছে ফেলতে চান?')) {
                adminState.keys.splice(idx, 1);
                renderAdminKeysList();
                adminSaveAllSettings(true);
            }
        }

        // Test API Key
        async function adminTestApiKey(idx) {
            const keyObj = adminState.keys[idx];
            if (!keyObj) return;

            keyObj.status = 'testing';
            renderAdminKeysList();

            try {
                const res = await fetch('/api/admin/test_key', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ api_key: keyObj.key })
                });
                const data = await res.json();
                if (res.ok && data.success) {
                    keyObj.status = 'valid';
                    renderAdminKeysList();
                    customAlert('টেস্ট সফল!', `কী "${keyObj.label}" সক্রিয় এবং গুগলের সাথে সফলভাবে যুক্ত রয়েছে!`);
                } else {
                    keyObj.status = 'invalid';
                    renderAdminKeysList();
                    customAlert('টেস্ট ব্যর্থ', data.error || 'এই কী দিয়ে রিকোয়েস্ট সফল হয়নি। কোটা শেষ বা ইনভ্যালিড কী।');
                }
            } catch (err) {
                keyObj.status = 'invalid';
                renderAdminKeysList();
                customAlert('টেস্ট ত্রুটি', err.message);
            }
        }

        // Reset Prompt
        function adminResetPrompt(key) {
            if (adminState.defaultPrompts[key]) {
                const el = document.getElementById('promptInput_' + key);
                if (el) el.value = adminState.defaultPrompts[key];
                adminState.prompts[key] = adminState.defaultPrompts[key];
            }
        }

        // Save All Settings
        async function adminSaveAllSettings(silent = false) {
            // Read all prompts from textareas
            ['passport', 'fresh', 'joint', 'stamp', 'custom', 'question'].forEach(k => {
                const el = document.getElementById('promptInput_' + k);
                if (el) adminState.prompts[k] = el.value.trim();
            });

            // Save to localStorage for instant client offline access
            localStorage.setItem('danam_gemini_keys', JSON.stringify(adminState.keys));
            localStorage.setItem('danam_prompts', JSON.stringify(adminState.prompts));

            // Also sync primary active key to custom_gemini_api_key for Tab 4 compatibility
            if (adminState.keys.length > 0) {
                localStorage.setItem('custom_gemini_api_key', adminState.keys[0].key);
            }

            try {
                const payload = {
                    gemini_api_keys: adminState.keys.map(k => ({ key: k.key, label: k.label })),
                    prompts: adminState.prompts
                };

                const res = await fetch('/api/admin/settings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();

                if (res.ok && data.success) {
                    if (!silent) {
                        customAlert('সফলভাবে সংরক্ষিত', 'সকল ছবি তৈরির প্রম্পট ও Gemini API কী সফলভাবে সংরক্ষিত হয়েছে!');
                    }
                }
            } catch (err) {
                if (!silent) {
                    customAlert('সংরক্ষিত', 'সেটিংস ব্রাউজারে সফলভাবে সংরক্ষিত হয়েছে!');
                }
            }
            updateApiStatusUI();
        }

        // Updated getActiveApiKey() supporting multi-key rotation and failover
        function getActiveApiKey() {
            // 1. Pick from adminState.keys (prefer valid or untested)
            if (adminState.keys && adminState.keys.length > 0) {
                const validObj = adminState.keys.find(k => k.status !== 'invalid');
                if (validObj) return validObj.key;
                return adminState.keys[0].key;
            }

            // 2. Fallback to localStorage custom_gemini_api_key
            const saved = localStorage.getItem("custom_gemini_api_key");
            if (saved && saved.trim() !== "") return saved.trim();

            return apiKey || "";
        }

        // Initialize admin state on page load
        window.addEventListener('load', function() {
            if (localStorage.getItem('danam_admin_logged_in') === 'true') {
                adminState.isLoggedIn = true;
                updateAdminHeaderUI();
            }
            loadAdminSettings();
        });

    