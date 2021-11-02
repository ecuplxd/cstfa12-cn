const fs = require('fs');
const path = require('path');
const prettier = require('prettier');

const packageMetaKeys = [
    'scripts',
    'dependencies',
    'peerDependencies',
    'bin',
    'build',
    'angularCompilerOptions',
    'compilerOptions',
    '$schema',
];
const codePath = path.normalize('/code/');
let log = loadLogs();

function revertObj(obj) {
    let result = {};

    for (const key in obj) {
        if (Object.hasOwnProperty.call(obj, key)) {
            result[obj[key]] = key;
        }
    }

    return result;
}

class Wrapper {
    static parsers = {
        json: 'json',
        dot: 'typescript',
        step: 'typescript',
        typescript: 'typescript',
    };

    static parserIs(kind) {
        return Wrapper.parsers[kind];
    }

    static getParser(kind) {
        return Wrapper.parserIs(kind);
    }

    constructor(kind, code) {
        this.code = code.replace(/…/g, '...');
        this.kind = kind || 'typescript';
        this.lastIsComma = false;

        if (this.kind === 'json') {
            this.code = this.code.replace(/\\"/g, '**');
        }

        this.mergeMultiString();
        this.patchBracket();
    }

    completeComment() {
        this.code = this.code
            .split(' ')
            .map((ch) => {
                return ch.startsWith('**') ? '/' + ch : ch;
            })
            .join(' ');
    }

    execute(kind) {
        this.kind = kind || this.kind;

        switch (this.kind) {
            case 'json': {
                this.wrapJSON();
                break;
            }
            case 'dot': {
                this.wrapDot();
                break;
            }
            case 'step': {
                this.wrapStep();
                break;
            }
            case 'typescript': {
                this.wrapClass();
                break;
            }
            default:
                break;
        }

        return this.code;
    }

    removeSpace(text) {
        return text.includes('//') && !text.includes('://')
            ? text
            : text
                  .split(' ')
                  .map((item) => item.trim())
                  .filter(Boolean)
                  .join(' ');
    }

    mergeMultiString() {
        this.code = this.code.replace(/'.*?'/gs, (match) =>
            this.removeSpace(match)
        );
        this.code = this.code.replace(/".*?"/gs, (match) =>
            this.removeSpace(match)
        );
    }

    patchBracket() {
        const results = [];
        const codes = this.code.split('');
        const stacks = [];
        const openBrackets = {
            '(': ')',
            '[': ']',
            // '"': '"',
            // "'": "'",
            '{': '}',
            // '`': '`',
        };
        const closeBrackets = revertObj(openBrackets);

        codes.forEach((ch) => {
            if (openBrackets[ch]) {
                stacks.push(ch);
            } else if (closeBrackets[ch]) {
                while (stacks.length) {
                    const top = stacks.pop();

                    if (closeBrackets[ch] !== top) {
                        this.kind !== 'json'
                            ? results.push('..\n' + openBrackets[top])
                            : results.push(openBrackets[top]);
                    } else {
                        break;
                    }
                }
            }

            results.push(ch);
        });

        while (stacks.length) {
            const top = stacks.pop();

            this.kind !== 'json'
                ? results.push('..\n' + openBrackets[top])
                : results.push(openBrackets[top]);
        }

        this.code = results.join('');

        return this.code;
    }

    wrapJSON() {
        const codes = this.code
            .trim()
            .split('\n')
            .map((item) => item.trim())
            .filter(Boolean);
        let result = codes
            .map((item, i) => {
                const LastKey =
                    codes[i + 1] && codes[i + 1].trim().includes('}');

                if (item.includes('..')) {
                    const keyValue = `"|": "${item.replace(',', '')}"`;

                    return LastKey ? keyValue : keyValue + ',';
                }

                return item;
            })
            .join('\n');

        if (result.substr(-1) === ',') {
            this.lastIsComma = true;
            result = result.substring(0, result.length - 1);
        }

        this.code = '{\n' + result + '}';

        return this.code;
    }

    isLineBreak(text) {
        return text.indexOf('\r') !== -1 || text.indexOf('\n') !== -1;
    }

    wrapDot() {
        this.code = this.code.replace(/\.{2,}[\])}\s]+/g, (match) => {
            match = match.trim();
            const lastDot = match.lastIndexOf('.') + 1;

            return (
                '//|' +
                match.substring(0, lastDot) +
                '\n' +
                match.substring(lastDot)
            );
        });

        return this.code;
    }

    wrapStep() {
        const codes = this.code.split('');
        const chars = new Set(['a', 'b', 'c', 'd', 'e']);
        const results = [];

        for (let i = 0; i < codes.length; i++) {
            let ch = codes[i];
            const next = codes[i + 1];
            const prev = codes[i - 1];
            const num = parseInt(ch);

            if (isNaN(num)) {
                if (ch === '%') {
                    if (next === '\\') {
                        ch = `/*${ch}`;
                    } else if (prev === '}') {
                        ch = `${ch}*/`;
                    }
                }
            } else {
                if (
                    (/\s/.test(next) && /\s/.test(prev)) ||
                    prev === '}' ||
                    chars.has(next)
                ) {
                    ch = `/*%\\step{${ch + next.trim()}}%*/`;
                    i++;
                }
            }

            results.push(ch);
        }

        this.code = results.join('');

        return this.code;
    }

    wrapClass() {
        this.code = `class A{` + this.code + '}';

        return this.code;
    }

    unwrap(code) {
        this.code = code.trim();

        switch (this.kind) {
            case 'json': {
                this.unwrapJson();
                break;
            }
            case 'dot': {
                this.unwrapDot();
                break;
            }
            case 'step': {
                this.unwrapDot();
                this.unwrapStep();
                break;
            }
            case 'typescript': {
                this.unwrapDot();
                this.unwrapStep();
                this.unwrapClass();
                break;
            }
            default:
                break;
        }

        return this.code;
    }

    unwrapJson() {
        const codes = this.code
            .split('\n')
            .slice(1, -1)
            .map((item) =>
                item.includes('"|"')
                    ? item.replace(/: /g, '').replace(/[|"]/g, '')
                    : item
            );
        const last = codes.length - 1;

        if (this.lastIsComma) {
            codes[last] = codes[last] + ',';
        }

        codes.push('');

        this.code = codes.join('\n');

        return this.code;
    }

    unwrapDot() {
        let result = this.code.replace(/\/\/\|/g, () => '');

        this.code = result + '\n';

        return this.code;
    }

    unwrapStep() {
        let result = this.code.trim().replace(/\/\*%/g, () => '%');

        result = result.replace(/%\*\//g, () => '%');

        this.code = result + '\n';

        return this.code;
    }

    unwrapClass() {
        const codes = this.code.trim().split('\n').slice(1, -1);

        this.code = codes.join('\n');

        return this.unwrapDot();
    }
}

function travel(dir, callback) {
    fs.readdirSync(dir).forEach((file) => {
        const pathName = path.join(dir, file);

        if (fs.statSync(pathName).isDirectory()) {
            travel(pathName, callback);
        } else {
            callback(pathName);
        }
    });
}

function getCode(fileName) {
    const data = fs.readFileSync(fileName, 'utf-8');
    const code = data.trim().split('\n').slice(1, -1).join('\n');
    const parser = chooseParser(code);

    return {
        code: Wrapper.parserIs('typescript')
            ? code.replace('Export ', 'export')
            : code,
        parser,
    };
}

function writeResult(code, fileName, lang) {
    const result = '\\begin{minted}{' + lang + '}\n' + code + '\\end{minted}\n';

    fs.writeFileSync(fileName, result);
}

function loadLogs() {
    const data = fs.readFileSync('./log.json', 'utf-8');

    return JSON.parse(data);
}

function chooseParser(code) {
    const firstChar = code[0];

    if (firstChar == '{' || firstChar == '"') {
        return 'json';
    }

    for (let i = 0; i < packageMetaKeys.length; i++) {
        if (code.includes(`"${packageMetaKeys[i]}": `)) {
            return 'json';
        }
    }

    return 'typescript';
}

function addLog(fileName, success, error) {
    const basename = path.basename(fileName);

    log[basename] = success;

    if (!success && error) {
        console.warn(fileName, '格式化失败，原因：', error.message);
    }
}

function shouldSkip(fileName) {
    const basename = path.basename(fileName);

    if (log[basename] && log[basename] !== undefined) {
        // console.info(basename, '已格式化成功，跳过。');
    }

    // return log[basename] || !path.normalize(fileName).includes(codePath);
    return !path.normalize(fileName).includes(codePath);
}

function tryToFix(code, parser, fileName) {
    const tryParsers = parser === 'json' ? [parser] : ['dot', 'step', parser];
    const wrap = new Wrapper(parser, code);
    let lastError = '';

    for (let i = 0; i < tryParsers.length; i++) {
        parser = tryParsers[i];

        wrap.execute(parser);

        try {
            const lang = Wrapper.getParser(parser);
            const result = format(wrap.code, lang);

            writeResult(wrap.unwrap(result), fileName, lang);
            lastError = '';

            break;
        } catch (error) {
            lastError = error;
        }
    }

    return lastError;
}

function format(code, parser) {
    return prettier.format(code, {
        parser,
        singleQuote: true,
    });
}

travel('./output', function (fileName) {
    if (!shouldSkip(fileName)) {
        const { code, parser } = getCode(fileName);

        if (fileName.includes('14_4_24.tex')) {
            let a = 1;
        }
        try {
            writeResult(format(code, parser), fileName, parser);
            addLog(fileName, true);
        } catch (error) {
            const tryResult = tryToFix(code, parser, fileName);

            addLog(fileName, !tryResult, tryResult);
        }
    }
});

fs.writeFileSync('log.json', JSON.stringify(log, null, 2));
