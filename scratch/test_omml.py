import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def findBalancedBrace(str_val, startIdx):
    depth = 0
    for i in range(startIdx, len(str_val)):
        if str_val[i] == '{':
            depth += 1
        elif str_val[i] == '}':
            depth -= 1
            if depth == 0:
                return i
    return -1

def findBalancedBackwards(str_val, closeIdx, openChar, closeChar):
    depth = 0
    for i in range(closeIdx, -1, -1):
        if str_val[i] == closeChar:
            depth += 1
        elif str_val[i] == openChar:
            depth -= 1
            if depth == 0:
                return i
    return -1

def findBalancedBraceBackwards(str_val, closeIdx):
    return findBalancedBackwards(str_val, closeIdx, '{', '}')

def findBalancedParenthesisBackwards(str_val, closeIdx):
    return findBalancedBackwards(str_val, closeIdx, '(', ')')

def findBalancedBracketBackwards(str_val, closeIdx):
    return findBalancedBackwards(str_val, closeIdx, '[', ']')

def findMatchingOpenTag(str_val, closeTagEndIdx):
    p = closeTagEndIdx
    tagStart = str_val.rfind('<', 0, p)
    if tagStart == -1:
        return -1
    tagText = str_val[tagStart:p + 1]
    match = re.match(r"^</([a-zA-Z0-9:]+)>", tagText)
    if not match:
        return -1
    tagName = match.group(1)

    depth = 1
    currentIdx = tagStart
    while depth > 0 and currentIdx > 0:
        prevTagStart = str_val.rfind('<', 0, currentIdx)
        if prevTagStart == -1:
            return -1
        prevTagEnd = str_val.find('>', prevTagStart)
        if prevTagEnd == -1:
            return -1
        prevTagText = str_val[prevTagStart:prevTagEnd + 1]
        
        if prevTagText.startswith('</' + tagName + '>'):
            depth += 1
        elif prevTagText.startswith('<' + tagName + '>') or prevTagText.startswith('<' + tagName + ' '):
            depth -= 1
        currentIdx = prevTagStart
    return currentIdx

def extractScript(str_val, scriptCharIdx):
    rest = str_val[scriptCharIdx + 1:]
    if rest.startswith('{'):
        braceEnd = findBalancedBrace(str_val, scriptCharIdx + 1)
        if braceEnd != -1:
            return {
                'content': str_val[scriptCharIdx + 2:braceEnd],
                'endIndex': braceEnd + 1
            }
    p = 0
    while p < len(rest) and rest[p].isspace():
        p += 1
    if p < len(rest):
        if rest[p] == '\\':
            cmdMatch = re.match(r"^\\[a-zA-Z]+", rest[p:])
            if cmdMatch:
                cmd = cmdMatch.group(0)
                return {
                    'content': cmd,
                    'endIndex': scriptCharIdx + 1 + p + len(cmd)
                }
        return {
            'content': rest[p],
            'endIndex': scriptCharIdx + 1 + p + 1
        }
    return None

def findBaseData(str_val, scriptCharIdx):
    p = scriptCharIdx - 1
    while p >= 0 and str_val[p].isspace():
        p -= 1
    if p < 0:
        return None
    
    char = str_val[p]
    if char == '}':
        openBrace = findBalancedBraceBackwards(str_val, p)
        if openBrace != -1:
            return {
                'text': str_val[openBrace + 1:p],
                'startIndex': openBrace
            }
    elif char == ')':
        openParen = findBalancedParenthesisBackwards(str_val, p)
        if openParen != -1:
            return {
                'text': str_val[openParen + 1:p],
                'startIndex': openParen
            }
    elif char == ']':
        openBracket = findBalancedBracketBackwards(str_val, p)
        if openBracket != -1:
            return {
                'text': str_val[openBracket + 1:p],
                'startIndex': openBracket
            }
    elif char == '>':
        openTag = findMatchingOpenTag(str_val, p)
        if openTag != -1:
            return {
                'text': str_val[openTag:p + 1],
                'startIndex': openTag
            }
    else:
        sub = str_val[:p + 1]
        match = re.search(r"(\\[a-zA-Z]+|[a-zA-Z0-9θαβ∞∠△°·×÷±≈≠≤≥∈ℕℤ∖∪∩]+)$", sub)
        if match:
            text = match.group(1)
            return {
                'text': text,
                'startIndex': p + 1 - len(text)
            }
        return {
            'text': char,
            'startIndex': p
        }
    return None

def parseScriptsToWordHtml(str_val):
    f = str_val
    idx = -1
    for i in range(len(f)):
        if f[i] == '^' or f[i] == '_':
            lastOpen = f.rfind('<', 0, i)
            lastClose = f.rfind('>', 0, i)
            if lastOpen > lastClose:
                continue
            idx = i
            break
    if idx == -1:
        return f
    
    isSup = (f[idx] == '^')
    script1Data = extractScript(f, idx)
    if not script1Data:
        nextStr = f[:idx] + f[idx + 1:]
        return parseScriptsToWordHtml(nextStr)
    
    script1Content = script1Data['content']
    script1End = script1Data['endIndex']
    
    hasSecondScript = False
    script2IsSup = False
    script2Data = None
    
    nextCharIdx = script1End
    while nextCharIdx < len(f) and f[nextCharIdx].isspace():
        nextCharIdx += 1
    
    if nextCharIdx < len(f):
        char = f[nextCharIdx]
        if (isSup and char == '_') or (not isSup and char == '^'):
            hasSecondScript = True
            script2IsSup = (char == '^')
            script2Data = extractScript(f, nextCharIdx)
    
    baseData = findBaseData(f, idx)
    if not baseData:
        nextStr = f[:idx] + script1Content + f[script1End:]
        return parseScriptsToWordHtml(nextStr)
    
    baseText = baseData['text']
    baseStart = baseData['startIndex']
    
    baseText = parseScriptsToWordHtml(baseText)
    script1Content = parseScriptsToWordHtml(script1Content)
    
    script2Content = ""
    replacementEndIdx = script1End
    if hasSecondScript and script2Data:
        script2Content = parseScriptsToWordHtml(script2Data['content'])
        replacementEndIdx = script2Data['endIndex']
    
    replacement = ""
    if hasSecondScript:
        subContent = script2Content if isSup else script1Content
        supContent = script1Content if isSup else script2Content
        replacement = f"<m:sSubSup><m:e>{baseText}</m:e><m:sub>{subContent}</m:sub><m:sup>{supContent}</m:sup></m:sSubSup>"
    else:
        if isSup:
            replacement = f"<m:sSup><m:e>{baseText}</m:e><m:sup>{script1Content}</m:sup></m:sSup>"
        else:
            replacement = f"<m:sSub><m:e>{baseText}</m:e><m:sub>{script1Content}</m:sub></m:sSub>"
    
    nextStr = f[:baseStart] + replacement + f[replacementEndIdx:]
    return parseScriptsToWordHtml(nextStr)

def parseFractionsToWordHtml(str_val):
    f = str_val
    index = f.find('\\frac')
    while index != -1:
        numStart = f.find('{', index)
        if numStart == -1:
            break
        numEnd = findBalancedBrace(f, numStart)
        if numEnd == -1:
            break
        num = f[numStart + 1:numEnd]

        denStart = f.find('{', numEnd)
        if denStart == -1 or denStart != numEnd + 1:
            spacesStr = f[numEnd + 1:]
            matchSpaces = re.match(r"^\s*\{", spacesStr)
            if matchSpaces:
                denStart = numEnd + 1 + spacesStr.find('{')
            else:
                break
        denEnd = findBalancedBrace(f, denStart)
        if denEnd == -1:
            break
        den = f[denStart + 1:denEnd]

        num = parseFractionsToWordHtml(num)
        den = parseFractionsToWordHtml(den)

        ommlFraction = f"<m:f><m:num>{num}</m:num><m:den>{den}</m:den></m:f>"
        f = f[:index] + ommlFraction + f[denEnd + 1:]
        index = f.find('\\frac')
    return f

def parseRootsToWordHtml(str_val):
    f = str_val
    index = f.find('\\sqrt')
    while index != -1:
        rest = f[index + 5:]
        braceMatch = re.match(r"^\s*\{", rest)
        if braceMatch:
            numStart = index + 5 + rest.find('{')
            numEnd = findBalancedBrace(f, numStart)
            if numEnd != -1:
                content = f[numStart + 1:numEnd]
                content = parseRootsToWordHtml(content)
                ommlRoot = f"<m:rad><m:radPr><m:degHide m:val=\"on\"/></m:radPr><m:e>{content}</m:e></m:rad>"
                f = f[:index] + ommlRoot + f[numEnd + 1:]
                index = f.find('\\sqrt')
                continue
        
        nextCharIdx = index + 5
        while nextCharIdx < len(f) and f[nextCharIdx].isspace():
            nextCharIdx += 1
        if nextCharIdx < len(f):
            char = f[nextCharIdx]
            ommlRoot = f"<m:rad><m:radPr><m:degHide m:val=\"on\"/></m:radPr><m:e>{char}</m:e></m:rad>"
            f = f[:index] + ommlRoot + f[nextCharIdx + 1:]
        else:
            f = f[:index] + '√' + f[index + 5:]
        index = f.find('\\sqrt')
    return f

def wrapOmmlRuns(str_val):
    # Split by XML tags
    segments = re.split(r"(<\/?[a-zA-Z0-9:]+(?:\s+[a-zA-Z0-9:]+=\"[^\"]*\")*\/?>)", str_val)
    result = ""
    for seg in segments:
        if not seg:
            continue
        if seg.startswith('<') and seg.endswith('>'):
            result += seg
        else:
            cleanSeg = seg.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            result += f"<m:r><m:t>{cleanSeg}</m:t></m:r>"
    return result

def cleanLaTeXFormula(formula):
    f = formula
    f = re.sub(r"\\text\s*\{([^}]+)\}", r"\1", f)
    f = re.sub(r"(?:\\t|\t)ext\s*\{?([^}]*)\}?", r"\1", f)
    f = re.sub(r"\bext([a-zA-Z]+)", r" \1", f)
    f = re.sub(r"\\dot\s*\{([^}]+)\}", r"\1̇", f)

    # Parse roots
    f = parseRootsToWordHtml(f)
    # Parse fractions
    f = parseFractionsToWordHtml(f)
    # Parse scripts
    f = parseScriptsToWordHtml(f)

    replacements = [
        (re.compile(r"\\in\b"), ' ∈ '),
        (re.compile(r"\\mathbb\{N\}"), 'ℕ'),
        (re.compile(r"\\mathbb\s+N"), 'ℕ'),
        (re.compile(r"\\mathbb\s+Z"), 'ℤ'),
        (re.compile(r"\\setminus\b"), ' ∖ '),
        (re.compile(r"\\backslash\b"), ' ∖ '),
        (re.compile(r"\\cup\b"), ' ∪ '),
        (re.compile(r"\\cap\b"), ' ∩ '),
        (re.compile(r"\\theta\b"), 'θ'),
        (re.compile(r"\\sin\b"), 'sin'),
        (re.compile(r"\\cos\b"), 'cos'),
        (re.compile(r"\\tan\b"), 'tan'),
        (re.compile(r"\\cot\b"), 'cot'),
        (re.compile(r"\\angle\b"), '∠'),
        (re.compile(r"\\circ\b"), '°'),
        (re.compile(r"\\triangle\b"), '△'),
        (re.compile(r"\\le\b"), ' ≤ '),
        (re.compile(r"\\ge\b"), ' ≥ '),
        (re.compile(r"\\cdot\b"), '·'),
        (re.compile(r"\\div\b"), ' ÷ '),
        (re.compile(r"\\times\b"), ' × '),
        (re.compile(r"\\approx\b"), ' ≈ '),
        (re.compile(r"\\neq\b"), ' ≠ '),
        (re.compile(r"\\pm\b"), ' ± '),
        (re.compile(r"\\infty\b"), ' ∞ '),
        (re.compile(r"\\alpha\b"), 'α'),
        (re.compile(r"\\beta\b"), 'β'),
        (re.compile(r"\\quad\b"), '   '),
        (re.compile(r"\\,"), ' '),
        (re.compile(r"\\;"), ' '),
        (re.compile(r"\\\{"), '{'),
        (re.compile(r"\\\}"), '}')
    ]

    for regex, replace in replacements:
        f = regex.sub(replace, f)

    wrapped = wrapOmmlRuns(f)
    return f"<m:oMath>{wrapped}</m:oMath>"

tests = [
    r"x^3 + \frac{1}{x^3} = 5\sqrt{2}",
    r"x_1^2 + y_2^2 = 25",
    r"\sqrt{x^2 - 3} = 2\sqrt{2}"
]

for t in tests:
    print(f"LaTeX Input: {t}")
    print(f"OMML Output: {cleanLaTeXFormula(t)}")
    print("-----------------------------------------")
