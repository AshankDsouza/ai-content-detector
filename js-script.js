const a0_0x3f367b = a0_0x1b37;
(function(_0x18d7ff, _0x5919dd) {
    const _0x255b38 = a0_0x1b37
      , _0x29620a = _0x18d7ff();
    while (!![]) {
        try {
            const _0x2d57aa = parseInt(_0x255b38(0x131)) / 0x1 + parseInt(_0x255b38(0x161)) / 0x2 + parseInt(_0x255b38(0x135)) / 0x3 + -parseInt(_0x255b38(0x158)) / 0x4 * (parseInt(_0x255b38(0x13c)) / 0x5) + parseInt(_0x255b38(0x139)) / 0x6 * (-parseInt(_0x255b38(0x11b)) / 0x7) + -parseInt(_0x255b38(0x14c)) / 0x8 + -parseInt(_0x255b38(0x167)) / 0x9 * (parseInt(_0x255b38(0x15c)) / 0xa);
            if (_0x2d57aa === _0x5919dd)
                break;
            else
                _0x29620a['push'](_0x29620a['shift']());
        } catch (_0x5cf01b) {
            _0x29620a['push'](_0x29620a['shift']());
        }
    }
}(a0_0x46af, 0xbf740));
let results = [];
const creationThresholdDate = new Date(a0_0x3f367b(0x125))[a0_0x3f367b(0x126)]();
function a0_0x1b37(_0x18eb64, _0x2f36fe) {
    const _0x46af99 = a0_0x46af();
    return a0_0x1b37 = function(_0x1b375e, _0x2f4f4a) {
        _0x1b375e = _0x1b375e - 0x108;
        let _0x4e4d3b = _0x46af99[_0x1b375e];
        return _0x4e4d3b;
    }
    ,
    a0_0x1b37(_0x18eb64, _0x2f36fe);
}
async function processFiles() {
    const _0x4fbf36 = a0_0x3f367b
      , _0x405b68 = document[_0x4fbf36(0x11d)](_0x4fbf36(0x146))[_0x4fbf36(0x145)]
      , _0x1a8f3c = document[_0x4fbf36(0x11d)](_0x4fbf36(0x16e));
    results = [],
    _0x1a8f3c[_0x4fbf36(0x128)] = '';
    if (_0x405b68[_0x4fbf36(0x163)] === 0x0) {
        _0x1a8f3c[_0x4fbf36(0x128)] = _0x4fbf36(0x118);
        return;
    }
    for (const _0xa91b2d of _0x405b68) {
        if (_0xa91b2d[_0x4fbf36(0x142)] && _0xa91b2d[_0x4fbf36(0x142)] >= creationThresholdDate) {
            let _0x2f2b0c = '';
            try {
                if (_0xa91b2d['type'] === _0x4fbf36(0x138))
                    window['fullres'] ||= {
                        'events': []
                    },
                    window[_0x4fbf36(0x15e)][_0x4fbf36(0x157)][_0x4fbf36(0x16b)]({
                        'key': _0x4fbf36(0x153),
                        'fileType': 'PDF'
                    }),
                    _0x2f2b0c = await readPDF(_0xa91b2d);
                else {
                    if (_0xa91b2d[_0x4fbf36(0x119)][_0x4fbf36(0x156)]('wordprocessingml'))
                        window[_0x4fbf36(0x15e)] ||= {
                            'events': []
                        },
                        window[_0x4fbf36(0x15e)][_0x4fbf36(0x157)][_0x4fbf36(0x16b)]({
                            'key': _0x4fbf36(0x153),
                            'fileType': 'Word'
                        }),
                        _0x2f2b0c = await readDocx(_0xa91b2d);
                    else {
                        window[_0x4fbf36(0x15e)] ||= {
                            'events': []
                        },
                        window[_0x4fbf36(0x15e)][_0x4fbf36(0x157)][_0x4fbf36(0x16b)]({
                            'key': _0x4fbf36(0x178),
                            'fileName': _0xa91b2d[_0x4fbf36(0x173)],
                            'fileType': _0xa91b2d['type']
                        }),
                        _0x1a8f3c[_0x4fbf36(0x128)] += '<p>' + _0xa91b2d['name'] + _0x4fbf36(0x12d);
                        continue;
                    }
                }
                const _0x4db0b4 = (_0x2f2b0c['match'](/['"]/g) || [])[_0x4fbf36(0x163)]
                  , _0x2d5442 = (_0x2f2b0c[_0x4fbf36(0x130)](/[“”‘’]/g) || [])[_0x4fbf36(0x163)]
                  , _0x2fcd5e = /(?:\bchat[\s-]?gpt\b|chatgpt\b|chat\s+gpt\b)/i[_0x4fbf36(0x16f)](_0x2f2b0c)
                  , _0x4237d9 = /\bgrammarly\b(?=\s|[.,;:/-]|$)/i['test'](_0x2f2b0c)
                  , _0x30bd07 = /\bclaude\b(?=\s|[.,;:/-]|$)/i['test'](_0x2f2b0c)
                  , _0x3fdbf6 = /\bgemini\b(?=\s|[.,;:/-]|$)/i[_0x4fbf36(0x16f)](_0x2f2b0c)
                  , _0xf333cc = /\b(llama|meta)\b(?=\s|[.,;:/-]|$)/i['test'](_0x2f2b0c)
                  , _0x76a5c7 = /\bcopilot\b(?=\s|[.,;:/-]|$)/i[_0x4fbf36(0x16f)](_0x2f2b0c)
                  , _0x2fb3d7 = !_0x2fcd5e && !_0x4237d9 && !_0x30bd07 && !_0x3fdbf6 && !_0xf333cc && !_0x76a5c7;
                let _0x5c93df;
                if (_0x4db0b4 > 0x0 && _0x2fb3d7 && _0x2d5442 == 0x0)
                    _0x5c93df = _0x4fbf36(0x168);
                else
                    _0x4db0b4 > 0x0 && _0x2fb3d7 ? _0x5c93df = _0x4fbf36(0x151) : _0x5c93df = 'green';
                _0x1a8f3c[_0x4fbf36(0x128)] += _0x4fbf36(0x14f) + _0x5c93df + _0x4fbf36(0x149) + _0xa91b2d[_0x4fbf36(0x173)] + _0x4fbf36(0x155) + _0x4db0b4 + '<br>\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20ChatGPT\x20Mentioned:\x20' + (_0x2fcd5e ? _0x4fbf36(0x14a) : 'No') + _0x4fbf36(0x176) + (_0x4237d9 ? _0x4fbf36(0x14a) : 'No') + _0x4fbf36(0x10a) + (_0x30bd07 ? _0x4fbf36(0x14a) : 'No') + '<br>\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20Gemini\x20Mentioned:\x20' + (_0x3fdbf6 ? _0x4fbf36(0x14a) : 'No') + '<br>\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20Llama/Meta\x20Mentioned:\x20' + (_0xf333cc ? 'Yes' : 'No') + _0x4fbf36(0x13b) + (_0x76a5c7 ? _0x4fbf36(0x14a) : 'No') + _0x4fbf36(0x10f),
                results[_0x4fbf36(0x16b)]({
                    'fileName': _0xa91b2d['name'],
                    'aiTracesCount': _0x4db0b4,
                    'regularTracesCount': _0x2d5442,
                    'gptDetected': _0x2fcd5e ? 'Yes' : 'No',
                    'grammarlyDetected': _0x4237d9 ? _0x4fbf36(0x14a) : 'No',
                    'claudeDetected': _0x30bd07 ? _0x4fbf36(0x14a) : 'No',
                    'geminiDetected': _0x3fdbf6 ? 'Yes' : 'No',
                    'llamaMetaDetected': _0xf333cc ? 'Yes' : 'No',
                    'copilotDetected': _0x76a5c7 ? _0x4fbf36(0x14a) : 'No'
                }),
                document[_0x4fbf36(0x11d)]('feedback')['style'][_0x4fbf36(0x15f)] = _0x4fbf36(0x144);
            } catch (_0x24837f) {
                _0x1a8f3c['innerHTML'] += '<p>' + _0xa91b2d[_0x4fbf36(0x173)] + _0x4fbf36(0x169) + _0x24837f[_0x4fbf36(0x13f)] + _0x4fbf36(0x137);
            }
        } else
            _0x1a8f3c['innerHTML'] += '<p>' + _0xa91b2d[_0x4fbf36(0x173)] + _0x4fbf36(0x141);
    }
    results[_0x4fbf36(0x163)] > 0x0 && (createCSVDownloadLink(results),
    createExcelDownloadLink(results));
}
async function readPDF(_0x200848) {
    const _0x69919d = new FileReader();
    return new Promise( (_0x590d13, _0x4ffb14) => {
        const _0x5478f8 = a0_0x1b37;
        _0x69919d[_0x5478f8(0x175)] = async _0x4abfe1 => {
            const _0x2a9b93 = _0x5478f8;
            try {
                const _0xf71ade = pdfjsLib[_0x2a9b93(0x11a)]({
                    'data': _0x4abfe1[_0x2a9b93(0x109)][_0x2a9b93(0x116)]
                })
                  , _0x5af894 = await _0xf71ade[_0x2a9b93(0x143)];
                let _0x15398b = '';
                for (let _0x3d7e78 = 0x0; _0x3d7e78 < _0x5af894['numPages']; _0x3d7e78++) {
                    const _0x15194f = await _0x5af894['getPage'](_0x3d7e78 + 0x1)
                      , _0x169888 = await _0x15194f[_0x2a9b93(0x12c)]();
                    _0x169888[_0x2a9b93(0x134)]['forEach'](_0x2cc86a => {
                        const _0x35850e = _0x2a9b93;
                        _0x15398b += (_0x2cc86a[_0x35850e(0x162)] || '') + '\x20';
                    }
                    );
                }
                _0x590d13(_0x15398b[_0x2a9b93(0x152)]());
            } catch (_0xcbb285) {
                _0x4ffb14(new Error(_0x2a9b93(0x16d)));
            }
        }
        ,
        _0x69919d[_0x5478f8(0x16a)](_0x200848);
    }
    );
}
async function readDocx(_0x29737d) {
    return new Promise( (_0x3393e8, _0x450884) => {
        const _0xea4f57 = a0_0x1b37
          , _0x272c78 = new FileReader();
        _0x272c78['onload'] = function(_0x48eeac) {
            const _0x319733 = a0_0x1b37;
            mammoth[_0x319733(0x129)]({
                'arrayBuffer': _0x48eeac[_0x319733(0x109)][_0x319733(0x116)]
            })['then'](_0x2d931a => _0x3393e8(_0x2d931a[_0x319733(0x13a)]))[_0x319733(0x113)](_0x59c267 => _0x450884(_0x59c267));
        }
        ,
        _0x272c78[_0xea4f57(0x16a)](_0x29737d);
    }
    );
}
function createCSVDownloadLink(_0x30ff38) {
    const _0x4ff868 = a0_0x3f367b
      , _0x581da6 = _0x4ff868(0x16c) + _0x30ff38[_0x4ff868(0x127)](_0x2ca0e6 => _0x2ca0e6[_0x4ff868(0x147)] + ';' + _0x2ca0e6['aiTracesCount'] + ';' + _0x2ca0e6[_0x4ff868(0x159)] + ';' + _0x2ca0e6[_0x4ff868(0x136)] + ';' + _0x2ca0e6['claudeDetected'] + ';' + _0x2ca0e6[_0x4ff868(0x108)] + ';' + _0x2ca0e6[_0x4ff868(0x10c)] + ';' + _0x2ca0e6[_0x4ff868(0x164)])[_0x4ff868(0x123)]('\x0a')
      , _0x3ab0d5 = new Blob([_0x581da6],{
        'type': _0x4ff868(0x174)
    })
      , _0x45c5ad = URL['createObjectURL'](_0x3ab0d5)
      , _0x25bec7 = document['getElementById'](_0x4ff868(0x150));
    _0x25bec7[_0x4ff868(0x117)] = _0x45c5ad,
    _0x25bec7[_0x4ff868(0x10e)][_0x4ff868(0x15f)] = _0x4ff868(0x144),
    _0x25bec7[_0x4ff868(0x133)] = _0x4ff868(0x15b);
}
function a0_0x46af() {
    const _0x43021e = ['columns', 'getTextContent', ':\x20Unsupported\x20file\x20type</p>', 'feedbackClick_No', 'solid', 'match', '1166213mOvpIH', 'every', 'textContent', 'items', '4592085EPLxBQ', 'grammarlyDetected', '</p>', 'application/pdf', '6KAzBaX', 'value', '<br>\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20Copilot\x20Mentioned:\x20', '4448090qqRMXe', 'Llama/Meta\x20Mentioned', 'addRow', 'message', 'ChatGPT\x20Mentioned', '\x20was\x20created\x20before\x20November\x2022,\x202022\x20(the\x20introduction\x20of\x20ChatGPT)\x20and\x20was\x20skipped.</p>', 'lastModified', 'promise', 'block', 'files', 'fileInput', 'fileName', 'regularTracesCount', ';\x22><strong>', 'Yes', 'claudeDetected', '11484064uHhnZU', 'aiTracesCount', 'addWorksheet', '<p\x20style=\x22color:\x20', 'downloadLinkCSV', 'red', 'trim', 'fileScan', 'Copilot\x20Mentioned', ':</strong><br>\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20AI\x20Traces:\x20', 'includes', 'events', '4lULeEj', 'gptDetected', 'addEventListener', 'Download\x20CSV\x20Results', '67170lfnaWG', 'AI\x20Traces', 'fullres', 'display', 'feedbackNo', '1675402hcQqPG', 'str', 'length', 'copilotDetected', 'FF00FF00', 'feedbackClick_Yes', '36vCHdhy', 'black', ':\x20Error\x20processing\x20file.\x20', 'readAsArrayBuffer', 'push', 'File\x20Name;AI\x20Traces;ChatGPT\x20Mentioned;Grammarly\x20Mentioned;Claude\x20Mentioned;Gemini\x20Mentioned;Llama/Meta\x20Mentioned;Copilot\x20Mentioned\x0a', 'Failed\x20to\x20extract\x20text\x20from\x20PDF', 'output', 'test', 'forEach', 'eachRow', 'File\x20Name', 'name', 'text/csv', 'onload', '<br>\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20Grammarly\x20Mentioned:\x20', 'Grammarly\x20Mentioned', 'unsupportedFileAttempt', 'createObjectURL', 'geminiDetected', 'target', '<br>\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20Claude\x20Mentioned:\x20', 'Claude\x20Mentioned', 'llamaMetaDetected', 'xlsx', 'style', '<br></p>', 'writeBuffer', 'FF808080', 'Gemini\x20Mentioned', 'catch', 'fill', 'Download\x20Excel\x20Results', 'result', 'href', '<p>No\x20files\x20selected.\x20Please\x20upload\x20at\x20least\x20one\x20file.</p>', 'type', 'getDocument', '2788961Pulzey', 'getCell', 'getElementById', 'values', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'eachCell', 'click', 'preventDefault', 'join', 'Workbook', '2022-11-22', 'getTime', 'map', 'innerHTML', 'extractRawText', 'FFFF0000'];
    a0_0x46af = function() {
        return _0x43021e;
    }
    ;
    return a0_0x46af();
}
async function createExcelDownloadLink(_0x38fab8) {
    const _0x98da41 = a0_0x3f367b
      , _0x2cf765 = new ExcelJS[(_0x98da41(0x124))]()
      , _0x4fc035 = _0x2cf765[_0x98da41(0x14e)]('AI\x20Detection\x20Results');
    _0x4fc035[_0x98da41(0x12b)] = [{
        'header': _0x98da41(0x172),
        'key': _0x98da41(0x147),
        'width': 0x1e
    }, {
        'header': _0x98da41(0x15d),
        'key': _0x98da41(0x14d),
        'width': 0xa
    }, {
        'header': _0x98da41(0x140),
        'key': 'gptDetected',
        'width': 0x14
    }, {
        'header': _0x98da41(0x177),
        'key': _0x98da41(0x136),
        'width': 0x14
    }, {
        'header': _0x98da41(0x10b),
        'key': _0x98da41(0x14b),
        'width': 0x14
    }, {
        'header': _0x98da41(0x112),
        'key': _0x98da41(0x108),
        'width': 0x14
    }, {
        'header': _0x98da41(0x13d),
        'key': 'llamaMetaDetected',
        'width': 0x14
    }, {
        'header': _0x98da41(0x154),
        'key': _0x98da41(0x164),
        'width': 0x14
    }],
    _0x38fab8[_0x98da41(0x170)](_0x5692b2 => _0x4fc035[_0x98da41(0x13e)](_0x5692b2)),
    _0x4fc035[_0x98da41(0x171)]( (_0xf62740, _0x743093) => {
        const _0x75eee0 = _0x98da41;
        if (_0x743093 > 0x1) {
            const _0x131fb0 = _0xf62740[_0x75eee0(0x11c)](0x2)
              , _0x1f059f = _0xf62740[_0x75eee0(0x11e)][_0x75eee0(0x148)]
              , _0x2889c9 = [0x3, 0x4, 0x5, 0x6, 0x7, 0x8][_0x75eee0(0x127)](_0x443281 => _0xf62740[_0x75eee0(0x11c)](_0x443281))
              , _0x322317 = _0x2889c9[_0x75eee0(0x132)](_0xd1d3b1 => _0xd1d3b1[_0x75eee0(0x13a)] === 'No')
              , _0x444d61 = parseInt(_0x131fb0['value']) > 0x0 && _0x322317 && parseInt(_0x1f059f) == 0x0 ? _0x75eee0(0x111) : parseInt(_0x131fb0[_0x75eee0(0x13a)]) > 0x0 && _0x322317 ? _0x75eee0(0x12a) : _0x75eee0(0x165);
            _0xf62740[_0x75eee0(0x120)]({
                'includeEmpty': !![]
            }, _0x2e57e4 => {
                const _0x55de0c = _0x75eee0;
                _0x2e57e4[_0x55de0c(0x114)] = {
                    'type': 'pattern',
                    'pattern': _0x55de0c(0x12f),
                    'fgColor': {
                        'argb': _0x444d61
                    }
                };
            }
            );
        }
    }
    );
    const _0x10a69e = await _0x2cf765[_0x98da41(0x10d)][_0x98da41(0x110)]()
      , _0xc5e84 = new Blob([_0x10a69e],{
        'type': _0x98da41(0x11f)
    })
      , _0x25f4aa = URL[_0x98da41(0x179)](_0xc5e84)
      , _0x58796b = document[_0x98da41(0x11d)]('downloadLinkExcel');
    _0x58796b[_0x98da41(0x117)] = _0x25f4aa,
    _0x58796b[_0x98da41(0x10e)]['display'] = 'block',
    _0x58796b[_0x98da41(0x133)] = _0x98da41(0x115);
}
document[a0_0x3f367b(0x11d)]('feedbackYes')[a0_0x3f367b(0x15a)](a0_0x3f367b(0x121), _0x26787c => {
    const _0x133bec = a0_0x3f367b;
    _0x26787c[_0x133bec(0x122)](),
    window[_0x133bec(0x15e)] ||= {
        'events': []
    },
    window[_0x133bec(0x15e)][_0x133bec(0x157)][_0x133bec(0x16b)]({
        'key': _0x133bec(0x166),
        'response': 'Yes'
    });
}
),
document['getElementById'](a0_0x3f367b(0x160))['addEventListener'](a0_0x3f367b(0x121), _0x2f662c => {
    const _0x46dbe5 = a0_0x3f367b;
    _0x2f662c[_0x46dbe5(0x122)](),
    window[_0x46dbe5(0x15e)] ||= {
        'events': []
    },
    window[_0x46dbe5(0x15e)][_0x46dbe5(0x157)][_0x46dbe5(0x16b)]({
        'key': _0x46dbe5(0x12e),
        'response': 'No'
    });
}
);
