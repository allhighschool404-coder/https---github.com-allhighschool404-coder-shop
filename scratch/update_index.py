# -*- coding: utf-8 -*-
import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. HTML Block for Photo Engineering Tab
photo_tab_html = '''
            <!-- TAB 5: PHOTO ENGINEERING (ফটো ইঞ্জিনিয়ারিং) -->
            <div id="photoEngineeringTab" class="hidden">
                <!-- Banner -->
                <div class="bg-gradient-to-r from-blue-700 via-sky-600 to-indigo-800 rounded-2xl p-6 md:p-8 text-white mb-8 shadow-lg">
                    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                        <div>
                            <div class="inline-flex items-center gap-2 bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider mb-2">
                                <span>⚡</span> স্টুডিও কোয়ালিটি এআই ইঞ্জিন
                            </div>
                            <h2 class="text-2xl md:text-3xl font-black flex items-center gap-2">
                                <span>📸</span> ফটো ইঞ্জিনিয়ারিং ও স্টুডিও ল্যাব
                            </h2>
                            <p class="text-blue-100 text-sm md:text-base mt-1">
                                পাসপোর্ট, স্ট্যাম্প, 3R, 4R, 10R সাইজের ছবি তৈরি • অটো ফ্রেশ ও ত্বক মসৃণকরণ • ক্লাসিক ব্লু ব্যাকগ্রাউন্ড • দুটি ছবি একসাথে কম্বিনেশন
                            </p>
                        </div>
                        <!-- Mode Selector Pill -->
                        <div class="bg-white/10 backdrop-blur-md p-1.5 rounded-xl border border-white/20 flex gap-1 self-start md:self-auto">
                            <button type="button" id="peModeSingleBtn" onclick="peSetMode('single')"
                                class="px-4 py-2 rounded-lg font-bold text-sm transition bg-white text-blue-800 shadow">
                                👤 একক ছবি
                            </button>
                            <button type="button" id="peModeDualBtn" onclick="peSetMode('dual')"
                                class="px-4 py-2 rounded-lg font-bold text-sm transition text-white hover:bg-white/20">
                                👥 দুটি ছবি একসাথে
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Main Work Area: 2 Columns Grid -->
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    <!-- Left Column: Controls (7 cols) -->
                    <div class="lg:col-span-7 space-y-6">

                        <!-- SECTION 1: PHOTO UPLOAD -->
                        <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
                            <h3 class="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                                <span class="w-7 h-7 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center text-sm font-bold">১</span>
                                ছবি আপলোড ও উৎস নির্বাচন
                            </h3>

                            <!-- Single Photo Upload Area -->
                            <div id="peSingleUploadArea" class="block">
                                <div id="peDropzone1"
                                    class="border-2 border-dashed border-blue-300 rounded-xl p-6 text-center bg-blue-50/50 hover:bg-blue-50 transition cursor-pointer relative group">
                                    <input type="file" id="peFile1" accept="image/*" class="hidden" onchange="peHandleFileSelect(this, 1)">
                                    <div id="peDropContent1">
                                        <div class="w-16 h-16 mx-auto mb-3 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-3xl group-hover:scale-110 transition-transform">
                                            📁
                                        </div>
                                        <p class="font-bold text-slate-800 text-base mb-1">এখানে ছবি টেনে আনুন বা ক্লিক করে ফাইল নির্বাচন করুন</p>
                                        <p class="text-xs text-slate-500 mb-4">সমর্থিত ফরম্যাট: JPG, PNG, WEBP, GIF, PSD, ইত্যাদি (যেকোনো রেজুলোশন)</p>
                                        <div class="flex items-center justify-center gap-3">
                                            <button type="button" onclick="document.getElementById('peFile1').click()"
                                                class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-semibold transition shadow-sm flex items-center gap-2">
                                                <span>📂</span> ব্রাউজ করুন
                                            </button>
                                            <button type="button" onclick="peOpenWebcam(1)"
                                                class="px-4 py-2 bg-slate-700 hover:bg-slate-800 text-white rounded-lg text-sm font-semibold transition shadow-sm flex items-center gap-2">
                                                <span>📸</span> ক্যামেরা দিয়ে তুলুন
                                            </button>
                                        </div>
                                    </div>
                                    <!-- Thumbnail when selected -->
                                    <div id="peThumbBox1" class="hidden flex items-center justify-between p-3 bg-white rounded-lg border border-slate-200">
                                        <div class="flex items-center gap-3">
                                            <img id="peThumbImg1" src="" class="w-14 h-14 object-cover rounded-md border border-slate-300">
                                            <div class="text-left">
                                                <p id="peThumbName1" class="font-bold text-sm text-slate-800 truncate max-w-xs">photo.jpg</p>
                                                <p id="peThumbSize1" class="text-xs text-slate-500">2.4 MB</p>
                                            </div>
                                        </div>
                                        <button type="button" onclick="document.getElementById('peFile1').click()"
                                            class="px-3 py-1.5 text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-md font-semibold">
                                            ছবি পরিবর্তন
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <!-- Dual Photo Upload Area -->
                            <div id="peDualUploadArea" class="hidden space-y-4">
                                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                    <!-- Photo 1 Card -->
                                    <div class="border-2 border-dashed border-blue-300 rounded-xl p-4 text-center bg-blue-50/40 relative">
                                        <p class="font-bold text-sm text-blue-900 mb-2">👤 প্রথম ব্যক্তির ছবি (ছবি ১)</p>
                                        <input type="file" id="peFileDual1" accept="image/*" class="hidden" onchange="peHandleFileSelect(this, 1)">
                                        <div id="peDualDropContent1">
                                            <div class="w-12 h-12 mx-auto mb-2 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xl">
                                                👤
                                            </div>
                                            <div class="flex flex-col gap-2">
                                                <button type="button" onclick="document.getElementById('peFileDual1').click()"
                                                    class="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold transition">
                                                    📂 ছবি ১ নির্বাচন
                                                </button>
                                                <button type="button" onclick="peOpenWebcam(1)"
                                                    class="px-3 py-1.5 bg-slate-700 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold transition">
                                                    📸 ক্যামেরায় তুলুন
                                                </button>
                                            </div>
                                        </div>
                                        <div id="peDualThumbBox1" class="hidden mt-2 p-2 bg-white rounded-lg border border-slate-200 flex items-center gap-2">
                                            <img id="peDualThumbImg1" src="" class="w-10 h-10 object-cover rounded border">
                                            <p id="peDualThumbName1" class="text-xs font-semibold truncate flex-1 text-left"></p>
                                            <button type="button" onclick="document.getElementById('peFileDual1').click()" class="text-xs text-blue-600 font-bold">বদলান</button>
                                        </div>
                                    </div>

                                    <!-- Photo 2 Card -->
                                    <div class="border-2 border-dashed border-indigo-300 rounded-xl p-4 text-center bg-indigo-50/40 relative">
                                        <p class="font-bold text-sm text-indigo-900 mb-2">👤 দ্বিতীয় ব্যক্তির ছবি (ছবি ২)</p>
                                        <input type="file" id="peFileDual2" accept="image/*" class="hidden" onchange="peHandleFileSelect(this, 2)">
                                        <div id="peDualDropContent2">
                                            <div class="w-12 h-12 mx-auto mb-2 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-xl">
                                                👤
                                            </div>
                                            <div class="flex flex-col gap-2">
                                                <button type="button" onclick="document.getElementById('peFileDual2').click()"
                                                    class="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold transition">
                                                    📂 ছবি ২ নির্বাচন
                                                </button>
                                                <button type="button" onclick="peOpenWebcam(2)"
                                                    class="px-3 py-1.5 bg-slate-700 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold transition">
                                                    📸 ক্যামেরায় তুলুন
                                                </button>
                                            </div>
                                        </div>
                                        <div id="peDualThumbBox2" class="hidden mt-2 p-2 bg-white rounded-lg border border-slate-200 flex items-center gap-2">
                                            <img id="peDualThumbImg2" src="" class="w-10 h-10 object-cover rounded border">
                                            <p id="peDualThumbName2" class="text-xs font-semibold truncate flex-1 text-left"></p>
                                            <button type="button" onclick="document.getElementById('peFileDual2').click()" class="text-xs text-indigo-600 font-bold">বদলান</button>
                                        </div>
                                    </div>
                                </div>

                                <!-- Dual Combination Style -->
                                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3">
                                    <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider">কম্বিনেশন স্টাইল</label>
                                    <div class="grid grid-cols-2 gap-3">
                                        <button type="button" id="peDualStyleJointBtn" onclick="peSetDualLayout('joint')"
                                            class="p-3 rounded-lg border-2 border-blue-600 bg-blue-50 text-blue-900 font-bold text-xs flex items-center justify-center gap-2">
                                            <span>👫</span> যৌথ ছবি (একসাথে এক ফ্রেমে)
                                        </button>
                                        <button type="button" id="peDualStyleSplitBtn" onclick="peSetDualLayout('side_by_side')"
                                            class="p-3 rounded-lg border-2 border-slate-200 bg-white text-slate-700 font-bold text-xs flex items-center justify-center gap-2">
                                            <span>🔲</span> পাশাপাশি দুটি ছবি (বিভক্ত)
                                        </button>
                                    </div>

                                    <!-- Fine tuning for dual mode -->
                                    <div class="grid grid-cols-3 gap-3 pt-2 text-xs">
                                        <div>
                                            <label class="block font-semibold text-slate-600 mb-1">ছবি ১ সাইজ: <span id="peScale1Val" class="font-bold text-blue-700">1.0x</span></label>
                                            <input type="range" id="peScale1" min="0.6" max="1.5" step="0.05" value="1.0" oninput="peUpdateDualSliders()" class="w-full accent-blue-600">
                                        </div>
                                        <div>
                                            <label class="block font-semibold text-slate-600 mb-1">ছবি ২ সাইজ: <span id="peScale2Val" class="font-bold text-blue-700">1.0x</span></label>
                                            <input type="range" id="peScale2" min="0.6" max="1.5" step="0.05" value="1.0" oninput="peUpdateDualSliders()" class="w-full accent-blue-600">
                                        </div>
                                        <div>
                                            <label class="block font-semibold text-slate-600 mb-1">দুজনের ব্যবধান: <span id="peGapVal" class="font-bold text-blue-700">0px</span></label>
                                            <input type="range" id="peGap" min="-50" max="100" step="5" value="0" oninput="peUpdateDualSliders()" class="w-full accent-blue-600">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- SECTION 2: PHOTO SIZE (পাসপোর্ট, স্ট্যাম্প, 3R, 4R, 10R) -->
                        <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
                            <div class="flex items-center justify-between mb-4">
                                <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
                                    <span class="w-7 h-7 rounded-lg bg-indigo-100 text-indigo-700 flex items-center justify-center text-sm font-bold">২</span>
                                    ছবির সাইজ নির্বাচন করুন
                                </h3>
                                <span class="text-xs bg-indigo-50 text-indigo-700 px-2.5 py-1 rounded-full font-bold">৩০০ DPI স্টুডিও প্রিন্ট</span>
                            </div>

                            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mb-4">
                                <!-- Passport BD -->
                                <button type="button" onclick="peSelectSize('passport_bd')" id="peSize_passport_bd"
                                    class="pe-size-btn p-3 rounded-xl border-2 border-indigo-600 bg-indigo-50 text-indigo-900 text-left transition font-bold shadow-sm">
                                    <div class="text-xs text-indigo-600 font-semibold mb-0.5">পাসপোর্ট (বাংলাদেশ)</div>
                                    <div class="text-sm font-extrabold">৪০ x ৫০ মিমি</div>
                                    <div class="text-[10px] text-slate-500 font-normal mt-0.5">১.৫৭ x ১.৯৭ ইঞ্চি</div>
                                </button>
                                <!-- Passport Intl -->
                                <button type="button" onclick="peSelectSize('passport_intl')" id="peSize_passport_intl"
                                    class="pe-size-btn p-3 rounded-xl border-2 border-slate-200 bg-white text-slate-800 text-left hover:border-indigo-300 transition font-bold">
                                    <div class="text-xs text-slate-500 font-semibold mb-0.5">আন্তর্জাতিক পাসপোর্ট</div>
                                    <div class="text-sm font-extrabold">৩৫ x ৪৫ মিমি</div>
                                    <div class="text-[10px] text-slate-500 font-normal mt-0.5">বায়োমেট্রিক সাইজ</div>
                                </button>
                                <!-- Visa / 2x2 -->
                                <button type="button" onclick="peSelectSize('passport_us')" id="peSize_passport_us"
                                    class="pe-size-btn p-3 rounded-xl border-2 border-slate-200 bg-white text-slate-800 text-left hover:border-indigo-300 transition font-bold">
                                    <div class="text-xs text-slate-500 font-semibold mb-0.5">ভিসা / ২x২ ইঞ্চি</div>
                                    <div class="text-sm font-extrabold">৫০.৮ x ৫০.৮ মিমি</div>
                                    <div class="text-[10px] text-slate-500 font-normal mt-0.5">স্কয়ার ফরম্যাট</div>
                                </button>
                                <!-- Stamp Size -->
                                <button type="button" onclick="peSelectSize('stamp')" id="peSize_stamp"
                                    class="pe-size-btn p-3 rounded-xl border-2 border-slate-200 bg-white text-slate-800 text-left hover:border-indigo-300 transition font-bold">
                                    <div class="text-xs text-slate-500 font-semibold mb-0.5">স্ট্যাম্প সাইজ</div>
                                    <div class="text-sm font-extrabold">২০ x ২৫ মিমি</div>
                                    <div class="text-[10px] text-slate-500 font-normal mt-0.5">০.৮ x ১.০ ইঞ্চি</div>
                                </button>
                                <!-- 3R Size -->
                                <button type="button" onclick="peSelectSize('3r')" id="peSize_3r"
                                    class="pe-size-btn p-3 rounded-xl border-2 border-slate-200 bg-white text-slate-800 text-left hover:border-indigo-300 transition font-bold">
                                    <div class="text-xs text-slate-500 font-semibold mb-0.5">৩-আর (3R) সাইজ</div>
                                    <div class="text-sm font-extrabold">৩.৫ x ৫.০ ইঞ্চি</div>
                                    <div class="text-[10px] text-slate-500 font-normal mt-0.5">৮৯ x ১২৭ মিমি</div>
                                </button>
                                <!-- 4R Size -->
                                <button type="button" onclick="peSelectSize('4r')" id="peSize_4r"
                                    class="pe-size-btn p-3 rounded-xl border-2 border-slate-200 bg-white text-slate-800 text-left hover:border-indigo-300 transition font-bold">
                                    <div class="text-xs text-slate-500 font-semibold mb-0.5">৪-আর (4R) সাইজ</div>
                                    <div class="text-sm font-extrabold">৪.০ x ৬.০ ইঞ্চি</div>
                                    <div class="text-[10px] text-slate-500 font-normal mt-0.5">স্ট্যান্ডার্ড ফটো প্রিন্ট</div>
                                </button>
                                <!-- 10R Size -->
                                <button type="button" onclick="peSelectSize('10r')" id="peSize_10r"
                                    class="pe-size-btn p-3 rounded-xl border-2 border-slate-200 bg-white text-slate-800 text-left hover:border-indigo-300 transition font-bold">
                                    <div class="text-xs text-slate-500 font-semibold mb-0.5">১০-আর (10R) সাইজ</div>
                                    <div class="text-sm font-extrabold">১০.০ x ১২.০ ইঞ্চি</div>
                                    <div class="text-[10px] text-slate-500 font-normal mt-0.5">বড় অ্যালবাম / ফ্রেম</div>
                                </button>
                                <!-- Custom Size -->
                                <button type="button" onclick="peSelectSize('custom')" id="peSize_custom"
                                    class="pe-size-btn p-3 rounded-xl border-2 border-slate-200 bg-white text-slate-800 text-left hover:border-indigo-300 transition font-bold">
                                    <div class="text-xs text-slate-500 font-semibold mb-0.5">কাস্টম সাইজ</div>
                                    <div class="text-sm font-extrabold">পছন্দমতো মাপ</div>
                                    <div class="text-[10px] text-slate-500 font-normal mt-0.5">মিমি / ইঞ্চি / পিক্সেল</div>
                                </button>
                            </div>

                            <!-- Custom Size Inputs (Hidden by default) -->
                            <div id="peCustomSizeInputs" class="hidden p-4 bg-slate-50 rounded-xl border border-slate-200 mb-4">
                                <p class="text-xs font-bold text-slate-700 mb-2">কাস্টম মাপ নির্ধারণ করুন:</p>
                                <div class="grid grid-cols-3 gap-3">
                                    <div>
                                        <label class="block text-xs text-slate-600 mb-1">প্রস্থ (Width)</label>
                                        <input type="number" id="peCustomW" value="40" step="0.1" class="w-full px-3 py-1.5 border rounded-lg text-sm font-semibold">
                                    </div>
                                    <div>
                                        <label class="block text-xs text-slate-600 mb-1">উচ্চতা (Height)</label>
                                        <input type="number" id="peCustomH" value="50" step="0.1" class="w-full px-3 py-1.5 border rounded-lg text-sm font-semibold">
                                    </div>
                                    <div>
                                        <label class="block text-xs text-slate-600 mb-1">একক (Unit)</label>
                                        <select id="peCustomUnit" class="w-full px-3 py-1.5 border rounded-lg text-sm font-semibold bg-white">
                                            <option value="mm">মিমি (mm)</option>
                                            <option value="in">ইঞ্চি (inch)</option>
                                            <option value="px">পিক্সেল (px)</option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <!-- SECTION 3: ORIENTATION (PORTRAIT & LANDSCAPE) -->
                            <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
                                <label class="text-sm font-bold text-slate-700 flex items-center gap-1.5">
                                    <span>🔄</span> ওরিয়েন্টেশন (Orientation):
                                </label>
                                <div class="inline-flex rounded-xl bg-slate-100 p-1 border border-slate-200">
                                    <button type="button" id="peOrientPortraitBtn" onclick="peSetOrientation('portrait')"
                                        class="px-4 py-1.5 rounded-lg text-xs font-bold transition bg-white text-indigo-700 shadow-sm flex items-center gap-1.5">
                                        <span>📱</span> পোর্ট্রেট (লম্বালম্বি)
                                    </button>
                                    <button type="button" id="peOrientLandscapeBtn" onclick="peSetOrientation('landscape')"
                                        class="px-4 py-1.5 rounded-lg text-xs font-bold transition text-slate-600 hover:text-indigo-600 flex items-center gap-1.5">
                                        <span>💻</span> ল্যান্ডস্কেপ (আড়াআড়ি)
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- SECTION 4: BACKGROUND BLUE COLOR & OPTIONS -->
                        <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
                            <div class="flex items-center justify-between mb-4">
                                <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
                                    <span class="w-7 h-7 rounded-lg bg-sky-100 text-sky-700 flex items-center justify-center text-sm font-bold">৩</span>
                                    ব্যাকগ্রাউন্ড ব্লু কালার ও পরিবর্তন
                                </h3>
                                <label class="inline-flex items-center gap-2 cursor-pointer">
                                    <input type="checkbox" id="peRemoveBgToggle" checked onchange="peToggleRemoveBg(this.checked)" class="w-4 h-4 text-blue-600 rounded">
                                    <span class="text-xs font-bold text-slate-700">এআই ব্যাকগ্রাউন্ড কাটআউট</span>
                                </label>
                            </div>

                            <div id="peBgColorControls">
                                <p class="text-xs text-slate-500 mb-3">পাসপোর্ট ও অফিসিয়াল স্টুডিও ব্যাকগ্রাউন্ড কালার নির্বাচন করুন:</p>
                                <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                                    <!-- Studio Blue (Default) -->
                                    <button type="button" onclick="peSelectBgColor('#1E6091', 'studio_blue')" id="peColor_studio_blue"
                                        class="pe-color-btn p-2.5 rounded-xl border-2 border-blue-600 bg-blue-50/50 flex items-center gap-2 text-left transition">
                                        <span class="w-6 h-6 rounded-lg shadow-sm border border-black/10 flex-shrink-0" style="background-color: #1E6091;"></span>
                                        <div>
                                            <div class="text-xs font-bold text-slate-800">স্টুডিও ব্লু</div>
                                            <div class="text-[10px] text-slate-500">ক্লাসিক পাসপোর্ট</div>
                                        </div>
                                    </button>
                                    <!-- Royal Blue -->
                                    <button type="button" onclick="peSelectBgColor('#0047AB', 'royal_blue')" id="peColor_royal_blue"
                                        class="pe-color-btn p-2.5 rounded-xl border-2 border-slate-200 bg-white flex items-center gap-2 text-left transition hover:border-slate-300">
                                        <span class="w-6 h-6 rounded-lg shadow-sm border border-black/10 flex-shrink-0" style="background-color: #0047AB;"></span>
                                        <div>
                                            <div class="text-xs font-bold text-slate-800">রয়েল ব্লু</div>
                                            <div class="text-[10px] text-slate-500">গাঢ় নীল</div>
                                        </div>
                                    </button>
                                    <!-- Vivid Blue -->
                                    <button type="button" onclick="peSelectBgColor('#2B78E4', 'vivid_blue')" id="peColor_vivid_blue"
                                        class="pe-color-btn p-2.5 rounded-xl border-2 border-slate-200 bg-white flex items-center gap-2 text-left transition hover:border-slate-300">
                                        <span class="w-6 h-6 rounded-lg shadow-sm border border-black/10 flex-shrink-0" style="background-color: #2B78E4;"></span>
                                        <div>
                                            <div class="text-xs font-bold text-slate-800">উজ্জ্বল ব্লু</div>
                                            <div class="text-[10px] text-slate-500">ভাইব্রেন্ট স্কাই</div>
                                        </div>
                                    </button>
                                    <!-- Light Blue -->
                                    <button type="button" onclick="peSelectBgColor('#85C1E9', 'sky_blue')" id="peColor_sky_blue"
                                        class="pe-color-btn p-2.5 rounded-xl border-2 border-slate-200 bg-white flex items-center gap-2 text-left transition hover:border-slate-300">
                                        <span class="w-6 h-6 rounded-lg shadow-sm border border-black/10 flex-shrink-0" style="background-color: #85C1E9;"></span>
                                        <div>
                                            <div class="text-xs font-bold text-slate-800">আকাশি ব্লু</div>
                                            <div class="text-[10px] text-slate-500">হালকা নীল</div>
                                        </div>
                                    </button>
                                    <!-- White -->
                                    <button type="button" onclick="peSelectBgColor('#FFFFFF', 'white')" id="peColor_white"
                                        class="pe-color-btn p-2.5 rounded-xl border-2 border-slate-200 bg-white flex items-center gap-2 text-left transition hover:border-slate-300">
                                        <span class="w-6 h-6 rounded-lg shadow-sm border border-slate-300 flex-shrink-0" style="background-color: #FFFFFF;"></span>
                                        <div>
                                            <div class="text-xs font-bold text-slate-800">সাদা (White)</div>
                                            <div class="text-[10px] text-slate-500">ভিসা / আইডি</div>
                                        </div>
                                    </button>
                                    <!-- Light Gray -->
                                    <button type="button" onclick="peSelectBgColor('#E5E7EB', 'light_gray')" id="peColor_light_gray"
                                        class="pe-color-btn p-2.5 rounded-xl border-2 border-slate-200 bg-white flex items-center gap-2 text-left transition hover:border-slate-300">
                                        <span class="w-6 h-6 rounded-lg shadow-sm border border-slate-300 flex-shrink-0" style="background-color: #E5E7EB;"></span>
                                        <div>
                                            <div class="text-xs font-bold text-slate-800">হালকা ধূসর</div>
                                            <div class="text-[10px] text-slate-500">অফিশিয়াল গ্রে</div>
                                        </div>
                                    </button>
                                    <!-- Transparent PNG -->
                                    <button type="button" onclick="peSelectBgColor('transparent', 'transparent')" id="peColor_transparent"
                                        class="pe-color-btn p-2.5 rounded-xl border-2 border-slate-200 bg-white flex items-center gap-2 text-left transition hover:border-slate-300">
                                        <span class="w-6 h-6 rounded-lg shadow-sm border border-slate-300 bg-gradient-to-tr from-slate-200 via-white to-slate-200 flex-shrink-0 text-center text-xs flex items-center justify-center">🪟</span>
                                        <div>
                                            <div class="text-xs font-bold text-slate-800">স্বচ্ছ (PNG)</div>
                                            <div class="text-[10px] text-slate-500">ট্রান্সপারেন্ট</div>
                                        </div>
                                    </button>
                                    <!-- Custom Color Picker -->
                                    <div class="pe-color-btn p-2 rounded-xl border-2 border-slate-200 bg-white flex items-center gap-2 transition hover:border-slate-300 relative">
                                        <input type="color" id="peCustomColorPicker" value="#1E6091" onchange="peSelectBgColor(this.value, 'custom_color')"
                                            class="w-7 h-7 rounded-lg cursor-pointer border-0 p-0 flex-shrink-0">
                                        <div class="truncate">
                                            <div class="text-xs font-bold text-slate-800">কাস্টম কালার</div>
                                            <span id="peCustomHexVal" class="text-[10px] text-slate-500 font-mono">#1E6091</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- SECTION 5: PHOTO FRESH & STUDIO RETOUCH -->
                        <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
                            <div class="flex items-center justify-between mb-4">
                                <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
                                    <span class="w-7 h-7 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center text-sm font-bold">৪</span>
                                    ফোটো ফ্রেশ ও স্টুডিও রিটাচ
                                </h3>
                                <button type="button" onclick="peResetSliders()" class="text-xs text-slate-500 hover:text-slate-800 underline font-semibold">
                                    রিসেট
                                </button>
                            </div>

                            <!-- 1-Click Auto Fresh Banner Button -->
                            <div class="mb-5">
                                <button type="button" id="peAutoFreshBtn" onclick="peToggleAutoFresh()"
                                    class="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-bold text-sm shadow-md flex items-center justify-center gap-2 transition-all transform active:scale-95">
                                    <span class="text-lg">✨</span>
                                    <span>১-ক্লিকে অটো ফ্রেশ ও গ্লো (অটো লাইটিং, ত্বক মসৃণ ও শার্পনেস)</span>
                                    <span id="peAutoFreshBadge" class="ml-2 bg-white/20 text-white text-xs px-2 py-0.5 rounded-full font-extrabold">চালু আছে</span>
                                </button>
                            </div>

                            <!-- Sliders Grid -->
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <!-- Brightness -->
                                <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                                    <div class="flex justify-between text-xs font-bold text-slate-700 mb-1">
                                        <span class="flex items-center gap-1">☀️ উজ্জ্বলতা (Brightness)</span>
                                        <span id="peValBrightness" class="text-blue-600 font-mono">0</span>
                                    </div>
                                    <input type="range" id="peSliderBrightness" min="-100" max="100" value="0" oninput="peUpdateSliderVal('Brightness')" class="w-full accent-blue-600">
                                </div>
                                <!-- Contrast -->
                                <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                                    <div class="flex justify-between text-xs font-bold text-slate-700 mb-1">
                                        <span class="flex items-center gap-1">🌓 কনট্রাস্ট (Contrast)</span>
                                        <span id="peValContrast" class="text-blue-600 font-mono">0</span>
                                    </div>
                                    <input type="range" id="peSliderContrast" min="-100" max="100" value="0" oninput="peUpdateSliderVal('Contrast')" class="w-full accent-blue-600">
                                </div>
                                <!-- Skin Smoothness -->
                                <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                                    <div class="flex justify-between text-xs font-bold text-slate-700 mb-1">
                                        <span class="flex items-center gap-1">💆 ত্বক মসৃণতা (Skin Softening)</span>
                                        <span id="peValSmoothness" class="text-blue-600 font-mono">0</span>
                                    </div>
                                    <input type="range" id="peSliderSmoothness" min="0" max="100" value="0" oninput="peUpdateSliderVal('Smoothness')" class="w-full accent-blue-600">
                                </div>
                                <!-- Sharpness -->
                                <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                                    <div class="flex justify-between text-xs font-bold text-slate-700 mb-1">
                                        <span class="flex items-center gap-1">🔍 শার্পনেস (Sharpness)</span>
                                        <span id="peValSharpness" class="text-blue-600 font-mono">0</span>
                                    </div>
                                    <input type="range" id="peSliderSharpness" min="0" max="100" value="0" oninput="peUpdateSliderVal('Sharpness')" class="w-full accent-blue-600">
                                </div>
                                <!-- Saturation / Warmth -->
                                <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 sm:col-span-2">
                                    <div class="flex justify-between text-xs font-bold text-slate-700 mb-1">
                                        <span class="flex items-center gap-1">🎨 ত্বকের স্বাভাবিক রঙ ও ভাইব্রেন্স (Vibrance)</span>
                                        <span id="peValSaturation" class="text-blue-600 font-mono">0</span>
                                    </div>
                                    <input type="range" id="peSliderSaturation" min="-100" max="100" value="0" oninput="peUpdateSliderVal('Saturation')" class="w-full accent-blue-600">
                                </div>
                            </div>
                        </div>

                        <!-- SECTION 6: FRAMING & CROP ALIGNMENT -->
                        <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
                            <h3 class="text-lg font-bold text-slate-800 mb-4 flex items-center justify-between">
                                <span class="flex items-center gap-2">
                                    <span class="w-7 h-7 rounded-lg bg-amber-100 text-amber-700 flex items-center justify-center text-sm font-bold">৫</span>
                                    ফ্রেম ক্রপিং ও মুখমণ্ডল পজিশন
                                </span>
                                <button type="button" onclick="peResetCrop()" class="text-xs text-slate-500 hover:text-slate-800 underline font-semibold">
                                    সেন্টার রিসেট
                                </button>
                            </h3>
                            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                                <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                                    <div class="flex justify-between text-xs font-bold text-slate-700 mb-1">
                                        <span>🔍 জুম (Zoom)</span>
                                        <span id="peValZoom" class="text-amber-600 font-mono">1.0x</span>
                                    </div>
                                    <input type="range" id="peSliderZoom" min="0.6" max="2.2" step="0.05" value="1.0" oninput="peUpdateCropVal()" class="w-full accent-amber-600">
                                </div>
                                <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                                    <div class="flex justify-between text-xs font-bold text-slate-700 mb-1">
                                        <span>↔️ ডানে/বামে (Pan X)</span>
                                        <span id="peValPanX" class="text-amber-600 font-mono">0%</span>
                                    </div>
                                    <input type="range" id="peSliderPanX" min="-50" max="50" step="1" value="0" oninput="peUpdateCropVal()" class="w-full accent-amber-600">
                                </div>
                                <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                                    <div class="flex justify-between text-xs font-bold text-slate-700 mb-1">
                                        <span>↕️ উপরে/নিচে (Pan Y)</span>
                                        <span id="peValPanY" class="text-amber-600 font-mono">0%</span>
                                    </div>
                                    <input type="range" id="peSliderPanY" min="-50" max="50" step="1" value="0" oninput="peUpdateCropVal()" class="w-full accent-amber-600">
                                </div>
                            </div>
                        </div>

                        <!-- PROCESS BUTTON -->
                        <div>
                            <button type="button" id="peProcessBtn" onclick="peProcessPhoto()"
                                class="w-full py-4 px-6 rounded-2xl bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-700 hover:from-blue-700 hover:via-indigo-700 hover:to-purple-800 text-white font-extrabold text-lg shadow-xl hover:shadow-2xl flex items-center justify-center gap-3 transition-all transform active:scale-98">
                                <span class="text-2xl">⚡</span>
                                <span>ছবি ফ্রেশ ও প্রসেস করুন (Create Studio Photo)</span>
                            </button>
                        </div>

                    </div>

                    <!-- Right Column: Live Studio Preview & Downloads (5 cols) -->
                    <div class="lg:col-span-5">
                        <div class="sticky top-6 space-y-6">

                            <!-- Studio Preview Card -->
                            <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-md">
                                <div class="flex items-center justify-between mb-4">
                                    <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2">
                                        <span>🖼️</span> স্টুডিও আউটপুট প্রিভিউ
                                    </h3>
                                    <span id="peDpiBadge" class="text-xs bg-emerald-100 text-emerald-800 px-2.5 py-1 rounded-full font-bold">
                                        ৩০০ DPI HD
                                    </span>
                                </div>

                                <!-- Preview Frame Container -->
                                <div class="relative bg-slate-100 rounded-xl p-4 flex flex-col items-center justify-center min-h-[380px] border border-slate-200 overflow-hidden">
                                    <!-- Placeholder when empty -->
                                    <div id="pePreviewPlaceholder" class="text-center p-6 text-slate-400">
                                        <div class="w-20 h-20 mx-auto mb-3 rounded-2xl bg-slate-200 flex items-center justify-center text-4xl text-slate-400">
                                            👤
                                        </div>
                                        <p class="font-bold text-slate-600 text-base mb-1">কোনো ছবি প্রস্তুত করা হয়নি</p>
                                        <p class="text-xs text-slate-400 max-w-xs">বাম পাশের অপশন থেকে ছবি আপলোড করে "ছবি ফ্রেশ ও প্রসেস করুন" বাটনে চাপুন</p>
                                    </div>

                                    <!-- Loading Spinner Overlay -->
                                    <div id="peLoadingOverlay" class="hidden absolute inset-0 bg-white/90 backdrop-blur-sm z-20 flex flex-col items-center justify-center p-6 text-center">
                                        <div class="w-14 h-14 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-4"></div>
                                        <p class="font-black text-slate-800 text-lg mb-1">ফটো ইঞ্জিনিয়ারিং চলছে...</p>
                                        <p class="text-xs text-slate-500 max-w-xs">এআই দিয়ে ব্যাকগ্রাউন্ড ব্লু কালার ও নিখুঁত ফোটো ফ্রেশ করা হচ্ছে, একটু অপেক্ষা করুন</p>
                                    </div>

                                    <!-- Result Image Display -->
                                    <div id="peResultWrapper" class="hidden relative max-w-full flex flex-col items-center">
                                        <div class="relative p-1.5 bg-white shadow-2xl rounded-lg border border-slate-300">
                                            <img id="peResultImg" src="" alt="Studio Photo" class="max-h-[360px] w-auto object-contain rounded">
                                            <!-- Original comparison overlay -->
                                            <img id="peOriginalCompareImg" src="" alt="Original Photo" class="hidden absolute inset-1.5 max-h-[360px] w-auto object-contain rounded pointer-events-none">
                                        </div>
                                        <!-- Compare button -->
                                        <div class="mt-3">
                                            <button type="button" id="peCompareBtn"
                                                onmousedown="peShowOriginal(true)" onmouseup="peShowOriginal(false)"
                                                ontouchstart="peShowOriginal(true)" ontouchend="peShowOriginal(false)"
                                                class="px-3 py-1.5 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-xs font-semibold shadow-sm transition flex items-center gap-1.5">
                                                <span>👁️</span> চেপে ধরে মূল ছবি দেখুন
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                <!-- Size & Info Badge -->
                                <div id="peInfoBox" class="mt-4 p-3 bg-blue-50/70 border border-blue-200 rounded-xl text-xs space-y-1">
                                    <div class="flex justify-between">
                                        <span class="text-slate-500 font-semibold">নির্বাচিত সাইজ:</span>
                                        <span id="peInfoSizeName" class="font-extrabold text-blue-900">পাসপোর্ট (বাংলাদেশ) - ৪০x৫০ মিমি</span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span class="text-slate-500 font-semibold">রেজুলোশন:</span>
                                        <span id="peInfoResolution" class="font-mono text-blue-800">৪৭২ x ৫৯১ পিক্সেল (৩০০ DPI)</span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span class="text-slate-500 font-semibold">ব্যাকগ্রাউন্ড:</span>
                                        <span id="peInfoBgColor" class="font-semibold text-blue-800">স্টুডিও ক্লাসিক ব্লু</span>
                                    </div>
                                </div>

                                <!-- Download & Print Buttons -->
                                <div class="mt-5 space-y-2.5">
                                    <div class="grid grid-cols-2 gap-2.5">
                                        <button type="button" id="peDownloadJpgBtn" onclick="peDownloadFile('jpg')" disabled
                                            class="py-3 px-4 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed text-white font-bold text-sm shadow flex items-center justify-center gap-2 transition">
                                            <span>📥</span> ডাউনলোড জেপিজি
                                        </button>
                                        <button type="button" id="peDownloadPngBtn" onclick="peDownloadFile('png')" disabled
                                            class="py-3 px-4 rounded-xl bg-slate-700 hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed text-white font-bold text-sm shadow flex items-center justify-center gap-2 transition">
                                            <span>📥</span> ডাউনলোড পিএনজি
                                        </button>
                                    </div>
                                    <!-- Print Sheet Generator Button -->
                                    <button type="button" id="pePrintSheetBtn" onclick="peOpenPrintSheetModal()" disabled
                                        class="w-full py-3.5 px-4 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-700 hover:from-emerald-700 hover:to-teal-800 disabled:opacity-40 disabled:cursor-not-allowed text-white font-black text-sm shadow flex items-center justify-center gap-2 transition">
                                        <span>🖨️</span> ৪-আর (4R) বা এ-৪ (A4) পেজে বহু কপি প্রিন্ট শিট তৈরি করুন
                                    </button>
                                    <!-- Direct Print Button -->
                                    <button type="button" id="peDirectPrintBtn" onclick="peDirectPrint()" disabled
                                        class="w-full py-2.5 px-4 rounded-xl border border-slate-300 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed text-slate-700 font-bold text-xs flex items-center justify-center gap-2 transition">
                                        <span>🖨️</span> সরাসরি এই ছবি প্রিন্ট করুন
                                    </button>
                                </div>

                            </div>

                            <!-- Studio Tips Banner -->
                            <div class="bg-indigo-50/60 rounded-xl p-4 border border-indigo-100 text-xs text-indigo-900 space-y-1.5">
                                <p class="font-bold flex items-center gap-1.5 text-indigo-950">
                                    <span>💡</span> স্টুডিও ফটো ইঞ্জিনিয়ারিং টিপস:
                                </p>
                                <ul class="list-disc list-inside space-y-1 text-indigo-800 text-[11px]">
                                    <li>সরকারি পাসপোর্ট ও চাকরির ছবির জন্য <b>স্টুডিও ব্লু</b> ব্যাকগ্রাউন্ড স্ট্যান্ডার্ড।</li>
                                    <li>ইউএস, কানাডা ও সেনজেন ভিসার জন্য <b>সাদা (White)</b> ব্যাকগ্রাউন্ড ব্যবহার করুন।</li>
                                    <li>"অটো ফ্রেশ" স্বয়ংক্রিয়ভাবে চেহারা উজ্জ্বল ও স্কিন স্মুথ করে প্রিন্টের উপযোগী করে।</li>
                                    <li>৪-আর (4R) ফটো পেপারে ৪টি বা ৬টি পাসপোর্ট ছবি একসাথে প্রিন্ট করতে প্রিন্ট শিট ব্যবহার করুন।</li>
                                </ul>
                            </div>

                        </div>
                    </div>

                </div>
            </div>
'''

# 2. Modals for Print Sheet and Webcam
modals_html = '''
    <!-- Photo Engineering: 4R/A4 Print Sheet Modal -->
    <div id="pePrintSheetModal" class="fixed inset-0 bg-black/80 hidden z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl max-w-4xl w-full max-h-[92vh] flex flex-col overflow-hidden shadow-2xl">
            <!-- Modal Header -->
            <div class="p-5 border-b border-slate-200 flex items-center justify-between bg-slate-50">
                <div>
                    <h3 class="text-xl font-bold text-slate-800 flex items-center gap-2">
                        <span>🖨️</span> স্টুডিও ফটো প্রিন্ট শিট জেনারেটর
                    </h3>
                    <p class="text-xs text-slate-500 mt-0.5">ফটো পেপারে প্রিন্ট করার জন্য একাধিক কপি সম্বলিত রেডি শিট</p>
                </div>
                <button onclick="peClosePrintSheetModal()" class="text-slate-400 hover:text-slate-700 text-2xl font-bold p-1">✕</button>
            </div>

            <!-- Modal Body -->
            <div class="p-6 overflow-y-auto flex-1 space-y-4">
                <!-- Controls Row -->
                <div class="flex flex-wrap items-center justify-between gap-4 p-3 bg-blue-50/60 rounded-xl border border-blue-200">
                    <div class="flex items-center gap-2">
                        <label class="text-xs font-bold text-slate-700">কাগজের সাইজ:</label>
                        <div class="inline-flex rounded-lg bg-white p-1 border border-slate-300">
                            <button type="button" id="peSheet4RBtn" onclick="peSetSheetSize('4r')"
                                class="px-3 py-1 rounded text-xs font-bold bg-blue-600 text-white shadow-sm">
                                ৪-আর (4R - 4x6 ইঞ্চি)
                            </button>
                            <button type="button" id="peSheetA4Btn" onclick="peSetSheetSize('a4')"
                                class="px-3 py-1 rounded text-xs font-bold text-slate-600 hover:text-blue-600">
                                এ-৪ (A4 শিট)
                            </button>
                        </div>
                    </div>
                    <label class="inline-flex items-center gap-2 cursor-pointer text-xs font-bold text-slate-700">
                        <input type="checkbox" id="peSheetBorderToggle" checked onchange="peGeneratePrintSheet()" class="w-4 h-4 text-blue-600 rounded">
                        <span>✂️ কাটার সুবিধার জন্য হালকা বর্ডার দাগ</span>
                    </label>
                </div>

                <!-- Sheet Preview Container -->
                <div class="bg-slate-100 rounded-xl p-4 flex items-center justify-center min-h-[350px] border border-slate-200">
                    <div id="peSheetLoading" class="hidden text-center p-6">
                        <div class="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-3"></div>
                        <p class="text-sm font-bold text-slate-700">প্রিন্ট শিট তৈরি হচ্ছে...</p>
                    </div>
                    <img id="peSheetPreviewImg" src="" class="max-h-[50vh] w-auto object-contain rounded shadow-lg border border-slate-300 bg-white">
                </div>
            </div>

            <!-- Modal Footer -->
            <div class="p-5 border-t border-slate-200 bg-slate-50 flex items-center justify-between">
                <button onclick="peClosePrintSheetModal()" class="px-5 py-2.5 bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold rounded-xl text-sm transition">
                    বন্ধ করুন
                </button>
                <div class="flex items-center gap-3">
                    <button onclick="peDownloadPrintSheet()" class="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl text-sm transition shadow flex items-center gap-2">
                        <span>📥</span> প্রিন্ট শিট ডাউনলোড (JPG)
                    </button>
                    <button onclick="pePrintSheetNow()" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-sm transition shadow flex items-center gap-2">
                        <span>🖨️</span> এখনই প্রিন্ট করুন
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Photo Engineering: Webcam Camera Modal -->
    <div id="peWebcamModal" class="fixed inset-0 bg-black/85 hidden z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl max-w-xl w-full overflow-hidden shadow-2xl flex flex-col">
            <div class="p-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
                <h3 class="text-base font-bold text-slate-800 flex items-center gap-2">
                    <span>📸</span> ওয়েবক্যাম / ক্যামেরা দিয়ে ছবি তুলুন
                </h3>
                <button onclick="peCloseWebcam()" class="text-slate-400 hover:text-slate-700 text-xl font-bold">✕</button>
            </div>
            <div class="p-4 bg-black flex items-center justify-center relative min-h-[320px]">
                <video id="peWebcamVideo" autoplay playsinline class="w-full max-h-[380px] object-cover rounded-lg"></video>
                <!-- Flash effect overlay -->
                <div id="peWebcamFlash" class="hidden absolute inset-0 bg-white z-10 transition-opacity duration-300"></div>
                <canvas id="peWebcamCanvas" class="hidden"></canvas>
            </div>
            <div class="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between">
                <button onclick="peCloseWebcam()" class="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold rounded-xl text-xs transition">
                    বাতিল
                </button>
                <button onclick="peCaptureWebcam()" class="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl text-sm transition shadow flex items-center gap-2">
                    <span>📸</span> ছবি তুলুন (Snapshot)
                </button>
            </div>
        </div>
    </div>
'''

# 3. JavaScript Block for Photo Engineering
photo_js = '''
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
'''

# Target 1: Insert Photo Engineering Tab
target1 = '''                    </div>
                </div>
            </div>

        </div>
    </div>'''

replacement1 = f'''                    </div>
                </div>
            </div>
{photo_tab_html}
        </div>
    </div>'''

if target1 in html:
    html = html.replace(target1, replacement1, 1)
    print("Tab HTML inserted successfully!")
else:
    print("Error: target1 not found!")

# Target 2: Insert Modals before </body>
target2 = '</body>'
replacement2 = f'''{modals_html}
</body>'''

if target2 in html:
    html = html.replace(target2, replacement2, 1)
    print("Modals inserted successfully!")
else:
    print("Error: target2 (</body>) not found!")

# Target 3: Insert JS before </script>
target3 = '    </script>\n</body>'
replacement3 = f'''{photo_js}
    </script>
</body>'''

if target3 in html:
    html = html.replace(target3, replacement3, 1)
    print("JS inserted successfully!")
else:
    # Alternative target for closing script
    idx = html.rfind('</script>')
    if idx != -1:
        html = html[:idx] + photo_js + '\n' + html[idx:]
        print("JS inserted at rfind('</script>')!")

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html updated successfully!")

