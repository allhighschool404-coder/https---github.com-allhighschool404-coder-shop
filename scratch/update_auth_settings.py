# -*- coding: utf-8 -*-
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Header Banner to include Login button
target_header = '''        <!-- Header Banner -->
        <div class="bg-gradient-to-r from-indigo-700 via-purple-700 to-indigo-800 p-6 text-white text-center">
            <h1 class="text-3xl font-extrabold tracking-tight mb-2">অনলাইন অল-ইন-ওয়ান ফাইল কনভার্টার ও স্টুডিও</h1>
            <p class="text-indigo-100 text-sm md:text-base">ওয়ার্ড টু এক্সেল, জেপিজি, পিডিএফ ও ফটো ইঞ্জিনিয়ারিং (পাসপোর্ট, স্ট্যাম্প, 3R, 4R, 10R সাইজ)</p>
        </div>'''

replacement_header = '''        <!-- Header Banner -->
        <div class="relative bg-gradient-to-r from-indigo-700 via-purple-700 to-indigo-800 p-5 md:p-6 text-white shadow-md">
            <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
                <div class="text-center md:text-left flex-1">
                    <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight mb-1">অনলাইন অল-ইন-ওয়ান ফাইল কনভার্টার ও স্টুডিও</h1>
                    <p class="text-indigo-100 text-xs md:text-sm">ওয়ার্ড টু এক্সেল, জেপিজি, পিডিএফ ও ফটো ইঞ্জিনিয়ারিং (পাসপোর্ট, স্ট্যাম্প, 3R, 4R, 10R সাইজ)</p>
                </div>
                <!-- Auth / Login Header Section -->
                <div id="authHeaderBar" class="flex items-center gap-2">
                    <!-- Default: Not logged in -->
                    <button type="button" id="headerLoginBtn" onclick="openLoginModal()"
                        class="px-4 py-2 bg-white/15 hover:bg-white/25 border border-white/30 backdrop-blur-md rounded-xl text-xs md:text-sm font-bold text-white transition flex items-center gap-2 shadow-sm cursor-pointer">
                        <span>🔐</span> Login (লগইন)
                    </button>
                    <!-- Logged in state (Hidden until authenticated) -->
                    <div id="headerLoggedInBar" class="hidden flex items-center gap-2 bg-white/20 backdrop-blur-md px-3 py-1.5 rounded-xl border border-white/30 text-xs">
                        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                        <span class="font-bold text-white">👤 Danam (অ্যাডমিন)</span>
                        <button type="button" onclick="openAdminSettingsModal()"
                            class="ml-1 px-3 py-1.5 bg-white text-indigo-900 hover:bg-indigo-50 rounded-lg font-bold transition flex items-center gap-1.5 shadow-sm cursor-pointer">
                            <span>⚙️</span> প্রম্পট ও API ম্যানেজার
                        </button>
                        <button type="button" onclick="adminLogout()"
                            class="px-2.5 py-1.5 bg-red-500/80 hover:bg-red-600 text-white rounded-lg font-bold transition cursor-pointer">
                            লগআউট
                        </button>
                    </div>
                </div>
            </div>
        </div>'''

if target_header in html:
    html = html.replace(target_header, replacement_header, 1)
    print("Header banner updated successfully!")
else:
    print("Error: target_header not found!")

# 2. Modals HTML for Login and Admin Settings
admin_modals_html = '''
    <!-- Admin Login Modal -->
    <div id="adminLoginModal" class="fixed inset-0 bg-black/80 hidden z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl max-w-md w-full overflow-hidden shadow-2xl border border-slate-200">
            <!-- Modal Header -->
            <div class="p-6 bg-gradient-to-r from-indigo-700 via-purple-700 to-indigo-800 text-white flex items-center justify-between">
                <div>
                    <h3 class="text-xl font-black flex items-center gap-2">
                        <span>🔐</span> অ্যাডমিন লগইন (Admin Login)
                    </h3>
                    <p class="text-xs text-indigo-100 mt-1">প্রম্পট আপডেট ও একাধিক Gemini API Key ব্যবস্থাপনার জন্য লগইন করুন</p>
                </div>
                <button type="button" onclick="closeLoginModal()" class="text-white/70 hover:text-white text-2xl font-bold cursor-pointer">✕</button>
            </div>

            <!-- Modal Form -->
            <form id="adminLoginForm" onsubmit="handleAdminLogin(event)" class="p-6 space-y-4">
                <div id="loginErrorMsg" class="hidden p-3 bg-red-50 border border-red-200 rounded-xl text-xs font-bold text-red-700"></div>

                <div>
                    <label class="block text-xs font-bold text-slate-700 mb-1.5">ইউজার আইডি (User Id)</label>
                    <div class="relative">
                        <span class="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-400">👤</span>
                        <input type="text" id="adminUserIdInput" required value="Danam" placeholder="Danam"
                            class="w-full pl-9 pr-3 py-2.5 border border-slate-300 rounded-xl text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-indigo-500">
                    </div>
                </div>

                <div>
                    <label class="block text-xs font-bold text-slate-700 mb-1.5">পাসওয়ার্ড (Password)</label>
                    <div class="relative">
                        <span class="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-400">🔑</span>
                        <input type="password" id="adminPasswordInput" required value="Danam" placeholder="Danam"
                            class="w-full pl-9 pr-3 py-2.5 border border-slate-300 rounded-xl text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-indigo-500">
                    </div>
                </div>

                <div class="p-3 bg-indigo-50/70 border border-indigo-100 rounded-xl text-xs text-indigo-900 flex items-center gap-2">
                    <span class="text-base">💡</span>
                    <span>সঠিক তথ্য: <b>User Id:</b> <code class="bg-indigo-100 px-1 py-0.5 rounded font-bold">Danam</code> | <b>Password:</b> <code class="bg-indigo-100 px-1 py-0.5 rounded font-bold">Danam</code></span>
                </div>

                <div class="pt-2 flex items-center justify-end gap-3">
                    <button type="button" onclick="closeLoginModal()"
                        class="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition cursor-pointer">
                        বাতিল
                    </button>
                    <button type="submit" id="adminLoginSubmitBtn"
                        class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-bold shadow-md transition flex items-center gap-2 cursor-pointer">
                        <span>🔓</span> লগইন করুন
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- Admin Settings & Prompt Manager Modal -->
    <div id="adminSettingsModal" class="fixed inset-0 bg-black/85 hidden z-50 flex items-center justify-center p-3 md:p-6 overflow-y-auto">
        <div class="bg-white rounded-2xl max-w-4xl w-full max-h-[92vh] flex flex-col overflow-hidden shadow-2xl border border-slate-200">
            <!-- Modal Header -->
            <div class="p-5 bg-gradient-to-r from-indigo-700 via-purple-700 to-indigo-800 text-white flex items-center justify-between">
                <div>
                    <div class="inline-flex items-center gap-1.5 bg-white/20 backdrop-blur-md px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider mb-1">
                        <span>👑</span> অ্যাডমিন কন্ট্রোল প্যানেল
                    </div>
                    <h3 class="text-xl md:text-2xl font-black flex items-center gap-2">
                        <span>⚙️</span> প্রম্পট ও Gemini API কী সেটিংস
                    </h3>
                    <p class="text-xs text-indigo-100 mt-0.5">ছবি তৈরির এআই প্রম্পট আপডেট করুন এবং একাধিক জেমিনি এপিআই কী যুক্ত ও নিয়ন্ত্রণ করুন</p>
                </div>
                <button type="button" onclick="closeAdminSettingsModal()" class="text-white/80 hover:text-white text-2xl font-bold cursor-pointer p-1">✕</button>
            </div>

            <!-- Tabs Navigation inside Modal -->
            <div class="flex border-b border-slate-200 bg-slate-50 px-5 pt-3 gap-2">
                <button type="button" id="adminTabKeysBtn" onclick="switchAdminTab('keys')"
                    class="py-2.5 px-4 rounded-t-xl font-bold text-xs md:text-sm transition flex items-center gap-2 border-b-2 border-indigo-600 bg-white text-indigo-700 shadow-sm cursor-pointer">
                    <span>🔑</span> Gemini API Keys পুল (<span id="adminKeyCountBadge">০</span>)
                </button>
                <button type="button" id="adminTabPromptsBtn" onclick="switchAdminTab('prompts')"
                    class="py-2.5 px-4 rounded-t-xl font-bold text-xs md:text-sm transition flex items-center gap-2 border-b-2 border-transparent text-slate-500 hover:text-indigo-600 cursor-pointer">
                    <span>🎨</span> ছবি তৈরির প্রম্পটসমূহ
                </button>
            </div>

            <!-- Modal Content Area -->
            <div class="p-6 overflow-y-auto flex-1 space-y-6">

                <!-- SECTION A: GEMINI API KEYS POOL -->
                <div id="adminPanelKeys" class="space-y-6">
                    <!-- Add New Key Card -->
                    <div class="bg-gradient-to-r from-blue-50 to-indigo-50 p-5 rounded-2xl border border-indigo-100 shadow-sm">
                        <h4 class="text-sm font-bold text-indigo-950 mb-2 flex items-center gap-2">
                            <span>➕</span> নতুন Gemini API Key যুক্ত করুন
                        </h4>
                        <p class="text-xs text-slate-600 mb-4">
                            আপনি <b>এক বা একাধিক</b> জেমিনি এপিআই কী যুক্ত করতে পারেন। কোনো একটি কী-এর ফ্রি লিমিট শেষ হলে স্বয়ংক্রিয়ভাবে পরবর্তী সচল কী দিয়ে কাজ চলবে।
                        </p>

                        <div class="grid grid-cols-1 md:grid-cols-12 gap-3">
                            <div class="md:col-span-8">
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Gemini API Key (গুগল এআই স্টুডিও থেকে প্রাপ্ত):</label>
                                <input type="text" id="adminNewKeyInput" placeholder="AIzaSy..."
                                    class="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-xs md:text-sm font-mono focus:outline-none focus:ring-2 focus:ring-indigo-500">
                            </div>
                            <div class="md:col-span-4">
                                <label class="block text-xs font-semibold text-slate-600 mb-1">কী-এর নাম / লেবেল (ঐচ্ছিক):</label>
                                <input type="text" id="adminNewKeyLabel" placeholder="যেমন: Key 1"
                                    class="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-xl text-xs md:text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
                            </div>
                        </div>

                        <div class="mt-3 flex items-center justify-between">
                            <a href="https://aistudio.google.com/app/apikey" target="_blank"
                                class="text-xs text-indigo-600 hover:underline font-semibold flex items-center gap-1">
                                <span>🔗</span> বিনামূল্যে গুগল থেকে নতুন Gemini Key নিন
                            </a>
                            <button type="button" onclick="adminAddApiKey()"
                                class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs md:text-sm font-bold shadow transition flex items-center gap-1.5 cursor-pointer">
                                <span>➕</span> কী যুক্ত করুন
                            </button>
                        </div>
                    </div>

                    <!-- Active Keys List -->
                    <div class="space-y-3">
                        <div class="flex items-center justify-between">
                            <h4 class="text-sm font-bold text-slate-800 flex items-center gap-2">
                                <span>📋</span> সংরক্ষিত Gemini API কীগুলোর তালিকা
                            </h4>
                            <span id="adminKeyPoolStatus" class="text-xs px-2.5 py-1 bg-emerald-50 text-emerald-700 rounded-full font-bold border border-emerald-200">
                                ০টি সক্রিয়
                            </span>
                        </div>

                        <!-- Keys Container -->
                        <div id="adminKeysList" class="space-y-2.5">
                            <!-- Populated dynamically via JS -->
                        </div>
                    </div>
                </div>

                <!-- SECTION B: IMAGE & PHOTO PROMPTS -->
                <div id="adminPanelPrompts" class="hidden space-y-6">
                    <div class="p-4 bg-purple-50 rounded-xl border border-purple-100 text-xs text-purple-900 flex items-center gap-2">
                        <span class="text-lg">💡</span>
                        <span>এখানে ছবি তৈরি ও ফেস রিটাচিংয়ের প্রম্পটগুলো আপনার প্রয়োজন অনুযায়ী কাস্টমাইজ করতে পারবেন। যেকোনো সময় "রিসেট" বাটনে চেপে আসল ডিফল্ট প্রম্পটে ফিরে যেতে পারবেন।</span>
                    </div>

                    <!-- Prompt 1: Passport Photo -->
                    <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
                        <div class="flex items-center justify-between">
                            <label class="text-sm font-bold text-slate-800 flex items-center gap-2">
                                <span>🛂</span> পাসপোর্ট সাইজ ফটো এআই প্রম্পট (Passport Studio Prompt)
                            </label>
                            <button type="button" onclick="adminResetPrompt('passport')"
                                class="text-xs text-indigo-600 hover:underline font-bold cursor-pointer">
                                🔄 ডিফল্ট রিসেট
                            </button>
                        </div>
                        <textarea id="promptInput_passport" rows="3"
                            class="w-full p-3 border border-slate-300 rounded-xl text-xs md:text-sm font-sans focus:outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
                    </div>

                    <!-- Prompt 2: Photo Fresh & Skin Retouch -->
                    <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
                        <div class="flex items-center justify-between">
                            <label class="text-sm font-bold text-slate-800 flex items-center gap-2">
                                <span>✨</span> ফোটো ফ্রেশ ও ত্বক মসৃণকরণ প্রম্পট (Photo Fresh Retouch Prompt)
                            </label>
                            <button type="button" onclick="adminResetPrompt('fresh')"
                                class="text-xs text-indigo-600 hover:underline font-bold cursor-pointer">
                                🔄 ডিফল্ট রিসেট
                            </button>
                        </div>
                        <textarea id="promptInput_fresh" rows="3"
                            class="w-full p-3 border border-slate-300 rounded-xl text-xs md:text-sm font-sans focus:outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
                    </div>

                    <!-- Prompt 3: Joint / Couple Photo -->
                    <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
                        <div class="flex items-center justify-between">
                            <label class="text-sm font-bold text-slate-800 flex items-center gap-2">
                                <span>👥</span> যৌথ ছবি / দুটি ছবি একসাথে প্রম্পট (Joint Studio Photo Prompt)
                            </label>
                            <button type="button" onclick="adminResetPrompt('joint')"
                                class="text-xs text-indigo-600 hover:underline font-bold cursor-pointer">
                                🔄 ডিফল্ট রিসেট
                            </button>
                        </div>
                        <textarea id="promptInput_joint" rows="3"
                            class="w-full p-3 border border-slate-300 rounded-xl text-xs md:text-sm font-sans focus:outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
                    </div>

                    <!-- Prompt 4: Stamp Size Photo -->
                    <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
                        <div class="flex items-center justify-between">
                            <label class="text-sm font-bold text-slate-800 flex items-center gap-2">
                                <span>🏷️</span> স্ট্যাম্প সাইজ ফটো প্রম্পট (Stamp Size Studio Prompt)
                            </label>
                            <button type="button" onclick="adminResetPrompt('stamp')"
                                class="text-xs text-indigo-600 hover:underline font-bold cursor-pointer">
                                🔄 ডিফল্ট রিসেট
                            </button>
                        </div>
                        <textarea id="promptInput_stamp" rows="3"
                            class="w-full p-3 border border-slate-300 rounded-xl text-xs md:text-sm font-sans focus:outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
                    </div>

                    <!-- Prompt 5: Custom Image Prompt -->
                    <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
                        <div class="flex items-center justify-between">
                            <label class="text-sm font-bold text-slate-800 flex items-center gap-2">
                                <span>🎨</span> কাস্টম ছবি তৈরি ও সৃজনশীল প্রম্পট (Custom Image Creation Prompt)
                            </label>
                            <button type="button" onclick="adminResetPrompt('custom')"
                                class="text-xs text-indigo-600 hover:underline font-bold cursor-pointer">
                                🔄 ডিফল্ট রিসেট
                            </button>
                        </div>
                        <textarea id="promptInput_custom" rows="3"
                            class="w-full p-3 border border-slate-300 rounded-xl text-xs md:text-sm font-sans focus:outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
                    </div>

                    <!-- Prompt 6: Question Paper & Document Parsing -->
                    <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
                        <div class="flex items-center justify-between">
                            <label class="text-sm font-bold text-slate-800 flex items-center gap-2">
                                <span>📝</span> স্মার্ট প্রশ্নপত্র ও ডকুমেন্ট এআই প্রম্পট (Question Paper AI Prompt)
                            </label>
                            <button type="button" onclick="adminResetPrompt('question')"
                                class="text-xs text-indigo-600 hover:underline font-bold cursor-pointer">
                                🔄 ডিফল্ট রিসেট
                            </button>
                        </div>
                        <textarea id="promptInput_question" rows="3"
                            class="w-full p-3 border border-slate-300 rounded-xl text-xs md:text-sm font-sans focus:outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
                    </div>
                </div>

            </div>

            <!-- Modal Footer -->
            <div class="p-5 border-t border-slate-200 bg-slate-50 flex items-center justify-between">
                <button type="button" onclick="closeAdminSettingsModal()"
                    class="px-5 py-2.5 bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold rounded-xl text-xs md:text-sm transition cursor-pointer">
                    বন্ধ করুন
                </button>
                <button type="button" onclick="adminSaveAllSettings()"
                    class="px-6 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-700 hover:from-emerald-700 hover:to-teal-800 text-white font-extrabold rounded-xl text-xs md:text-sm shadow-md transition flex items-center gap-2 cursor-pointer">
                    <span>💾</span> সকল পরিবর্তন সেভ করুন (Save Changes)
                </button>
            </div>
        </div>
    </div>
'''

target_modals = '</body>\n\n</html>'
if target_modals in html:
    html = html.replace(target_modals, f'{admin_modals_html}\n</body>\n\n</html>', 1)
    print("Admin modals inserted successfully!")
else:
    print("Error: target_modals not found!")

# 3. JavaScript logic for Admin Auth & Settings
admin_js = '''
        // ==========================================
        // ADMIN AUTH & SETTINGS STATE AND LOGIC
        // ==========================================
        const adminState = {
            isLoggedIn: false,
            user: "Danam",
            keys: [], // array of { key: string, label: string, status: string }
            prompts: {
                passport: "High-resolution 300 DPI professional studio passport photo, sharp facial focus, natural skin tones, clear eyes and hairline, studio soft lighting, solid studio blue background, clean formal attire, neutral facial expression, perfectly centered framing, crystal clear studio print quality.",
                fresh: "Professional photographic skin enhancement, smooth gentle blemish removal while preserving natural skin pores, brightness and contrast optimization, enhance eye clarity, natural healthy skin vibrance, studio lighting balance.",
                joint: "Dual couple studio portrait photography, two people standing side by side naturally, uniform studio blue background, harmonious lighting and shadow balance, high resolution formal photo studio framing.",
                stamp: "Clean official stamp size portrait, crisp sharpness, solid background, high contrast, studio lighting.",
                question: "You are an expert examiner and teacher. Convert raw math exam text, questions, images, or PDF documents into clean structured JSON format with schoolName, examTitle, class, subject, marks, time, instruction, and sections.",
                custom: "Ultra-realistic studio photo, professional portrait lighting, sharp focus, 8k resolution, studio quality."
            },
            defaultPrompts: {
                passport: "High-resolution 300 DPI professional studio passport photo, sharp facial focus, natural skin tones, clear eyes and hairline, studio soft lighting, solid studio blue background, clean formal attire, neutral facial expression, perfectly centered framing, crystal clear studio print quality.",
                fresh: "Professional photographic skin enhancement, smooth gentle blemish removal while preserving natural skin pores, brightness and contrast optimization, enhance eye clarity, natural healthy skin vibrance, studio lighting balance.",
                joint: "Dual couple studio portrait photography, two people standing side by side naturally, uniform studio blue background, harmonious lighting and shadow balance, high resolution formal photo studio framing.",
                stamp: "Clean official stamp size portrait, crisp sharpness, solid background, high contrast, studio lighting.",
                question: "You are an expert examiner and teacher. Convert raw math exam text, questions, images, or PDF documents into clean structured JSON format with schoolName, examTitle, class, subject, marks, time, instruction, and sections.",
                custom: "Ultra-realistic studio photo, professional portrait lighting, sharp focus, 8k resolution, studio quality."
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
'''

# 4. Insert admin_js right before closing </script>
idx = html.rfind('</script>')
if idx != -1:
    html = html[:idx] + admin_js + '\n    ' + html[idx:]
    print("Admin JS inserted successfully!")
else:
    print("Error: </script> not found!")

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated templates/index.html with Admin Auth & Settings successfully!")

