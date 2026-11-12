
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

function findBalancedBackwards(str, closeIdx, openChar, closeChar) {
    let depth = 0;
    for (let i = closeIdx; i >= 0; i--) {
        if (str[i] === closeChar) depth++;
        else if (str[i] === openChar) {
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

        let ommlFraction = `<m:f><m:num>${num}</m:num><m:den>${den}</m:den></m:f>`;
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

    // Parse roots
    f = parseRootsToWordHtml(f);
    // Parse fractions
    f = parseFractionsToWordHtml(f);
    // Parse scripts
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

    // Wrap plain text in runs and the entire formula in m:oMath
    let wrapped = wrapOmmlRuns(f);
    return `<m:oMath>${wrapped}</m:oMath>`;
}

const tests = [
    "x^3 + \\frac{1}{x^3} = 5\\sqrt{2}",
    "x_1^2 + y_2^2 = 25",
    "\\sqrt{x^2 - 3} = 2\\sqrt{2}"
];

tests.forEach(t => {
    console.log("LaTeX Input: " + t);
    console.log("OMML Output: " + cleanLaTeXFormula(t));
    console.log("-----------------------------------------");
});
